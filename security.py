import PIL as pil
import pyotp
import core_functions as core
import qrcode

#
# To be honest this module isn't even important
# but I wanted to make it secure so I made the module.
#
# But hey its more secure than before. You can't argue with
# that
#

def verifyOtp(chat_id, key):
    raw_auth_list = core.openJsonFile("auth_list.json")
    user_key = raw_auth_list["core_admin"][str(chat_id)][0]
    otpkey = pyotp.TOTP(user_key)
    return(otpkey.verify(key))

def generateKey():
    return(pyotp.random_base32())

def generateOtpAppUrl(key, name, issuer):
    return(pyotp.totp.TOTP(key).provisioning_uri(name, issuer_name=issuer))
    
def generateAndSaveQrCode(data, save_name):
    img = qrcode.make(data)
    img.save(save_name)