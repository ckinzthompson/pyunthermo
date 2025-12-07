import ctypes
import subprocess
import numpy as np
from pathlib import Path

root = Path(__file__).resolve().parent
go_root = root / "unthermo"
dylib_path = go_root / "libunthermo.dylib"
export_dir = go_root / "export"

def load_lib():
	lib = ctypes.CDLL(dylib_path)

	lib.OpenFile.argtypes = [ctypes.c_char_p]
	lib.OpenFile.restype = ctypes.c_int

	lib.CloseFile.argtypes = [ctypes.c_int]
	lib.CloseFile.restype = None

	lib.NScans.argtypes = [ctypes.c_int]
	lib.NScans.restype = ctypes.c_int

	lib.GetScanSpectrum.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int)]
	lib.GetScanSpectrum.restype = ctypes.c_int

	return lib

def find_nscans(fn):
	lib = load_lib()
	fhandle = lib.OpenFile(fn.encode('utf-8'))
	nscans = lib.NScans(fhandle)
	lib.CloseFile(fhandle)
	return nscans

def load_all_spectra(fn):
	lib = load_lib()
	nscans = find_nscans(fn)
	print(f'Num. Scans: {nscans:5d}')

	fhandle = lib.OpenFile(fn.encode('utf-8'))

	## 1M seems safe
	data = []
	max_points = 10000000 

	for scan_number in range(1,nscans+1):
		mz = (ctypes.c_double * max_points)()
		inten = (ctypes.c_double * max_points)()
		npts = ctypes.c_int()
		## nb had to modify the scanevents load code b/c it read 8 bytes too many
		result = lib.GetScanSpectrum(fhandle, scan_number, 0, mz, inten, ctypes.byref(npts))  # 0 = raw
		if result == 0:
			mz_array = np.ctypeslib.as_array(mz, shape=(npts.value,))[:npts.value]
			inten_array = np.ctypeslib.as_array(inten, shape=(npts.value,))[:npts.value]
			data.append([mz_array,inten_array])

	assert len(data) == nscans
	lib.CloseFile(fhandle)
	data = np.array(data,).astype('float32')
	print(f'Data Shape:  {data.shape}')
	return data

def compile_dylib():
	print(root)
	print(go_root)
	print(dylib_path)
	print(export_dir)
	if not dylib_path.exists():
		cmd = [
			"go", "build",
			"-buildmode=c-shared",
			"-o", str(dylib_path),
			str(export_dir)
		]
		print('Go library not compiled. Compiling now.')
		subprocess.check_call(cmd, cwd=str(go_root))
		# print('Perhaps install go lang (brew install go)')
