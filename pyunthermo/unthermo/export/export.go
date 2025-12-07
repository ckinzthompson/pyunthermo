package main

import "C"
import (
	"pyunthermo/unthermo"
	"sync"
	"unsafe"
)

var (
	mu    sync.Mutex
	files = map[int]*unthermo.File{}
	next  = 1
)

//export OpenFile
func OpenFile(path *C.char) C.int {
	f, err := unthermo.Open(C.GoString(path))
	if err != nil {
		return 0 // failed to open
	}

	mu.Lock()
	id := next
	next++
	files[id] = &f // store pointer to struct
	mu.Unlock()
	return C.int(id)
}

//export CloseFile
func CloseFile(id C.int) {
	mu.Lock()
	f, ok := files[int(id)]
	if ok {
		f.Close()
		delete(files, int(id))
	}
	mu.Unlock()
}

//export NScans
func NScans(id C.int) C.int {
	mu.Lock()
	f, ok := files[int(id)]
	mu.Unlock()
	if !ok || f == nil {
		return -1
	}
	return C.int(f.NScans())
}

//export GetScanSpectrum
func GetScanSpectrum(fileID C.int, scanNumber C.int, centroid C.int, mzOut *C.double, intOut *C.double, nPoints *C.int) C.int {
	mu.Lock()
	f, ok := files[int(fileID)]
	mu.Unlock()
	if !ok || f == nil {
		return -1
	}

	scan := f.Scan(int(scanNumber))
	spectrum := scan.Spectrum(centroid == 1) // 0 = raw profile, 1 = centroided
	if len(spectrum) == 0 {
		*nPoints = 0
		return 0
	}

	*nPoints = C.int(len(spectrum))
	ptrMz := (*[1 << 30]C.double)(unsafe.Pointer(mzOut))
	ptrInt := (*[1 << 30]C.double)(unsafe.Pointer(intOut))
	for i, p := range spectrum {
		ptrMz[i] = C.double(p.Mz)
		ptrInt[i] = C.double(p.I)
	}
	return 0
}

func main() {}
