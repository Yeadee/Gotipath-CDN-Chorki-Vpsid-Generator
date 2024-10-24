import requests, re, datetime, json, hmac
from hashlib import sha1
from flask import request, redirect, render_template, url_for
from flask_smorest import Blueprint
from chorki.config import *

bp = Blueprint("chorki", "__name__", static_folder='static', template_folder='chorki/templates')

def vpsid_gen(message, key):
    key = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')
    digester = hmac.new(key, message, sha1)
    signature1 = digester.hexdigest()
    sig2 = signature1[0:20]
    return sig2

@bp.route("/chrkplay/<path:vurl>")
def chrkplay(vurl):
    if ".m3u8" in vurl:
        response = requests.get(vurl, headers=headers).text.replace("https://kms.chorki.com","/chkey")
        return response
    response = requests.get(vurl).content
    return response

@bp.route("/chkey/<path:keypath>")
def chkey(keypath):
    content_id = request.args["content_id"]
    base = "https://kms.chorki.com"
    key2 = "/" + keypath + "?content_id=" + content_id
    startime = datetime.datetime.now(datetime.UTC)-datetime.timedelta(minutes=5)
    stime = startime.strftime('%Y%m%d%H%M%S')
    endtime = datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes=10)
    etime = endtime.strftime('%Y%m%d%H%M%S')
    keyurl = f"{key2}?st={stime}&et={etime}"
    vpsid = vpsid_gen(keyurl, SECRET_KEY) ##SECRET KEY cannot be disclosed.
    keyhead = headers | {"vet":etime,"vpsid":vpsid,"vst":stime}
    url = base + key2
    key = requests.get(url,headers=keyhead).content
    return key

