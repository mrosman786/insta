import base64
import json
import shutil
from glob import glob

import instaloader
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "welcome"


@app.route('/user/<username>')
def download_pic(username):
    ig = instaloader.Instaloader(compress_json=False)
    status = "success"
    try:
        ig.download_profile(username, profile_pic_only=True)
        profile_pic = glob(f"{username}/*.jpg")[0]
        read_file = open(profile_pic, "rb").read()
        base64_bytes = base64.b64encode(read_file)
        json_file = glob(f"{username}/*.json")[0]
        jdata = json.load(open(json_file))
        node = jdata.get('node')
    except:
        node = {}
        base64_bytes = b""
        status = "error"

    out = {
        "status": status,
        "id": node.get("id"),
        "username": node.get("username"),
        "full_name": node.get("full_name"),
        "biography": node.get("biography"),
        "following": node.get("edge_follow", {}).get("count"),
        "followers": node.get("edge_followed_by", {}).get("count"),
        "is_private": node.get("is_private"),
        "profile_pic_url_hd": node.get("profile_pic_url_hd"),
        "pic_code": base64_bytes.decode(),
    }

    shutil.rmtree(f'{username}', ignore_errors=True)
    return out


app.run()
