import mysql.connector
from datetime import datetime
import pymongo
import youtubeData

mydb = mysql.connector.connect(
  host="",
  user="admin",
  password="",
  database="sys"
)

client = pymongo.MongoClient("")

def getAllChanels():

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM channels")
    channels = mycursor.fetchall()
    return channels

def getVideosByChannelId(Id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Videos where ChannelId='" + Id + "'")
    videos = mycursor.fetchall()
    return videos

def getVideosTop100():
    mydb.reconnect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Videos  LIMIT 100")
    videos = mycursor.fetchall()
    return videos

def InsertChanelDetails(chanelId,chanelName):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT ChanelId Total FROM channels where ChanelId='"+chanelId+"'")
    myresult = mycursor.fetchall()
    if not myresult:
        sql1 = "INSERT INTO channels(ChanelId,ChanelName,CreatedOn) VALUES (%s, %s, %s)"
        val1 = (chanelId, chanelName, datetime.now())
        mycursor.execute(sql1, val1)
        mydb.commit()
        return 1

def InsertLog(chanelId):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT ChannelId Total FROM LogDetails where Status='Pending'")
    myresult = mycursor.fetchall()
    if not myresult:
        sql1 = "INSERT INTO LogDetails(ChannelId,Status,CreatedOn) VALUES (%s, %s, %s)"
        val1 = (chanelId,'Pending', datetime.now())
        mycursor.execute(sql1, val1)
        mydb.commit()
        return 1

def InsertVideoDetails(dataItems):
    for iterator in dataItems:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT VideoId Total FROM Videos where VideoId='" + iterator['video_id'] + "'")
        myresult = mycursor.fetchall()
        if not myresult:
            sql = "INSERT INTO Videos(ChannelId, VideoId, Title, Decription, Views, VideoDate, thumbnail, VideosPath, CreatedDate) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s)"
            val = (iterator['chanel_id'], iterator['video_id'], iterator['video_title'], iterator['decription'],
                   iterator['views'], iterator['videoDate'], iterator['thumbnail_image'], iterator['VideosPath_url'],
                   iterator['CreatedDate'])
            mycursor.execute(sql, val)
            mydb.commit()

            coments=youtubeData.youtubeComents(iterator['video_id'])
            comentsList=youtubeData.parse_Coments_response(coments)
            if comentsList:
                db1 = client['mongotest']
                coll = db1['comments']
                coll.insert_many(comentsList)

    return 1

def getPendingVideos():
    mycursor = mydb.cursor()
    mycursor.execute("select ID,VideoId from Videos where VideosPath='' limit 100")
    myresult = mycursor.fetchall()
    return myresult

def updateVideoPath(videoId,Path):
    mycursor = mydb.cursor()
    sql = "update Videos set VideosPath =%s where VideoId =%s"
    val = (Path,videoId)
    mycursor.execute(sql, val)
    mydb.commit()



def getDownloadPendingChannels():
    mycursor = mydb.cursor()
    mycursor.execute("select * from LogDetails where Status='Pending' limit 1")
    myresult = mycursor.fetchall()
    return myresult

