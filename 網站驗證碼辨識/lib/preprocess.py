import cv2
import numpy as np
import time
import os


def getVProjection(image):
    vProjection = np.zeros(image.shape, np.uint8)
    (h, w) = image.shape
    # 長度與圖寬一致的組
    w_ = [0] * w

    # 循環統計每一列白色像素的個數
    for x in range(w):
        for y in range(h):
            if image[y, x] == 255:
                w_[x] += 1

    # 繪製垂直平投影圖像
    for x in range(w):
        for y in range(h - w_[x], h):
            vProjection[y, x] = 255

    # cv2.imshow('vProjection',vProjection)

    return w_


def splitAlphabet(projectImg, oriImg, resultImg):
    position = []
    W = getVProjection(projectImg)
    H_Start = 0
    H_End = np.size(projectImg, 0)
    Wstart = 0
    Wend = 0
    W_Start = 0
    W_End = 0
    for j in range(len(W)):
        if W[j] > 0 and Wstart == 0:
            W_Start = j
            Wstart = 1
            Wend = 0
        if W[j] <= 0 and Wstart == 1:
            W_End = j
            Wstart = 0
            Wend = 1
        if Wend == 1:
            position.append([W_Start, H_Start, W_End, H_End])
            Wend = 0
    splitImg = []
    splitImgW = 40  # 切割後固定每張圖的寬度
    for m in range(len(position)):
        if oriImg is not None:
            cv2.rectangle(oriImg, (position[m][0], position[m][1]), (position[m][2], position[m][3]), (0, 255, 255),
                          1)
        tmpH = position[m][3] - position[m][1]
        tmpW = position[m][2] - position[m][0]
        tmpImg = resultImg[position[m][1]:position[m][1] + tmpH, position[m][0]:position[m][0] + tmpW]
        tmpW = tmpImg.shape[1]
        paddingW = int(splitImgW / 2 - tmpW / 2)
        # 切割後等寬
        if tmpW < splitImgW:
            if tmpW % 2 > 0:
                tmpImg = cv2.copyMakeBorder(tmpImg, 0, 0, paddingW + 1, paddingW, cv2.BORDER_CONSTANT,
                                            value=[255, 255, 255])
            else:
                tmpImg = cv2.copyMakeBorder(tmpImg, 0, 0, paddingW, paddingW, cv2.BORDER_CONSTANT,
                                            value=[255, 255, 255])
        splitImg.append(tmpImg)
    return splitImg


def findPaths(directory):
    # directory = r'/Users/moriakiraakira/Desktop/OCR_Sample/cathayOCR/Source'
    filePaths = []
    for entry in os.scandir(directory):
        if (entry.path.endswith(".jpg")
            or entry.path.endswith(".png")) and entry.is_file():
            filePaths.append(entry.path)
    return filePaths


def processImg(oriImg, resize_num, threshold, erodeIterationTimes, dilateIterationTimes,
               medianBlurKernel, isRevert):
    isShowImg = False

    oriImg = cv2.copyMakeBorder(oriImg, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    # resize
    oriImg = cv2.resize(oriImg,
                        (oriImg.shape[1] * int(resize_num), oriImg.shape[0] * int(resize_num)),
                        interpolation=cv2.INTER_CUBIC)

    # gray
    grayImg = cv2.cvtColor(oriImg, cv2.COLOR_BGR2GRAY)

    # sharpen
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    sharpenImg = cv2.filter2D(grayImg, -1, kernel=kernel)

    # binary
    retval, binImg = cv2.threshold(sharpenImg, threshold, 255, cv2.THRESH_BINARY_INV)

    # erode
    erodeImg = cv2.erode(binImg, (5, 5), iterations=erodeIterationTimes)

    # dilate
    dilateImg = cv2.dilate(erodeImg, (5, 5), iterations=dilateIterationTimes)

    # medianBlur
    medianBImg = cv2.medianBlur(dilateImg, medianBlurKernel)

    # 反相
    if isRevert:
        resultImg = 255 - medianBImg
    else:
        resultImg = medianBImg

    # 分割
    splitImgs = splitAlphabet(projectImg=medianBImg, oriImg=oriImg, resultImg=resultImg)

    return splitImgs


# best[3,150,3,3,7]
def split_image(filePath, resize_num=3, threshold=150, erodeIterationTimes=3, dilateIterationTimes=3,
              medianBlurKernel=7, isRevert=True):
    oriImg = cv2.imread(filePath)
    splitImgs = processImg(oriImg, resize_num, threshold, erodeIterationTimes, dilateIterationTimes, medianBlurKernel,
                           isRevert)

    return splitImgs
