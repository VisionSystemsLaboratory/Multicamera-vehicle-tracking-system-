import numpy as np
import cv2
import matplotlib.pyplot as plt

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

    # fig, ax = plt.subplots()
    # ax.set_xlim([0, 256])
    # for i in range(3):
    #     plt.plot(binEdgesRGB[0:-1, i], histogramRGB[:, i], colors[i])
    # ax.set_title("Color Histogram")
    # ax.set_xlabel("Color value")
    # ax.set_ylabel("Pixel count")
    return histogramRGB


# frame RGB, mask - gray scale (0, 255)
def getHistogramsRGB(frame, mask):
    retval, MaskCv = cv2.connectedComponents(mask)
    # plt.figure(figsize=(13, 6))
    # plt.imshow(MaskCv, cmap='plasma')
    # plt.axis('off')
    # plt.show()
    histsRGB = []
    for idx in range(1, retval):
        maskIdx = np.where(MaskCv == idx, 1, 0)
        histsRGB.append(histogramRGB(frame, maskIdx))
    return histsRGB
        
    
        

img = cv2.imread("shapes.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

imgMask = cv2.imread("shapesMask.png")
imgMask = cv2.cvtColor(imgMask, cv2.COLOR_BGR2RGB)
imgMask = imgMask[:, :, 0]

fig, ax = plt.subplots(1, 2)
ax[0].imshow(img)
ax[1].imshow(imgMask, cmap='gray')

getHistogramsRGB(img, imgMask)

