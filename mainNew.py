import requests
from pytube import YouTube
from pytube import Channel
import mysql.connector
from datetime import datetime
import youtubeData

mydb = mysql.connector.connect(
  host="database-1.cfd6ooxyl9ve.ap-southeast-1.rds.amazonaws.com",
  user="admin",
  password="rafi1234",
  database="sys"
)

def youtubeChanel():
    c = Channel('https://www.youtube.com/channel/UCNU_lfiiWBdtULKOw6X0Dig')
    for url in c.video_urls[:50]:
        print(url)
def youtube():
    c = YouTube('https://www.youtube.com/watch?v=COTMO2sYJh0')
    print(c.views)
    print(c.title)
    print(c.description)
    print(c.publish_date)
    print(c.channel_id)
    print(c.video_id)
    print(c.thumbnail_url)
    print(c.author.title())

def getData():
    mycursor = mydb.cursor()
    sql = "INSERT INTO Videos(ChannelId, VideoId, Title, Decription, Likes, Comments, VideoDate, thumbnail, VideosPath, CreatedDate) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"
    val = ('Test','test2','test3','test4',1,123,datetime.now(),'test','dkdd',datetime.now())
    mycursor.execute(sql, val)
    mydb.commit()


def downloadYTV(link):
    SAVE_PATH = "C:/Rafi_Folder/Youtube_V"
    yt = YouTube(link)
    mp4files = yt.filter('mp4')
    yt.set_filename('Test.mp4')
    d_video = yt.get(mp4files[-1].extension, mp4files[-1].resolution)
    d_video.download(SAVE_PATH)

def latestVideos():
    api_url = "https://www.googleapis.com/youtube/v3/search?channelId=UCNU_lfiiWBdtULKOw6X0Dig&order=date&part=snippet&type=video&maxResults=10&key=AIzaSyDEVvW3u4bQHVZsmWRgt8Xa9d1LTtwHTno"
    response = requests.get(api_url)
    data=response.json()
    dataItems=data["items"]
    for d in dataItems:
        print(d["id"]["videoId"])

def InsertChanelDetails(chanelId,chanelName):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT ChanelId Total FROM Channels where ChanelId="+chanelId)
    myresult = mycursor.fetchall()
    if not myresult:
        sql1 = "INSERT INTO Channels(ChanelId,ChanelName,CreatedOn) VALUES (%s, %s, %s)"
        val1 = (chanelId, chanelName, datetime.now())
        mycursor.execute(sql1, val1)
        mydb.commit()
        return 1

def getComents(Id):
    print(youtubeData.youtubeComents(Id))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    response=youtubeData.youtubeComents('jLcuVu5xdDo')
    print(response)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
