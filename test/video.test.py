import sys
sys.path.append('..')
from tupu_api import TUPU

if __name__ == '__main__':
    tupu = TUPU(secret_id='54f50aa037e9880d6d2a86ee',
                private_key_path='./rsa_private_key.pem')
    # video sync url
    video = 'http://example.com/video.mp4'
    result = tupu.video_sync_api(video=video, is_url=True)
    print(result)

    # video sync file
    video = '/home/user/video.mp4'
    result = tupu.video_sync_api(video=video, is_url=False)
    print(result)

    # video async
    video = 'http://example.com/video.mp4'
    callbackUrl = 'http://example.com/callback'
    result = tupu.video_async_api(video=video, callbackUrl=callbackUrl)
    print(result)

    # video stream
    video = 'rtmp://example.com/stream'
    callbackUrl = 'http://example.com/callback'
    result = tupu.video_stream_api(video=video, callbackUrl=callbackUrl)
    print(result)

    # close video
    videoId = '5e425c8a3d69826ad7a77036'
    result = tupu.video_close_api(videoId=videoId)
    print(result)
