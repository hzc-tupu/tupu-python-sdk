# TUPU Python SDK

SDK for TUPU visual recognition service
######
<https://www.tuputech.com>

## Install Dependencies
```
sudo pip install rsa requests base64 json
```

## Interface
```
tupu_client = TUPU(secret_id, private_key_path, url)
```

#### Parameters
- **secretId**: user's secret-id for accessing the API
- **private_key_path**: user's private key path
- **url**: default is "http://api.open.tuputech.com/v3/recognition/"

## Example
```
from tupu_api import TUPU
tupu = TUPU(secret_id='xxxxxxxxxxxxxxxxxx',
                    private_key_path='./rsa_private_key.pem')
# url
images = ["http://example.com/001.jpg", "http://example.com/002.jpg"]
result = tupu.api(images=images, is_url=True)
# image file
images = ["/home/user/001.jpg", "/home/user/002.jpg"]
result = tupu.api(images=images, is_url=False)
# zip file
images = ["/home/user/001.zip", "/home/user/002.zip"]
result = tupu.api(images=images, is_url=False)

print result["verify_result"]
```

## Video API

#### 1. Video Sync API
```python
tupu.video_sync_api(video [, is_url, interval, maxFrames, tag])
```
detail specification can be found [here.](http://cloud.doc.tuputech.com/API/video/syncscan/)

example:
```python
# video url
video = 'http://example.com/video.mp4'
result = tupu.video_sync_api(video=video, is_url=True)

# video file
video = '/home/user/video.mp4'
result = tupu.video_sync_api(video=video, is_url=False)
```

#### 2. Video Async API
```python
tupu.tupu.video_async_api(video, callbackUrl [, interval, realTimeCallback, audio, customInfo, callbackRules])
```
detail specification can be found [here.](http://cloud.doc.tuputech.com/API/video/asyncscan/#1)

example:
```python
video = 'http://example.com/video.mp4'
callbackUrl = 'http://example.com/callback'
result = tupu.video_async_api(video=video, callbackUrl=callbackUrl)
```

#### 3. Video Stream API
```python
tupu.tupu.video_stream_api(video, callbackUrl [, interval, customInfo, callbackRules])
```
detail specification can be found [here.](http://cloud.doc.tuputech.com/API/video/asyncscan/#2)

example:
```python
video = 'rtmp://example.com/stream'
callbackUrl = 'http://example.com/callback'
result = tupu.video_stream_api(video=video, callbackUrl=callbackUrl)
```

#### 4. Video Close API
```python
tupu.tupu.video_close_api(videoId)
```
detail specification can be found [here.](http://cloud.doc.tuputech.com/API/video/asyncscan/#3)

example:
```python
videoId = '5e425c8a3d69826ad7a77036'
result = tupu.video_close_api(videoId=videoId)
```
