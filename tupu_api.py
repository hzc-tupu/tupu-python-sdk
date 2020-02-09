"""
1. Install Dependencies
sudo pip install rsa requests base64 json

2. Interface
tupu_client = TUPU(secret_id, private_key_path, url)
parameter: "url" default is "http://api.open.tuputech.com/v3/recognition/"

3. Example

from tupu_api import TUPU
tupu = TUPU(secret_id="xxxxxxxxxxxxxxxxxx",
            private_key_path="./rsa_private_key.pem")
# url
images = ["http://example.com/001.jpg", "http://example.com/002.jpg"]
result = tupu.api(images=images, is_url=True)

# image file
images = ["/home/user/001.jpg", "/home/user/002.jpg"]
result = tupu.api(images=images, is_url=False)

# zip file
images = ["/home/user/001.zip", "/home/user/002.zip"]
result = tupu.api(images=images, is_url=False)
"""

import os
import random
import time
import rsa
import requests
import base64
import json
import mimetypes


TUPU_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDyZneSY2eGnhKrArxaT6zswVH9
/EKz+CLD+38kJigWj5UaRB6dDUK9BR6YIv0M9vVQZED2650tVhS3BeX04vEFhThn
NrJguVPidufFpEh3AgdYDzOQxi06AN+CGzOXPaigTurBxZDIbdU+zmtr6a8bIBBj
WQ4v2JR/BA6gVHV5TwIDAQAB
-----END PUBLIC KEY-----
"""

class TUPU:
    def __init__(self, secret_id, private_key_path, url='http://api.open.tuputech.com/v3/recognition/'):
        self.__url = url + ('' if url.endswith('/') else '/') + secret_id
        self.__video_sync_url = url + ('' if url.endswith('/') else '/') + 'video/syncscan/' + secret_id
        self.__video_async_url = url + ('' if url.endswith('/') else '/') + 'video/asyncscan/' + secret_id
        self.__secret_id = secret_id
        # get private key
        with open(private_key_path) as private_key_file:
            self.__private_key = rsa.PrivateKey.load_pkcs1(private_key_file.read())
        # get tupu public key
        self.__public_key = rsa.PublicKey.load_pkcs1_openssl_pem(TUPU_PUBLIC_KEY)

    def __sign(self):
        """get the signature"""
        self.__timestamp = time.time()
        self.__nonce = random.randint(1 << 4, 1 << 32)
        sign_string = "%s,%s,%s" % (self.__secret_id, self.__timestamp, self.__nonce)
        self.__signature = base64.b64encode(rsa.sign(sign_string.encode("utf-8"), self.__private_key, 'SHA-256')).decode('utf-8')

    def __verify(self, signature, verify_string):
        """verify the signature"""
        try:
            rsa.verify(verify_string.encode("utf-8"), base64.b64decode(signature), self.__public_key)
            return "Success"
        except rsa.pkcs1.VerificationError:
            print ("Verification Failed")
        return "Failed"

    def api(self, images, is_url=False):
        if not isinstance(images, list):
            raise Exception('[ArgsError] images is a list')
        self.__sign()
        request_data = {
            "timestamp": self.__timestamp,
            "nonce": self.__nonce,
            "signature": self.__signature
        }
        response = None
        if is_url:
            request_data["image"] = images
            response = requests.post(self.__url, data=request_data)
        else:
            multiple_files = []
            for image_file in images:
                if not os.path.isfile(image_file):
                    print ('[SKIP FILE] No such file "%s"' % image_file)
                    continue
                multiple_files.append(('image', (image_file, open(image_file, 'rb'), 'application/*')))
            response = requests.post(self.__url, data=request_data, files=multiple_files)
        response_json = json.loads(response.text)
        if not "error" in response_json:
            response_json['verify_result'] = self.__verify(response_json['signature'], response_json['json'])
            response_json['json'] = json.loads(response_json['json'])
        return response_json

    def video_sync_api(self, video, is_url=False, interval=1, maxFrames=200):
        if not video:
            raise Exception('video is required')
        self.__sign()
        request_data = {
            "timestamp": self.__timestamp,
            "nonce": self.__nonce,
            "signature": self.__signature,
            "interval": interval,
            "maxFrames": maxFrames
        }
        response = None
        if is_url:
            files = {'video': (None, video)}
        else:
            if not os.path.isfile(video):
                raise Exception('No such file "%s"' % video)
            mime = mimetypes.guess_type(video)
            files = {'video': (video, open(video, 'rb'), mime[0])}
        response = requests.post(self.__video_sync_url, data=request_data, files=files)
        response_json = json.loads(response.text)
        if not "error" in response_json:
            response_json['verify_result'] = self.__verify(response_json['signature'], response_json['json'])
            response_json['json'] = json.loads(response_json['json'])
        return response_json

    def video_async_api(self, video, callbackUrl, interval=1, realTimeCallback=False):
        if not video:
            raise Exception('video is required')
        if not callbackUrl:
            raise Exception('callbackUrl is required')
        self.__sign()
        request_data = {
            "timestamp": self.__timestamp,
            "nonce": self.__nonce,
            "signature": self.__signature,
            "video": video,
            "callbackUrl": callbackUrl,
            "interval": interval,
            "realTimeCallback": realTimeCallback
        }
        response = requests.post(self.__video_async_url, json=request_data)
        response_json = json.loads(response.text)
        if not "error" in response_json:
            response_json['verify_result'] = self.__verify(response_json['signature'], response_json['json'])
            response_json['json'] = json.loads(response_json['json'])
        return response_json
