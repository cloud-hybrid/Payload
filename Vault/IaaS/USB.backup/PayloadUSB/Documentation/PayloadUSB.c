/*
Function Syntax:
static PyObject *module_func(PyObject *self, PyObject *args) {
  *** Do stuff ***
  Py_RETURN_NONE;
}

Method/Mapping Table Syntax:
struct PyMethodDef {
  char *module_name;
  PyCFunction module_method;
  int module_flags;
  char *module_doc;
};
*/

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <libusb-1.0/libusb.h>

static PyObject * introduction(PyObject* self) {
  return Py_BuildValue("s", "Welcome to PayloadUSB's USB Wrapper");
}

static char introduction_documentation[] = "introduction( ): Print Introduction Message.\n";

static PyMethodDef PayloadUSBIntroduction_Methods[] = {
  {
    "introduction",
    introduction,
    METH_NOARGS,
    introduction_documentation
  }, { NULL, NULL, 0, NULL }
};

static struct PyModuleDef PayloadUSBIntroduction = {
  PyModuleDef_HEAD_INIT,
  "PayloadUSB",
  "PayloadUSB's Introduction Module.",
  -1,
  PayloadUSBIntroduction_Methods
};

PyMODINIT_FUNC PyInit_PayloadUSB(void) {
  return PyModule_Create(&PayloadUSBIntroduction);
}