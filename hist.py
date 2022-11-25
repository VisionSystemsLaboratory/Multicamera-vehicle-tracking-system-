import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd


def histogramRGB(image, mask):
    maskRGB = np.stack((mask, mask, mask), axis=2)
    objImg = image * maskRGB
    histogramRGB = np.zeros((256, 3))
    binEdgesRGB = np.zeros((257, 3))

    background = np.count_nonzero(mask == 0)
    colors = ("red", "green", "blue")

    for channel_id, color in enumerate(colors):
        histogram, binEdges = np.histogram(
            objImg[:, :, channel_id], bins=256, range=(0, 256)
        )
        histogram[0] -= background
        histogramRGB[:, channel_id] = histogram
        binEdgesRGB[:, channel_id] = binEdges

    return histogramRGB


def getHistogramsRGB(frame, nrOfComponents, maskId):
    invalidIds = set().union([0], maskId[:, 0],
                             maskId[:, -1], maskId[0, :], maskId[-1, :])

    histsRGB = np.zeros((nrOfComponents, 256, 3))
    histsIdx = np.arange(nrOfComponents)
    for idx in range(nrOfComponents):
        maskIdx = np.where(maskId == idx, 1, 0)
        histsRGB[idx] = (histogramRGB(frame, maskIdx))
    return np.delete(histsRGB, list(invalidIds), axis=0), np.delete(histsIdx, list(invalidIds), axis=0)


def getRGBHistograms(frame, nrOfComponents, maskId):
    invalidIds = set().union([0], maskId[:, 0],
                             maskId[:, -1], maskId[0, :], maskId[-1, :])

    histogramsRGB = np.zeros((nrOfComponents, 256, 3))
    histsIdx = np.arange(nrOfComponents)

    redLyr = 0
    greenLyr = 1
    blueLyr = 2

    for coord, objectIdx in np.ndenumerate(maskId):
        i, j = coord

        histogramsRGB[objectIdx, frame[i, j, redLyr], redLyr] += 1
        histogramsRGB[objectIdx, frame[i, j, greenLyr], greenLyr] += 1
        histogramsRGB[objectIdx, frame[i, j, blueLyr], blueLyr] += 1

    return np.delete(histogramsRGB, list(invalidIds), axis=0), np.delete(histsIdx, list(invalidIds), axis=0)


def hist_to_csv(frame, mask):
    histsRGB, _ = getRGBHistograms(frame, mask)
    for i, histRGB in enumerate(histsRGB):
        pd.DataFrame(histRGB).to_csv(f"Hists/auto_{i}.csv")


# frame = cv2.imread("img.jpg")
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

# threshold = 110
# binary = np.uint8(gray_frame < threshold) * 255
# kernel = np.ones((5, 5), np.uint8)
# dilated_mask = cv2.dilate(binary, kernel, iterations=5)
# mask = cv2.erode(dilated_mask, kernel, iterations=5)
# plt.figure()
# plt.imshow(binary)
# hist_to_csv(frame, mask)
