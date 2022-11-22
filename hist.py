import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd

def histogramRGB(image, mask):
    maskRGB = np.stack((mask, mask, mask), axis=2)
    objImg = image * maskRGB
    histogramRGB = np.zeros((256, 3))
    binEdgesRGB = np.zeros((257, 3))
    
    background = np.count_nonzero(mask==0)
    colors = ("red", "green", "blue")

    for channel_id, color in enumerate(colors):
        histogram, binEdges = np.histogram(
            objImg[:, :, channel_id], bins=256, range=(0, 256)
        )
        histogram[0] -= background
        histogramRGB[:, channel_id] = histogram
        binEdgesRGB[:, channel_id] = binEdges

    return histogramRGB


# frame RGB, mask - gray scale (0, 255)
def getHistogramsRGB(frame, mask):
    nrOfComponents, maskId = cv2.connectedComponents(mask)
    invalidIds = set().union([0], maskId[:, 0], maskId[:, -1], maskId[0, :], maskId[-1, :])
    histsRGB = np.zeros((nrOfComponents, 256, 3))
    for idx in range(nrOfComponents):
        maskIdx = np.where(maskId == idx, 1, 0)
        histsRGB[idx] = (histogramRGB(frame, maskIdx))
    return np.delete(histsRGB, list(invalidIds), axis=0)
        

def getRGBHistograms(frame, mask):
    nrOfComponents, maskId = cv2.connectedComponents(mask)
    temp = np.where(maskId == 0, 0, 255)
    invalidIds = set().union([0], maskId[:, 0], maskId[:, -1], maskId[0, :], maskId[-1, :])
    
    histogramsRGB = np.zeros((nrOfComponents, 256, 3))
    
    redLyr = 0
    greenLyr = 1
    blueLyr = 2
    
    for coord, objectIdx in np.ndenumerate(maskId):
        i, j = coord

        histogramsRGB[objectIdx, frame[i, j, redLyr], redLyr] += 1
        histogramsRGB[objectIdx, frame[i, j, greenLyr], greenLyr] += 1
        histogramsRGB[objectIdx, frame[i, j, blueLyr], blueLyr] += 1
                
    return np.delete(histogramsRGB, list(invalidIds), axis=0)
    
    
def hist_to_csv(frame, mask):
    histsRGB = getRGBHistograms(frame, mask)
    for i, histRGB in enumerate(histsRGB):
        pd.DataFrame(histRGB).to_csv(f"Hists/auto_{i}.csv")
    
<<<<<<< HEAD
# img = cv2.imread("shapes.png")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
# imgMask = cv2.imread("shapesMask.png")
# imgMask = cv2.cvtColor(imgMask, cv2.COLOR_BGR2RGB)
# imgMask = imgMask[:, :, 0]
#
# fig, ax = plt.subplots(1, 2)
# ax[0].imshow(img)
# ax[1].imshow(imgMask, cmap='gray')
#
# histA = getHistogramsRGB(img, imgMask)
# histB = fastHistogramsRGB(img, imgMask)
# histC = fastHistogramsRGB2(img, imgMask)
# print(np.all(histA == histB))
# print(histA)
=======
>>>>>>> 42308ee0e1bf53e26da08f7cae48e096d2f0fda2
# frame = cv2.imread("img.jpg")
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
#
# threshold = 110
# binary = np.uint8(gray_frame < threshold) * 255
# kernel = np.ones((5, 5), np.uint8)
# dilated_mask = cv2.dilate(binary, kernel, iterations=5)
# mask = cv2.erode(dilated_mask, kernel, iterations=5)
# plt.figure()
# plt.imshow(binary)
# hist_to_csv(frame, mask)
