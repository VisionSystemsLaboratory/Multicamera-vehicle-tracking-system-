import cv2 as cv
import numpy as np
import copy as cp
from hist import getHistogramsRGB
from file_management import save_hist_to_mem, update_hist_base

color = "red"  # red/green/blue

def main():

    # Pobieranie obrazu z pliku bądź kamery
    cap = cv.VideoCapture("video_samples/pracownia3.avi")
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    else:                                                       
        size_for_hist = (120, 100)
        ret, frame = cap.read()                                                 # Pobieranie ramki obrazu
        if not ret:                                                             # Sprawdzania czy odczytano ramkę obrazu poprawnie, jeżeli tak to ret == True
            print("Can't receive frame (stream end?). Exiting ...")
        else:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")

            hist_frame = cv.resize(cp.copy(frame), size_for_hist)
            hist_gray = cv.cvtColor(hist_frame, cv.COLOR_BGR2GRAY)

            threshold = 100
            hist_binary = np.uint8(hist_gray < threshold) * 255

            kernel = np.ones((5, 5), np.uint8)

            hist_dilated_mask = cv.dilate(hist_binary, kernel, iterations=5)
            hist_mask = cv.erode(hist_dilated_mask, kernel, iterations=5)

            nrOfComponents, maskId = cv.connectedComponents(hist_mask)
            histogramsRGB, histogramsIdx = getHistogramsRGB(hist_frame, nrOfComponents, maskId)

            save_hist_to_mem(histogramsRGB, color)

        cv.waitKey(0)
        cv.destroyAllWindows()
        update_hist_base(color)


main()
