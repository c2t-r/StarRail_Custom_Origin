import os
import json
from re import sub
from io import BufferedReader

with open("config.json", "r") as f:
    config = json.load(f)

your_origin = config["origin"]
ClientConfig_name = config["ClientConfig"]
server_env_config_name = config["server_env_config"]

def readOneByteString(f: BufferedReader):
    byte_length = f.read(2)
    length = int("0x" + byte_length.hex(), 0)
    string = f.read(length)
    return byte_length + string

def readArray(f: BufferedReader):
    out_bytes = []
    byte_length = f.read(2)
    length = int("0x" + byte_length.hex(), 0)
    out_bytes.append(byte_length)
    for i in range(length):
        byte_length = f.read(2)
        length = int("0x" + byte_length.hex(), 0)
        string = sub(r'https*://.+?([/"\?])', your_origin+"\\1", f.read(length).decode()).encode()
        out_bytes.append(bytes.fromhex(hex(len(string))[2:].zfill(4)))
        out_bytes.append(string)
    return b''.join(out_bytes)

os.makedirs("input", exist_ok=True)

ClientConfig_path = os.path.join("input", ClientConfig_name)
if ClientConfig_name and os.path.isfile(ClientConfig_path):
    f_cc_in = open(ClientConfig_path, "rb")
    f_cc_out = open(ClientConfig_name, "wb")

    f_cc_out.write(readOneByteString(f_cc_in))
    f_cc_out.write(readOneByteString(f_cc_in))
    f_cc_out.write(readOneByteString(f_cc_in))
    f_cc_out.write(readOneByteString(f_cc_in))
    f_cc_out.write(f_cc_in.read(2))
    f_cc_out.write(readArray(f_cc_in))
    f_cc_out.write(f_cc_in.read(16))

server_env_config_path = os.path.join("input", server_env_config_name)
if server_env_config_name and os.path.isfile(server_env_config_path):
    with open(server_env_config_path, "r") as f:
        server_env_config = f.read()
    out_config = sub(r'https*://.+?([/"\?])', your_origin+"\\1", server_env_config)
    with open(server_env_config_name, "w") as f:
        server_env_config = f.write(out_config)

# this script is written by c2tr. if you need my help, feel free to make issue
