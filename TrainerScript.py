# Enable Multithreading
import threading
import logging
import time

import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt, style
from pathlib import Path
import os
import re
from statistics import mean
import numpy as np

style.use('ggplot')
# def Main():

scale_percent = 50

sift = cv2.xfeatures2d.SIFT_create()  # patent - only free for academic purpose

try:

    image_to_compare = cv2.imread(r'people\dependent2.jpg')

    original = cv2.imread(r'people\independent.jpg')

    grayImageCompare = cv2.cvtColor(image_to_compare, cv2.COLOR_BGR2GRAY)
    cv2.createBackgroundSubtractorMOG2().apply(grayImageCompare)
    # calculate the 50 percent of original dimensions
    # Originalwidth = int(grayImageCompare.shape[1])
    # Originalheight = int(grayImageCompare.shape[0])
    # Originaldsize = (Originalwidth, Originalheight)

    width = int(grayImageCompare.shape[1] * scale_percent / 100)
    height = int(grayImageCompare.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    FinalImageCompare = cv2.resize(grayImageCompare, dsize)

    kp_2, desc_2 = sift.detectAndCompute(FinalImageCompare, None)

    # Should probably move to the top
    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    # put These into an array (Datasets)
    grayImage = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    # (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    # calculate the 50 percent of original dimensions
    width = int(grayImage.shape[1] * scale_percent / 100)
    height = int(grayImage.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    FinalImage = cv2.resize(grayImage, dsize)

    # 2) Check for similarities between the 2 images

    kp_1, desc_1 = sift.detectAndCompute(FinalImage, None)

    # bf = cv2.BFMatcher()
    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points2 = []
    # x1 = []
    # y1 = []
    for m, n in matches:
        good_points2.append(m)
    # if m.distance < 0.6 * n.distance:
    #    x1.append(m.distance)
    #   y1.append(n.distance)

    # print(len(good_points2))
    # plt.scatter(x1, y1, label="stars", color="green",marker="*", s=30)

    # x-axis label
    # plt.xlabel('x - axis')
    # frequency label
    # plt.ylabel('y - axis')
    # plot title
    # plt.title('My scatter plot!')
    # showing legend
    # plt.legend()

    # plt.show()
    # function to show the plot

    # img_matches2 = np.empty((max(grayImageCompare.shape[0], grayImage.shape[0]), grayImageCompare.shape[1] + grayImage.shape[1], 3),dtype=np.uint8)

    # draw2 = cv2.drawMatches(grayImageCompare, kp_1, grayImage, kp_2, good_points2, img_matches2,flags=2)

    # cv2.imwrite('imageCorrespondence.png', draw2)

    good_points = []
    x2 = []
    y2 = []

    good_pointsimg2 = []
    ximg2 = []
    yimg2 = []

    for m, n in matches:
        print("m " + str(m.distance))
        print("n " + str(n.distance))

        if 0.6 * n.distance > m.distance:
            good_points.append(m)

            img1_idx = m.queryIdx
            img2_idx = n.trainIdx

            x2.append(m.distance)
            y2.append(n.distance)

            (xa1, ya1) = kp_1[img1_idx].pt
            (xa2, ya2) = kp_2[img2_idx].pt
            print((xa1, ya1))
    #     ximg2.append((x, y))
    #    yimg2.append((x2, y2))

    # print(ximg2)

    print("test2 " + str(len(good_points2)))

    print("test " + str(len(good_points)))

    npx = np.array(x2, dtype=np.float64)
    npy = np.array(y2, dtype=np.float64)

    # def best_fit_slope_and_intercept(xs, ys):
    mx = (((mean(npx) * mean(npy)) - mean(npx * npy)) /
          ((mean(npx) ** 2) - mean(npx ** 2)))
    print("m = " + str(mx))
    by = mean(npx) - mx * mean(npx)

    #   return mx, by

    # m, b = best_fit_slope_and_intercept(x2, y2)

    print("b =" + str(by))
    regression_line = [(mx * x) + by for x in x2]

    regression_line = []
    for x in x2:
        regression_line.append((mx * x) + by)

    # plt.scatter(x2, y2, label="stars", color="green", marker="*", s=30)

    plt.scatter(x2, y2, color='#003F72')

    plt.plot(x2, regression_line)
    # x-axis label
    plt.xlabel('x - axis')
    # frequency label
    plt.ylabel('y - axis')
    # plot title
    plt.title('My scatter plot!')
    # showing legend
    plt.legend()

    plt.show()
    # function to show the plot
    plt.show()

    img_matches = np.empty(
        (max(grayImageCompare.shape[0], grayImage.shape[0]), grayImageCompare.shape[1] + grayImage.shape[1], 3),
        dtype=np.uint8)

    draw = cv2.drawMatches(grayImageCompare, kp_1, grayImage, kp_2, good_points, img_matches,
                           flags=2)
    # -- Show detected matches
    cv2.imshow('Good Matches', draw)
    cv2.imwrite('imageCorrespondence2.png', draw)
    print('Image Saved')
    print("Percentage = " + str((
                                        (
                                                len(good_points2) - len(good_points)
                                         ) / len(good_points2)) * 100))

    cv2.waitKey()
except Exception as e:
    print("Oops!", e.__class__, "occurred.")
    print("Next entry.")
    print()

# Main()
# try:
# while True:
# print("New thread started")
# x = threading.Thread(target=Main(), args=(1,))
# x.start()
# except:
#   print("Error")
# while 1:
#   pass
