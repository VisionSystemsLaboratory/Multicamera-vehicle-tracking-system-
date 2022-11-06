import numpy as np
import cv2
import matplotlib.pyplot as plt

def histogramRGB(image, mask):
    objImg = image * mask
    histogramRGB = np.zeros((256, 3))
    binEdgesRGB = np.zeros((257, 3))
    
    background = np.count_nonzero(mask[:, :, 0]==0)
    colors = ("red", "green", "blue")

    for channel_id, color in enumerate(colors):
        histogram, binEdges = np.histogram(
            objImg[:, :, channel_id], bins=256, range=(0, 256)
        )
        histogram[0] -= background
        histogramRGB[:, channel_id] = histogram
        binEdgesRGB[:, channel_id] = binEdges

    fig, ax = plt.subplots()
    ax.set_xlim([0, 256])
    for i in range(3):
        plt.plot(binEdgesRGB[0:-1, i], histogramRGB[:, i], colors[i])
    ax.set_title("Color Histogram")
    ax.set_xlabel("Color value")
    ax.set_ylabel("Pixel count")



img = cv2.imread("resorak.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
tempMask = np.zeros_like(img)
tempMask[250:550, :] = 1

# plt.figure()
# plt.imshow(img)
histogramRGB(img, tempMask)
