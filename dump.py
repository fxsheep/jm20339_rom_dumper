import subprocess

def readb_indirect(address):
    addr_bytes = address.to_bytes(2, byteorder='big')
    cmd = ['sg_raw', '-o', 'tmp.bin', '-r', '256', '/dev/sda', '0x12', '0x00', '0x00'] + [str(hex(addr_bytes[0])), str(hex(addr_bytes[1]))]+ ['0x28']
    subprocess.run(cmd, check=True)
    with open('tmp.bin', 'rb') as f:
        f.seek(0x24)
        return f.read(1)

with open("jm20339_rom_dump_0x0.bin", "wb") as f:
    for i in range(0x0, 0x8000):
        f.write(readb_indirect(i))

