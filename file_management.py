#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import pandas as pd
import csv
import numpy as np

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
        print(filename)
        with open(f"Hists\\{filename}", newline='') as f:
            reader = pd.read_csv(f)
            yield reader.values


def assign_object_id(target, histbase):
    # target - current processed histogram
    """
    Druga która przyjmuje histogramy z programu, historam obecnie przetwarzany,
     nadany numer pojazdu - porównuje który histogram jest najbardziej podobny. - zwroci który to jest obiekt

    Identyfikuje, sprawdza czy jest w bazie jak nie ma to dodaje do bazy
<<<<<<< HEAD
     i w pliku do wysłania bo jak już jest to nic nie rób.
     """

    """porównuje z bazą i mówi jaki to rodzaj, nadaje numer id, id w formacie kolor_numer,
     trzymać w pamięci te, które są na obrazie żeby nie nadawać im różnych numerów"""

    best_norm = np.inf
    object_id = np.NaN

    for i, histogram in enumerate(histbase):
        norm = np.linalg.norm(histogram - target)

        if norm < best_norm:
            object_id = i

    return object_id


with open("Hists\\target.csv", newline='') as f:
    car = pd.read_csv(f).values

hbase = list(load_hists())
assign_object_id(car, hbase)



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
            
assign_object_id()
# clear_to_send()