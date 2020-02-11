import sys
sys.path.append('..')
from tupu_api import TUPU

if __name__ == '__main__':
    tupu = TUPU(secret_id='54f50aa037e9880d6d2a86ee',
                private_key_path='./rsa_private_key.pem')
    # image url
    images = ['http://example.com/image.jpg']
    result = tupu.api(images=images, is_url=True)
    print(result)

    # image file
    images = ['/home/user/image.jpg']
    result = tupu.api(images=images, is_url=False)
    print(result)
