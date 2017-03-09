import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=0,
)
qr.add_data(1)
qr.make(fit=True)

img = qr.make_image()
img.save("another.png")
