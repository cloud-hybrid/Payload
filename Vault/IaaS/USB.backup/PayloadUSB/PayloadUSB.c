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
#include <stdio.h>
#include <libusb-1.0/libusb.h>

static PyObject * payloadUSB_devices(PyObject *self, libusb_device **devices) {
  libusb_device *device;
  int usb_iterator = 0;
  int path_iterator = 0;
  uint8_t path[8];

  while ((device = devices[usb_iterator++] != NULL))
    {
      struct libusb_device_descriptor description;
      int description_address = libusb_get_device_descriptor(device, &description);

      if (description_address < 0) {
        fprintf(stderr, "Error: Failed to get device descriptor.");
        return;
      }

      printf(
        "%04x:%04x (bus %d, dev %d)",
        description.idVendor, description.idProduct,
        libusb_get_bus_number(device),
        libusb_get_device_address(device)
      );

      int ports = libusb_get_port_numbers(device, path, sizeof(path));
      if (ports > 0) {
        printf(" path: %d", path[0]);

        for (path_iterator = 1; path_iterator < ports; path_iterator++) {
          printf(".%d", path[path_iterator]);
        }
      }
      printf("\n");
    }
    libusb_free_device_list(devices, 1);
    return Py_BuildValue(NULL);
  };

static char devices_documentation[] = "devices( ): Print USB Devices.\n";

static PyMethodDef PayloadUSBDevices_Methods[] = {
  {
    "payloadUSB_devices",
    payloadUSB_devices,
    METH_NOARGS,
    devices_documentation
  }, {NULL, NULL, 0, NULL}
};

static struct PyModuleDef PayloadUSBDevices = {
  PyModuleDef_HEAD_INIT,
  "PayloadUSBDevices",
  "PayloadUSBDevices's Devices Module.",
  -1,
  PayloadUSBDevices_Methods
};

PyMODINIT_FUNC PyInit_PayloadUSB(void) {
  return PyModule_Create(&PayloadUSBDevices);
};