import pytube
from googleapiclient.discovery import build
from datetime import datetime
from pytube import YouTube,Channel

api_key = "Your Key"
resource = build('youtube', 'v3', developerKey=api_key)


##Using Pytube
def GetTop50VideosFromChanel(chanelUrl):
    result = []
    c = Channel(chanelUrl)
    for url in c.video_urls[:50]:
        videoDetails=pytube.YouTube(url)
        result.append({
            'chanel_id': videoDetails.channel_id,
            'video_id': videoDetails.video_id,
            'video_title': videoDetails.title,
            'decription': videoDetails.description,
            'views': videoDetails.views,
            'videoDate': videoDetails.publish_date,
            'thumbnail_image': videoDetails.thumbnail_url,
            'VideosPath_url': '',
            'channelTitle': videoDetails.author,
            'CreatedDate': datetime.now()
        })

## Youtube Data API V3
def youtubeComents(video_id):
    request = resource.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100000,
        order="orderUnspecified")
    response = request.execute()
    items = response
    return items

def  parse_Coments_response(response):
    result = []
    items = response["items"]
    for item in items:
        item_info = item["snippet"]
        # the top level comment can have sub reply comments
        topLevelComment = item_info["topLevelComment"]
        comment_info = topLevelComment["snippet"]

        result.append({
            'CommentBy': comment_info["authorDisplayName"],
            'CommentText': comment_info["textDisplay"],
            'LikesonComment': comment_info["likeCount"],
            'CommentDate':  comment_info['publishedAt'],
            "videoId":item_info['videoId']
        })

    return result



## Youtube Data API V3
def GetLatestVideosUisngDataApi(channel_id):
    request = resource.search().list(
        part="snippet",
        channelId=channel_id,
        type="video",
        maxResults=20,
        order="date"
    )
    response = request.execute()
    return response

def parse_search_response(response):
    result = []
    for i, item in enumerate(response["items"]):

        yt = YouTube("https://www.youtube.com/watch?v=" + item['id']['videoId'])

        chanel_id = item["snippet"]["channelId"]
        video_id = item["id"]["videoId"]
        video_title = item['snippet']['title']
        decription= item['snippet']['description']
        views = yt.views
        videoDate = item['snippet']['publishTime']
        thumbnail_image = item['snippet']['thumbnails']['medium']['url']
        VideosPath_url = ''
        CreatedDate=datetime.now()
        channelTitle=item['snippet']['channelTitle']

        result.append({
            'chanel_id':chanel_id,
            'video_id': video_id,
            'video_title': video_title,
            'decription': decription,
            'views': views,
            'videoDate': videoDate,
            'thumbnail_image': thumbnail_image,
            'VideosPath_url': VideosPath_url,
            'channelTitle':channelTitle,
            'CreatedDate':CreatedDate
        })

    return result
