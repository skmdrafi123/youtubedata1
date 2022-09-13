from urllib import request
from flask import Flask, render_template,request, jsonify
import youtubeData
import dbOperations

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    chanels=dbOperations.getAllChanels()

    return render_template("index.html", chanels=chanels)

@app.route('/log', methods=['GET'])
def log():
    chanels=dbOperations.getAllChanels()
    return render_template("log.html", chanels=chanels)

@app.route('/channeldetails/<string:Id>', methods=['GET'])
def channeldetails(Id: str):
    chanels=dbOperations.getAllChanels()
    Videos = dbOperations.getVideosByChannelId(Id)
    return render_template("channeldetails.html", chanels=chanels,videosList=Videos)

@app.route('/search', methods=['POST'])
def search():
    searchString = request.form['search'].replace(" ", "")
    data = youtubeData.GetLatestVideosUisngDataApi(searchString)
    dataItems = youtubeData.parse_search_response(data)
    if dataItems:
        #Get Chanel Details From Firt Item
        firstItem = dataItems[0]
        chanelId = firstItem['chanel_id']
        chanelName = firstItem['channelTitle']
        #Insert Chanel If not avilable in DB
        dbOperations.InsertChanelDetails(chanelId, chanelName)
        #Insert Videos if not avilable in DB
        dbOperations.InsertVideoDetails(dataItems)
        chanels = dbOperations.getAllChanels()
        dbOperations.InsertLog(chanelId)
        #AwsUploader.downloadVideos(chanelId)
    return render_template("result.html", videosList=dataItems,
                           message="Download Videos has been scheduled job", chanels=chanels)

if __name__ == '__main__':
    app.run()