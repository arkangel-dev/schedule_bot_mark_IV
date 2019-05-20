import PIL as pil
import pyotp
import core_functions as core
import qrcode
import telepot
import json
import env

#
# To be honest this module isn't even important
# but I wanted to make it secure so I made the module.
#
# But hey its more secure than before. You can't argue with
# that
#

bot = telepot.Bot(env.TELEGRAM_BOT_API_KEY)

def verifyOtp(chat_id, key):
    # this is the function to verify an otp
    # request
    raw_auth_list = core.openJsonFile("auth_list.json")
    user_key = raw_auth_list["core_admin"][str(chat_id)][0]
    otpkey = pyotp.TOTP(user_key)
    return(otpkey.verify(key))

def generateKey():
    # this is the function to generate a key
    return(pyotp.random_base32())

def generateOtpAppUrl(key, name, issuer):
    # this the function to generate a url for the google authenticator to work
    return(pyotp.totp.TOTP(key).provisioning_uri(name, issuer_name=issuer))
    
def generateAndSaveQrCode(data, save_name):
    # this is the function to generate the qr code...
    # bascially just a function to generate a qr code... nothing more
    img = qrcode.make(data)
    img.save(save_name)

def updateQrCode(chat_id):
    # this is the function to update the qr code for the
    # user incase they fuck up
    raw_auth_list = core.openJsonFile("auth_list.json")
    username = bot.getChat(chat_id)["username"]
    new_key = generateKey()
    # del raw_auth_list["core_admin"][str(chat_id)]
    raw_auth_list["core_admin"].update({str(chat_id) : [new_key]})

    new_url = generateOtpAppUrl(new_key, username , "Friday Schedule Bot")
    generateAndSaveQrCode(new_url, "qr_code.png")
    core.saveJsonFile(raw_auth_list, "auth_list.json")
    return(True)