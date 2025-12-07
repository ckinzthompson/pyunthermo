# pyunthermo
This is a python wrapper around `unthermo` from proteininspector (https://bitbucket.org/proteinspector/ms/src/master/), which is a Go library for loading Thermo .raw files in a platform agnostic way. Thermo does provide DLLs but for Windows, so that's no good...

After compiling the Go library `unthermo`, the `pyunthermo` code acts as a python wrapper for the dylib using ctypes.

## License note
`pyunthermo` is just a wrapper over `unthermo` -- they did all of the work here. Licensing follows suit and uses the same license (Apache-2.0).

unthermo RAW Reader
Apache 2.0 license
Copyright ProteinInspector

This library includes software developed by ProteinInspector.

## Examples
```python
from pyunthermo import load_all_spectra
fn1 = 'spectrum.raw'
data = load_all_spectra(fn1)
```

## Functions

### load_all_spectra
* input: .raw filename (str,path)
* output: data (np.ndarray (Nscans,(x,y),Npoints))

### find_nscans 
* input: .raw filename (str,path)
* output: number of scans (int)

### compile_dylib
Compiles the Go library. Note, you may need to get the Go compiler first (`brew install go`)
* input: None
* output: None 


## Dusty Old Dev Notes

### Compiling Unthermo
* Get Go lang compiler on mac (`brew install go`)
* Compile without python
``` sh
cd ./pyunthermo/unthermo
go build -buildmode=c-shared -o libunthermo.dylib ./export
```

### Changes to unthermo
I have made a few changes to `unthermo` to make it work better for my use case: Loading all the MS1 scans from a .raw file into a numpy ndarray (in m/z space). The results are very close to that of the thermo DLL (as judged by mean UniDec extraction).

(Mildly Cocumented) Changes:
* In reader.go: the m/z conversion code wasn't working for all scans. This seem to be because `ScanEvent.Read` was reading 8 bytes too many so subsequent scans would be out of frame, and it would have to loop around over the course of several frames.
* In reader.go: the File.spectrum function now yield a dense m/z grid instead of just peaks.
* Finally, . Also, some convenience functions in there for me.