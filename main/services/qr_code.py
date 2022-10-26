import qrcode
import os

from django.conf import settings

# Create your send qr-code here.


# Create QR Code (for your referral link)
def create_qr_code(ref_link):
    data = 'http://' + settings.ALLOWED_HOSTS[0] + '/registration/' + ref_link + '/'

    filename = f"{ref_link}.png"
    img = qrcode.make(data)

    if not os.path.exists("media/referral_qr_code/"):
        os.mkdir("media/referral_qr_code")

    img.save(f"media/referral_qr_code/{filename}")
