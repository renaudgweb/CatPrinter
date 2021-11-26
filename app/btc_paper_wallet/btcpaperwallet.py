from bitcoin import *
import qrcode
from qrcode.image.styledpil import StyledPilImage
import string
import random
import os

# spaces = "----------------------------------------------"
letters = string.ascii_letters + string.digits + string.ascii_lowercase + string.punctuation
crypto =  ''.join(random.choice(letters) for i in range(10000))

#PrivateKey
# print(spaces)
# key1 = "PrivateKey"
# print(key1)
priv = sha256 (crypto)
# print(priv)
f = open("txt1.txt", "w")
f.write(str(priv))
f.close()
# print(spaces)

#PublicKey
pub = privtopub(priv)

#WalletAdress
# key3 = ("WalletAdress")
# print(key3)
addr = pubtoaddr(pub)
# print(addr)
f = open("txt2.txt", "w")
f.write(str(addr))
f.close()
# print(spaces)

#QRCode generation
qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(addr)
img1 = qr.make_image(image_factory=StyledPilImage)
img1.save("publicwalletqr.png")

qr.add_data(priv)
img2 = qr.make_image(image_factory=StyledPilImage)
img2.save("privatekey-qrcode.png")
