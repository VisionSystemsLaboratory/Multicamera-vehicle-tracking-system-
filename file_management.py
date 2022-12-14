#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import pandas as pd
import csv
import numpy as np
import cv2
import matplotlib.pyplot as plt


def generate_random_histogram():
    data = ""
    for i in range(255):
        random_num = random.randint(0, 100)
        numtext = str(random_num)
        data += f"{numtext}, {numtext}, {numtext} \n"

    with open("Hists/db3.csv", 'w') as file:
        file.write(data)


def load_hists():
    # histogram 3 kolumny R, G, B
    # format pliku CSV
    """Jedna funkcja, która z csv wczytuje histogramy z bazy - zmienne globalne?"""

    filenames = os.listdir("Hists")
    for filename in filenames:
        with open(f"Hists\\{filename}", newline='') as f:
            reader = pd.read_csv(f).values
            yield reader[:, 1:4]


def assign_object_id(targets, histbase):
    """

    :param targets: list[np.array] - histograms of image objects
    size of np.array must be (255, 3)
    :param histbase: list[np.array] - base of histograms to compare with
    size of np.array must be (255, 3)
    :return:
    Color of found object
    """
    # target - current processed histogram
    # todo :
    color_description = {0: "Czerwony", 1: "Niebieski",
                         2: "Zielony", np.NaN: "Niezidentyfikowany"}

    best_norm = 0
    car_id = np.NaN
    car_ids = []
    threshold = np.inf  # miara dopasowania

    for target in targets:
        for idx, histogram in enumerate(histbase):
            # temporary - could be improved by saving normalize histbase
            target = target / np.sum(target)

            # norm = np.linalg.norm(histogram - target)
            score = cv2.compareHist(histogram.astype("float32"), target.astype('float32'), method=cv2.HISTCMP_INTERSECT)

            if score > 0.5:
                if score > best_norm:
                    best_norm = score
                    car_id = idx
            # if norm < best_norm:
            #     best_norm = norm
            #     if best_norm < threshold:
            #         car_id = idx
            #     else:
            #         car_id = np.NaN

        print(f"Best norm is: {best_norm}")
        car_ids.append(color_description[car_id])
        best_norm = np.inf
        car_id = np.NaN

    return car_ids


def Assign_object_id(car, hist_base):
    # i w pliku do wysłania bo jak już jest to nic nie rób.

    # get random histogram for tests
    target = []
    for i in range(255):
        random_num = random.randint(0, 255)
        target.append(random_num)

    # calculate which hist is most similar
    hist1, hist2, hist3 = tuple(load_hists())
    hist_package = [hist1, hist2, hist3]
    best_hist_sum = np.inf
    for n, hist in enumerate(hist_package):
        data_sol = np.zeros_like(target)
        for i in range(len(target)):
            data_sol[i] = np.abs(target[i] - hist[i])
        sum_sol = np.sum(data_sol)
        if sum_sol < best_hist_sum:
            best_hist_sum = sum_sol
            best_hist_Nr = n+1

    print(best_hist_Nr)

    # prepare txt to send
    if not os.path.exists("ToSend/tosend.txt"):
        open("ToSend/tosend.txt", 'w').write('')
    with open("ToSend/tosend.txt", 'r') as file_R:
        list_to_send = list(file_R.read())
    print(list_to_send)
    if str(best_hist_Nr) not in list_to_send:
        with open("ToSend/tosend.txt", 'a') as file_A:
            file_A.write(str(best_hist_Nr))
    print(list(open("ToSend/tosend.txt", 'r').read()))

    # Tu chyba nie do końca ogarniam o jakie bazy chodzi, jest jedna z rodzajem samochodu/kolorem. Ale OCB z tą drugą,
    # która identyfikuje obiekt jako taki. Jak ma być przetwarzana????


def clear_to_send():
    if os.path.exists("ToSend/tosend.txt"):
        with open("ToSend/tosend.txt", 'w') as file:
            file.close()


def updateReceivedBase(base):
    rNr = len(base) + 1
    filePath = "Received_txt/car" + str(rNr) + ".txt"
    if os.path.isfile(filePath):
        with open(filePath) as f:
            data = [line.strip() for line in f.readlines()]
        base.append((data[0], int(data[1])))


def updateSendedBaseAndGetCarIds(detectedColors, sBase, rBase, idFactor=100):
    carIds = []
    checkRBase = len(rBase) > 0
    checksBase = len(sBase) > 0
    if checkRBase:
        rColors, rColorsId = list(zip(*rBase))
    if checksBase:
        sColors, sColorsId = list(zip(*sBase))

    for detectedColor in detectedColors:
        if checkRBase and detectedColor in rColors:
            it = rColors.index(detectedColor)
            carIds.append(rColorsId[it])
        elif checksBase and detectedColor in sColors:
            it = sColors.index(detectedColor)
            carIds.append(sColorsId[it])
        else:
            newId = len(sBase) + 1
            string = detectedColor + "\n" + str(newId)
            text_file = open(f"Sended_txt/car{newId}.txt", "w")
            text_file.write(string)
            text_file.close()
            sBase.append((detectedColor, newId))
            carIds.append(newId)
    return carIds

#   DELETE IT
def load_hist_to_mem(folder):
    filenames = os.listdir(folder)
    for filename in filenames:
        with open(f"{folder}\\{filename}", newline='') as f:
            reader = pd.read_csv(f).values
            yield reader[:, 1:4]


def print_hist(histogram):

    plt.plot(histogram[:, 0], "r")
    plt.plot(histogram[:, 1], "g")
    plt.plot(histogram[:, 2], "b")


def save_hist_to_mem(histsRGB, color):

    x = 0
    for i, histRGB in enumerate(histsRGB):
        path = {"red": "toDelete/red", "green": "toDelete/green", "blue": "toDelete/blue"}
        filenames = os.listdir(path[color])

        if filenames:
            filenames = [int(name[5]) for name in filenames]

        if filenames:
            pd.DataFrame(histRGB).to_csv(f"{path[color]}/auto_{max(filenames) + 1}.csv")
        else:
            pd.DataFrame(histRGB).to_csv(f"{path[color]}/auto_{0}.csv")


def update_hist_base(color):

    path = {"red": "toDelete/red", "green": "toDelete/green", "blue": "toDelete/blue"}
    number_color_encoding = {"red": 0, "green": 1, "blue": 2}
    hists = list(load_hist_to_mem(path[color]))
    num_of_samples = len(hists)

    sum_of_hist = 0
    for hist in hists:
        sum_of_hist += hist

    avg = sum_of_hist / num_of_samples
    pd.DataFrame(avg / np.sum(avg)).to_csv(f"Hists/auto_{number_color_encoding[color]}.csv")


