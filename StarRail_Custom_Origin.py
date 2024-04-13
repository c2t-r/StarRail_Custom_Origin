import os
import json
from re import sub
from io import BufferedReader

with open("config.json", "r") as f:
    config = json.load(f)

your_origin = config["origin"]
cc_name = config["ClientConfig"]
sec_name = config["server_env_config"]

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

print("StarRail Custom Origin by c2tr\n")

os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

cc_path = os.path.join("input", cc_name)
cc_out_path = os.path.join("output", cc_name)
if cc_name and os.path.isfile(cc_path):
    f_cc_in = open(cc_path, "rb")
    f_cc_out = open(os.path.join("output", cc_name), "wb")

    f_cc_out.write(readOneByteString(f_cc_in))
    f_cc_out.write(readOneByteString(f_cc_in))
    f_cc_out.write(readOneByteString(f_cc_in))
    f_cc_out.write(readOneByteString(f_cc_in))
    f_cc_out.write(f_cc_in.read(2))
    f_cc_out.write(readArray(f_cc_in))
    f_cc_out.write(f_cc_in.read(16))

    f_cc_in.close()
    f_cc_out.close()

    print(cc_out_path)

sec_path = os.path.join("input", sec_name)
sec_out_path = os.path.join("output", sec_name)
if sec_name and os.path.isfile(sec_path):
    with open(sec_path, "r") as f:
        server_env_config = f.read()
    out_config = sub(r'https*://.+?([/"\?])', your_origin+"\\1", server_env_config)
    with open(sec_out_path, "w") as f:
        server_env_config = f.write(out_config)
    print(sec_out_path)

print("\nDone!")

# this script is written by c2tr. if you need my help, feel free to make issue
