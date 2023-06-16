#Persona 3/4/5 PAK (.bin / .pac) format python implementation.


import serializeHelper

class pakedFile:
    def __init__(self, name="", content=b""):
        self.name = name
        self.content = content
    def exportFile(self, output):
        with open(output + self.name, "wb") as pakedFs:
            pakedFs.write(self.content)
    def deserializeFile(self, fileStream):
        self.name = fileStream.read(252).replace(b"\x00", b"").decode("ascii")
        fileDuration = serializeHelper.readIntLE(fileStream.read(4))
        if(self.name == "" or fileDuration == 0):
            return False
        self.content = fileStream.read(fileDuration)
        serializeHelper.align(fileStream)
        return True
    def serializeFile(self, fileStream):
        fileNameBytes = self.name.encode('ascii')
        fileStream.write(fileNameBytes)
        fileStream.seek(252-len(fileNameBytes), 1)
        fileStream.write(serializeHelper.writeIntLE(len(self.content)))
        fileStream.write(self.content)
        serializeHelper.align(fileStream)

class pakFile:
    def __init__(self, old=True):
        self.old = True
        self.files = []
    def deserialize(self, fileStream):
        fileState = True
        while(fileState == True):
            file = pakedFile()
            fileState = file.deserializeFile(fileStream)
            if not(file.name == ""):
                self.files.append(file)
    def serialize(self, fileStream):
        for file in self.files:
            file.serializeFile(fileStream)
        serializeHelper.align(fileStream)
        fileStream.write(b'\x01')
        
pak = pakFile()
with open("community2.bin", "rb") as fs:
    pak.deserialize(fs)

with open("community3.bin", "wb") as fs:
    pak.serialize(fs)



