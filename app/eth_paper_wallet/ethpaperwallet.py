import qrcode
from qrcode.image.styledpil import StyledPilImage
import numpy
from ecdsa import SigningKey, SECP256k1
import sha3
import random
import os

def checksum_encode(addr_str):  # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

# Generating new wallet
keccak = sha3.keccak_256()
priv = SigningKey.generate(curve=SECP256k1)
pub = priv.get_verifying_key().to_string()
keccak.update(pub)
address = keccak.hexdigest()[24:]
privstr = priv.to_string().hex()
addrstr = checksum_encode(address)

f = open("txt1.txt", "w")
f.write(str(privstr))
f.close()

f = open("txt2.txt", "w")
f.write(str(addrstr))
f.close()

qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(addrstr)
img1 = qr.make_image(image_factory=StyledPilImage)
img1.save("publicwalletqr.png")

qr.add_data(privstr)
img2 = qr.make_image(image_factory=StyledPilImage)
img2.save("privatekey-qrcode.png")

qr.add_data('https://etherscan.io/address/'+addrstr)
img3 = qr.make_image(image_factory=StyledPilImage)
img3.save("balancekey-qrcode.png")
