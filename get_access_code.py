import base64
import os

path = os.path.dirname(__file__)


with open(os.path.join(path, "option.json"), 'w') as ioStream:
    file = ioStream.read()
    file = base64.b64encode(file.encode())
    ioStream.write(file)