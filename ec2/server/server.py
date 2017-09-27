# -*- coding: utf-8 -*-
from flask import *
import boto3, botocore, json, datetime
from boto3 import *
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__, static_folder = 'templates', static_url_path = '')

error_page = '''
            <!DOCTYPE HTML>
            <html>
              <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <link rel="icon" href="favicon.ico" />
                <meta http-equiv="refresh" content="3;url=/">
                <title>UPMC HEALTHY DIET EVALUATION SYSTEM</title>
              </head>
              <body>You entered an invalid user ID, you will be redirected to homepage in 3 seconds ...</body>
            </html>
            '''

def get_status(score):
    return 'Unhealthy' if score < 40.0 else 'Healthy' if score > 70.0 else 'Fair'

def get_time_format(timestamp):
    return timestamp[:4] + '-' + timestamp[4:6] + '-' + timestamp[6:8] + ' ' + timestamp[8:10] + ':' + timestamp[10:12] + ':' + timestamp[12:14]

@app.route("/", methods=['GET', 'POST'])

def handle():
    if request.method == 'GET':
        return app.send_static_file("index.html")

    elif request.method == 'POST':
        try:
            userID = request.form['userID']
        #image = request.form['image']
        #s3_resource = boto3.resource('s3')
        #s3_resource.Bucket('ebiz17-team14-video-input-bucket').put_object(userID + '-' + str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))), Body = image)

        # connect database and send out the revised datas
        # ---
        except:
            return error_page

        if len(userID) == 0:
            return error_page

        dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1')
        table = dynamodb.Table('scores')
        response = table.query(
            Limit = 90,
            KeyConditionExpression = Key('userID').eq(userID),
            ScanIndexForward = False
        )
        response['Items'] = sorted(response['Items'], key = lambda item : int(item['time']), reverse = True)
        item_lenth = len(response['Items'])
        items = []
        imgNames = []
        if item_lenth == 0:
            return error_page
        elif item_lenth == 1:
            new_score = float(response['Items'][0]['score'])
            if new_score > 1:
                items.append(response['Items'][0])
            imgNames.append([str(get_time_format(response['Items'][0]['time'])), str('_'.join(response['Items'][0]['imgName'].split('_')[1:])), str(round(float(response['Items'][0]['score']), 1))])
        else:
            for item in response['Items']:
                imgNames.append([str(get_time_format(item['time'])), str('_'.join(item['imgName'].split('_')[1:])), str(round(float(item['score']), 1))])
            scores, count = -1, 1
            for index in range(0 , item_lenth):
                scores = float(response['Items'][index]['score'])
                if scores > 1:
                    break
            if scores < 0:
                return error_page
            i = index + 1
            while i < item_lenth:
                if response['Items'][i]['time'] == response['Items'][i - 1]['time']:
                    new_score = float(response['Items'][i]['score'])
                    if new_score > 1:
                        scores += new_score
                        count += 1
                    i += 1
                else:
                    if scores > 1:
                        response['Items'][i - 1]['score'] = scores / count
                        items.append(response['Items'][i - 1])
                    scores = float(response['Items'][i]['score'])
                    count = 1
                    i += 1
                    if i >= item_lenth:
                        break
                    while not scores > 1:
                        scores = float(response['Items'][i]['score'])
                        i += 1
                        if i >= item_lenth:
                            break
                            
            if scores > 1:
                response['Items'][item_lenth - 1]['score'] = scores / count
                items.append(response['Items'][item_lenth - 1])

        result = []
        monthDate = int((datetime.datetime.now() + datetime.timedelta(-30)).strftime('%Y%m%d%H%M%S'))
        weekDate = int((datetime.datetime.now() + datetime.timedelta(-7)).strftime('%Y%m%d%H%M%S'))
        monthTotal = 0.0
        monthNum = 0
        weekTotal = 0.0
        weekNum = 0
        for item in items:
            timestamp = item['time']
            time = int(timestamp)
            score = round(float(item['score']), 1)
            if time >= monthDate:
               monthTotal += score
               monthNum += 1
            if time >= weekDate:
               weekTotal += score
               weekNum += 1
            result.append([int(timestamp[:4]), int(timestamp[4:6]) - 1, int(timestamp[6:8]), int(timestamp[8:10]), int(timestamp[10:12]), int(timestamp[12:14]), score])

        score_weekly = 0.0
        score_monthly = 0.0
        if weekNum > 0:
            score_weekly = round(weekTotal / weekNum, 1)
            weekStatus = get_status(score_weekly)
        else:
            weekStatus = 'No records'
        if monthNum > 0:
            score_monthly = round(monthTotal / monthNum, 1)
            monthStatus = get_status(score_monthly)
        else:
            monthStatus = 'No records'

        return render_template("userInfo.html", data = result, week = score_weekly, status_week = weekStatus, month = score_monthly, status_month = monthStatus, user = userID, imgName = imgNames)

    else:
        redirect(url_for('/'))

if __name__ == '__main__':
    app.run(debug = True, host = "0.0.0.0", port = 80, threaded = True)
