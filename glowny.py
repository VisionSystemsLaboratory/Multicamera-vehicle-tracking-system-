import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import time
import copy as cp
from hist import getHistogramsRGB, getRGBHistograms
from file_management import assign_object_id, load_hists, updateReceivedBase, updateSendedBaseAndGetCarIds

def draw_countur(mask, frame):
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) # znajdowanie konturów

    contours_poly = [None]*len(contours)                  # Lista do przechowywania konturów wygładzonych
    boundRect = [None]*len(contours)                      # Lista do przechowywania bounding boxów
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)    # Aproksymacja wielomianowa w celu wygładzenia konturów
        boundRect[i] = cv.boundingRect(contours_poly[i])  # Tworzenie Bounding boxów
    
    for i in range(len(contours)):                        # Dodanie do Ramki obrazu bounding boxów
        color = (0, 0 ,255)
        cv.rectangle(frame, (int(boundRect[i][0]), int(boundRect[i][1])), \
          (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
          
    cv.imshow('Sledzone obiekty', frame)                  # Wyświetlanie na ekran przetworzonego obraz

def main():
    
    cap = cv.VideoCapture(0)                                        # Pobieranie obrazu z pliku bądź kamery
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    else:                                                       
        size = (720, 360)                                                      # Wymiar ramki przetwarzanego obrazu
        size_for_hist = (120, 100)          
        ret, frame = cap.read()                                                 # Pobieranie ramki obrazu
        if not ret:                                                             # Sprawdzania czy odczytano ramkę obrazu poprawnie, jeżeli tak to ret == True
            print("Can't receive frame (stream end?). Exiting ...")
        else:
            histBase = load_hists()                                             # Baza samochodow defaultowa
            sendedBase = []                                                     # baza wykrytych pojazdów [(kolor, id), (...)]
            receivedBase = []                                                   # baza pojazdów wykrytych przez drugą kamerę [(j.w)]
            # Pobieranie ramki z tłem                                  
            base =cv.resize(frame, size)                                         # Tło o zminionym rozmiarze
            gray_base = cv.cvtColor(base, cv.COLOR_BGR2GRAY)                    # Konwersja do barw odcieni szarości

            hist_base = cv.resize(cp.copy(base), size_for_hist)
            hist_base_gray = cv.cvtColor(hist_frame, cv.COLOR_BGR2GRAY)

# --------------- Główna pętla programu ---------------------------------------
            while True:
                # Pobieranie obecnie przetwarzanej ramki obrazu
                ret, frame = cap.read()
                if not ret:                                                     # Sprawdzania czy odczytano ramkę obrazu poprawnie, jeżeli tak to ret == True
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                # Zmiana rozmiaru ramki obrazu oraz konwersja to barw w skali szarości         
                frame =cv.resize(frame, size)                                   
                gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

                hist_frame = cv.resize(cp.copy(frame), size_for_hist)
                hist_gray = cv.cvtColor(hist_frame, cv.COLOR_BGR2GRAY)

                # Różnica obrazu obecnie przetwarzanego z tłem oraz binaryzacja
                # diff = cv.subtract(gray_frame, gray_base)
                threshold = 110
                binary = np.uint8(gray_frame < threshold) * 255
                hist_binary = np.uint8(hist_gray < threshold) * 255

                # Operacje morfologiczne - dylatacja i erozja
                kernel = np.ones((5, 5), np.uint8)

                dilated_mask = cv.dilate(binary, kernel, iterations=5)
                mask = cv.erode(dilated_mask, kernel, iterations=5)

                hist_dilated_mask = cv.dilate(hist_binary, kernel, iterations=5)
                hist_mask = cv.erode(hist_dilated_mask, kernel, iterations=5)

                # Klasyfikator do wykrywania obiektu pojawiającego się na obrazie
                SAD_classificator = np.sum(mask) / (size[0]*size[1])

                # Wyświetlanie wartości klasyfikatora aby dobrać odpowiedni próg:
                # print(f'SAD value: {SAD_classificator}')

                # Decyzja o momencie wyliczania histogramów - czyli obiekt pojawił się na obrazie - decyduje o tym SAD
                if SAD_classificator > 20:
                    """
                    # 1. Indeksowanie maski binarnej.
                    maskIdx = ...
                    # 2. Wyliczenie wszystkich histogramów oraz indeksów im odpowiadających (z indeksowania).
                    histsRGB, histsRGBIdx = ...
                    # 3. Sprawdzenie czy dany histogram znajduje się w bazie.
                    for i, histRGB in enumerate(histsRGB):
                      # 3.1. zwrócenie nazwy pliku z bazy (np. czerwony dla pliku czerwony.csv).
                      # 3.2. sprawdzenie czy samochód istnieje w bazie znalezionych pojazdów.
                      # 3.3. jeśli nie ma go w bazie to go zapisać kolor.txt/csv w środku ID albo kolor_ID.txt.
                      # 3.4. tu można powiązać numer ID z histsRGBIdx żeby można było wyświetlić ID w bounding box'ie.
                           czyli np. appendować jakąś listę: tuple(histsRGBIdx[i], Id) albo od razu zrobić # 4 jak można
                    # 4. wyświetlenie numerów ID w bounding boxach.
                    """
                    updateReceivedBase(receivedBase)
                    nrOfComponents, maskId = cv.connectedComponents(hist_mask)
                    histogramsRGB, histogramsIdx = getHistogramsRGB(hist_frame, nrOfComponents, maskId)
                    colorsOfDetectedCars = assign_object_id(histogramsRGB, histBase)
                    carIdx = updateSendedBaseAndGetCarIds(colorsOfDetectedCars, sendedBase, receivedBase)
                    #TODO przypisanie id do ramek (
                    #   histogramsIdx - ids z maski z indeksowania)
                    #   carIdx - faktyczne indeksy
                    #   wyszukac w maskId pokolei histogramsIdx i odpowiednio wypisac na obrazie carIdx
                    #   albo mozna liczyc srodek ciezkosci albo pierwszy napotkany

                # Próbne wyświetlanie obrazu:
                # cv.imshow('BINARY', mask)

                # Rysowanie boundingboxów na obrazie:
                draw_countur(mask, frame)

                # Zakończenie działania programu:
                if cv.waitKey(1) == ord('q'):
                    break

                # Do odczytywania video z pliku, jeśli z kamery to zakomentować linijkę poniżej
                time.sleep(0.03)

# --------------- Koniec głównej pętli programu -------------------------------

        # Niszczenie okien do wyświetlania obrazu oraz jego pobierania
        cv.waitKey(0)
        cv.destroyAllWindows()

main()