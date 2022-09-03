# nvidia-switch

A utility that completely turns of NVIDIA dGPU to save power.

## Prerequisites

* acpi-call-dkms
* initramfs-tools
* proprietary NVIDIA driver

## Installation

Before installing make sure module **acpi_call** is loaded at boot time. This is done by adding a kmod configuration file.

```bash
echo acpi_call > /etc/modules-load.d/acpi_call.conf
```

To install the utility:

```bash
cd nvidia-switch
./switch install
```

To remove the utility:

```bash
./switch remove
```

## Usage

To enable integrated graphics only:

```bash
prime-select intel
```

To enable hybrid graphics:

```bash
prime-select nvidia
```
