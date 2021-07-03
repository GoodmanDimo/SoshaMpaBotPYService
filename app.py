import os
import os.path
from os import path
import base64
from flask import Flask, request
from flask_pymongo import PyMongo
import ImageProcessing as Iprocessor

import threading

app = Flask(__name__)

app.config[
    "MONGO_URI"] = "mongodb+srv://Goodies:AmoThato@cluster0.gdvvp.mongodb.net/UserImages?retryWrites=true&w=majority"
myclient = PyMongo(app)
mydb = myclient.db
mycol = mydb["cUserImages"]


def getDBReCords(ID):
    cursor = mycol.find({}, {"ImageEntry": 1, "UserIP": ID, "Category": 1, "Results": "Pending",
                             "CurrentLocation": "Unknown", "_id": 0})

    for x in cursor:

        imgdata = x["ImageEntry"]
        # imageCategory = x["Category"]
        imageIP = x["UserIP"]

        # Datenow = datetime.now()  # time object

        filename = 'ProcessingTemp/' + str(imageIP) + '_Process.png'

        if path.exists(filename):
            os.remove(filename)

        base64_img_bytes = imgdata.encode('utf-8')
        with open(filename, 'wb') as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            file_to_save.write(decoded_image_data)
        # mycol.delete_one(x)


def Main(ID):
    image1 = "ProcessingTemp/" + ID + "_Process.png"

    ImageListPath = os.listdir("images/")

    match, perc, LocationName, Results = Iprocessor.main(image1,descriptionAry, image2Ary)

    LocationSplit = LocationName.split('_')
    Location = LocationSplit[1]

    getuserRecordQuery = {"UserIP": ID, "Results": "Pending"}

    results2 = {"$set": {"CurrentLocation": Location}}
    mycol.update_one(getuserRecordQuery, results2)

    # find loaction name from the file name
    results = {"$set": {"Results": Results}}
    # return await
    mycol.update_one(getuserRecordQuery, results)


@app.route("/index", methods=['GET'])
def index():
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    getDBReCords(id)

    t = threading.Thread(target=Main, args=[id])
    # setDaemon=False to stop the thread after complete
    t.setDaemon(False)
    # starting the thread
    t.start()

    print('thread started')
    return 'Background work still in progress'


# image1 = "testImages/test1.jpg"
# image2 = "testImages/test2.jpg"

# match = Iprocessor.main(image1, image2)

# https://docs.microsoft.co                m/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask
# return "Congratulations, it's a web app! for help go to https://realpython.com/python-web-applications/" \
#      + " Hello Mongo is working "


if __name__ == "__main__":

    ImageListPath = os.listdir("images/")
    descriptionAry, image2Ary = Iprocessor.ComputeDataseImages(ImageListPath)

    #app.run(host="127.0.0.1", port=8080, debug=True)
    app.run(host="192.168.8.100", port=8080, debug=True)
