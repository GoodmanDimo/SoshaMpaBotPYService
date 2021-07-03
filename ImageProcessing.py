import cv2 as cv2
from cv2 import imread, cvtColor

scale_percent = 50

sift = cv2.xfeatures2d.SIFT_create()  # patent - only free for academic purpose


def ComputeUserImage(image1):
    image_to_compare = imread(image1)

    grayImageCompare = cvtColor(image_to_compare, cv2.COLOR_BGR2GRAY)

    cv2.createBackgroundSubtractorMOG2().apply(grayImageCompare)

    width = int(grayImageCompare.shape[1] * scale_percent / 100)
    height = int(grayImageCompare.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)
    # resize image
    FinalImageCompare = cv2.resize(grayImageCompare, dsize)

    kp_2, desc_2 = sift.detectAndCompute(FinalImageCompare, None)

    return kp_2, desc_2

def ComputeDataseImages(image2Path):


    descArry = []
    imagename = []
    for imageItem in image2Path:

        image2 = "images/" + imageItem

        original = imread(image2)  # put These into an array (Datasets)

        grayOriginalImage = cvtColor(original, cv2.COLOR_BGR2GRAY)

        cv2.createBackgroundSubtractorMOG2().apply(grayOriginalImage)

        # calculate the 50 percent of original dimensions
        OringinalResizewidth = int(grayOriginalImage.shape[1] * scale_percent / 100)
        OringinalResizeheight = int(grayOriginalImage.shape[0] * scale_percent / 100)

        # dsize
        Originaldsize = (OringinalResizewidth, OringinalResizeheight)

        # resize image
        FinalOriginalImage = cv2.resize(grayOriginalImage, Originaldsize)

        # 2) Check for similarities between the 2 images
        kp_1, desc_1 = sift.detectAndCompute(FinalOriginalImage, None)
        descArry.append(desc_1)
        imagename.append(imageItem)

    return descArry, imagename


def main(image1, descriptionAry, image2Ary):

    KP2, desc_2 = ComputeUserImage(image1)

    counter = -1

    # Should probably move to the top
    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    for desc_1 in descriptionAry:

        counter += 1
        # bf = cv2.BFMatcher()
        matches = flann.knnMatch(desc_1, desc_2, k=2)

        good_points2, good_points = [], []

        for m, n in matches:
            good_points2.append(m)
            if 0.6 * n.distance > m.distance:
                good_points.append(m)


        a = len(good_points)
        percent = (a * 100) / len(KP2)
        print("{} % similarity".format(percent))
        if percent >= 75.00:
            print('Match Found')
        if percent < 75.00:
            print('Match not Found')

        perc = (
                       (
                               len(good_points2) - len(good_points)
                       ) / len(good_points2)) * 100

        image2 = image2Ary[counter]
        print('Perc' + str(perc) + ' ' + image2)

        if perc < 99:

            return True, perc, image2, 1
        else:
            continue

    return False, 0.0, 'Not Found', 0
