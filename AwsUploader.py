from pytube import YouTube
import boto3
import os
from io import BytesIO
import dbOperations

s3 = boto3.client('s3')

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='',
    aws_secret_access_key=''
)

def downloadVideos():
    download = dbOperations.getPendingVideos()
    for da in download:
        buffer = BytesIO()
        url = YouTube("https://www.youtube.com/watch?v=" + da[1])
        video = url.streams.get_by_itag(22)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        key = url.title.replace(' ','') + ".mp4"
        print(key)
        url=s3.Bucket('rafiyoutubedata').upload_fileobj(buffer, key)
        dbOperations.updateVideoPath(da[1],key)



downloadVideos()
# for da in download:
#     link = "https://www.youtube.com/watch?v=" + da[1]
#     yt = YouTube(link)
#     video = yt.streams.first()
#     file=video.download("videos")
#     key = video.title + ".mp4"
#     s3.Bucket('rafiyoutubedata').upload_file(file, key)
#     print(file)





