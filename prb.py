import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import time 
from hist import histogramRGB


def get_band_img(mask, frame, lst_bound):
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
    
    print(f'punkty: {boundRect}')
    print()
    for i in range(len(contours)):
        x1 = int(boundRect[i][0])
        y1 = int(boundRect[i][1])
        x2 = int(boundRect[i][0]+boundRect[i][2])
        y2 = int(boundRect[i][1]+boundRect[i][3])
        color = (0, 0 ,255)
        img_bound = frame[y1 + 10 : y2 + 10, x1 + 10 : x2 + 10, :]
        print(f'Wymiary baudbox: {img_bound.shape}')
        if img_bound.shape[0] > 140 and img_bound.shape[1] > 150:
            lst_bound.append(img_bound)
            cv.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
    cv.imshow('Contours', frame)


def draw_countur(mask, frame):
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
    
    for i in range(len(contours)):
        color = (0, 0 ,255)
        cv.rectangle(frame, (int(boundRect[i][0]), int(boundRect[i][1])), \
          (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
     
# KK 07.11.-----------------------------------------------------------------
            
        x1 = int(boundRect[i][0])
        y1 = int(boundRect[i][1])
        frame = cv.putText(frame, str(i), (x1,y1), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 5, cv.LINE_AA)
    # cv.imwrite('frame1.png', frame)


# -----------------------------------------------------------------------------    

    cv.imshow('Contours', frame)


def main():
    #cap = cv.VideoCapture("sample1.mp4")
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    else:
        lst_bound = []
        flag_pred = False
        lst_imgs = []
        size = (1200, 720)
        ret, frame = cap.read()
        if not ret:                                                     # Sprawdzania czy odczytano ramkę obrazu poprawnie, jeżeli tak to ret == True
            print("Can't receive frame (stream end?). Exiting ...")
        else:
            base =cv.resize(frame,size)
            gray_base = cv.cvtColor(base, cv.COLOR_BGR2GRAY)

            while True:
                ret, frame = cap.read()
                if not ret:                                                     # Sprawdzania czy odczytano ramkę obrazu poprawnie, jeżeli tak to ret == True
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                
                frame =cv.resize(frame, size)
                gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

                diff = cv.subtract(gray_frame, gray_base)
                threshold = 45
                binary = np.uint8(diff > threshold) * 255

                kernel = np.ones((5, 5), np.uint8)
                dilated = cv.dilate(binary, kernel, iterations=3)
                eroded = cv.erode(dilated, kernel, iterations=5)
                SAD_classificator = np.sum(eroded) /(size[0]*size[1])
                # print(f'SAD value: {SAD_classificator}')
                if SAD_classificator > 27 and not flag_pred:
                    print("Dokonaj predykcji")
                    get_band_img(eroded, frame, lst_bound)
                    flag_pred = True
                # cv.imshow('BINARY', eroded)
                # cv.imshow('my',eroded)
                draw_countur(eroded, frame)
                if cv.waitKey(1) == ord('q'):
                    break
                time.sleep(0.03)

        cv.waitKey(0)
        cv.destroyAllWindows()


    print(len(lst_bound))
    for i in range(len(lst_bound)):
        plt.figure()
        plt.imshow(lst_bound[i])
        plt.show()
        histogramRGB(lst_bound[i])
main()
