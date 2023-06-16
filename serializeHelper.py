def readIntLE(bytes):
    return int.from_bytes(bytes, 'little')

def writeIntLE(num):
    return num.to_bytes(4, 'little')

def align(fs, alignSize=64):
    diff = fs.tell() % alignSize
    diff = alignSize - diff
    diff = diff % alignSize
    fs.seek(diff, 1)
