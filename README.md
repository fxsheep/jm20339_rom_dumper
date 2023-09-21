# jm20339_rom_dumper
Dumping the internal ROM of JM20339 USB2.0-to-SATA converter 

## Requirements
 - python3
 - sg3-utils
 - bsdiff
 - Windows VM
 - A JM20339 based adapter that supports firmware update(has an SPI flash, not 93C46 EEPROM)
 - Firmware package `jmicron_2033x_mptool_v11303.rar` which can be found on usbdev.ru

## Usage
 - Unpack the firmware package and get `339 MinAik v1.11 CD.bin`. (SHA256: d74924f19c15be4e7953210c93d015a699a6f12224026295cd960464debdef47)
 - Patch it with bspatch: `bspatch 339\ MinAik\ v1.11\ CD.bin newfirm.bin fw_patch.diff`
 - Flash the patched firmware `newfirm.bin` using `JMMassProd` under Windows.
 - Dump ROM under Linux(running under tmpfs is advised): `sudo python3 dump.py`

## How it works
During initial analysis when I didn't have the internal ROM, I had no idea of how the external firmware is invoked by ROM. Therefore I can only find code snippets but could not chain them together. I've then found the code responsible for adding `j339` to the end of the reply of INQUIRY command(and many others). By patching a few lines, the INQUIRY command is changed to allow reading one byte from an arbitrary address in CODE space.

The patch:
```
	mov	DPTR,#0xff12
	movx	A,@DPTR
	mov	R7,A
	inc	DPTR
	movx	A,@DPTR
	mov	DPH,R7
	mov	DPL,A
	clr	A
	movc	A,@A+DPTR
	mov	DPTR,#0xff54
	movx	@DPTR,A
```

## TODO
 - Make this easier and without vendor tools(and Windows)
 - Port to those without an SPI flash, and to ROM-only variants(e.g. JM20329)
