import qrcode
import base64
from io import BytesIO
# from qrcode.image.styledpil import StyledPilImage

def mb64qr(bolt11):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=4,
        border=4,
    )

    qr.add_data(bolt11)
    qr.make(fit=True)
    # img = qr.make_image(image_factory=StyledPilImage, embeded_image_path="route/func/icon.png")
    img = qr.make_image(embeded_image_path="route/func/icon.png")

    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f'data:image/png;base64,{img_str}'