
from pymongo import MongoClient

from datetime import datetime

import base64

import ImageProcessing as Iprocessor
import os

from multiprocessing import Process

myclient = MongoClient("mongodb+srv://Goodies:AmoThato@cluster0-gdvvp.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["UserImages"]
mycol = mydb["cUserImages"]


# mycol.inventory.find( { status: "A" }, { item: 1, status: 1, _id: 0 } )

# SELECT item, status from inventory WHERE status = "A"


# mycol.find( {"ImageEntry": 1, "_id": 0 } )

def getDBReCords():
    cursor = mycol.find({}, {"ImageEntry": 1, "UserIP": 1, "Category": 1, "Results": "Pending",
                             "CurrentLocation": "Unknown", "_id": 0})

    counter = 0
    for x in cursor:
        imgdata = x["ImageEntry"]
        imageCategory = x["Category"]
        imageIP = x["UserIP"]

        counter = counter + 1

        Datenow = datetime.now()  # time object

        base64_img_bytes = imgdata.encode('utf-8')
        with open('ProcessingTemp/Userimage_Category' + str(imageCategory) + '_' + str(imageIP) + "_Process" + '.png',
                  'wb') as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            file_to_save.write(decoded_image_data)
        # mycol.delete_one(x)


def Main():
    ImageInputs = os.listdir("ProcessingTemp")

    for ImageInputItem in ImageInputs:
        image1 = 'ProcessingTemp/' + ImageInputItem

        categorysplit = ImageInputItem.split('_')
        userIP = categorysplit[2]

        print(ImageInputItem)

        ImageList = os.listdir("images/" + str(categorysplit[1]))
        for ImageListItems in ImageList:
            image2 = 'images/' + str(categorysplit[1]) + '/' + ImageListItems

            print(image2)
            match = Iprocessor.main(image1, image2)

            print(match)
            getuserRecordQuery = {"UserIP": userIP, "Results": "Pending"}
            print(getuserRecordQuery)

            if match:
                # find loaction name from the file name
                results = {"$set": {"Results": "1"}, "$set": {"CurrentLocation": "image2"}}
                return await mycol.update_one(getuserRecordQuery, results)

            else:
                results = {"$set": {"Results": "0"}, "$set": {"CurrentLocation": "Not Found"}}
                mycol.update_one(getuserRecordQuery, results)

        # os.remove(image1)


if __name__ == '__main__':
    p1 = Process(target=getDBReCords)
    p1.start()
    p2 = Process(target=Main)
    p2.start()
# os.rename('decoded_image.png', 'Userimg_' + str(imageIP) + str(Datenow) + '.png')
