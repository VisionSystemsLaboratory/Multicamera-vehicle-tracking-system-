#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import csv
import numpy as np

def generate_random_histogram():
    data = ""
    for i in range(255):
            random_num = random.randint(0, 255)
            numtext = str(random_num)
            data += numtext + ","

    with open("Hists/db3.csv", 'w') as file:
        file.write(data)

def load_hists():
    """Jedna funkcja, która z csv wczytuje histogramy z bazy - zmienne globalne? """
    # to jest jakby rodzaj pojazdu, jego bazowy kolor?

    filenames = os.listdir("Hists")

    for filename in filenames:
        with open(f"Hists\\{filename}", newline='') as f:
            reader = csv.reader(f)
            histogram = list(reader)[0]
            histogram = [int(x) for x in histogram[:-1]]
            yield histogram


# =============================================================================
# hist1, hist2, hist3 = tuple(load_hists())
# print(hist1)
# print(hist2)
# print(hist3)
# =============================================================================


def assign_object_id(target=0):
    # target - current processed histogram
    """Druga która przyjmuje histogramy z programu, historam obecnie przetwarzany,
     nadany numer pojazdu - porównuje który histogram jest najbardziej podobny. - zwroci który to jest obiekt

    Identyfikuje, sprawdza czy jest w bazie jak nie ma to dodaje do bazy
     i w pliku do wysłania bo jak już jest to nic nie rób.  """
     
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
    pass
    

def clear_to_send():
    if os.path.exists("ToSend/tosend.txt"):
        with open("ToSend/tosend.txt", 'w') as file:
            file.close()
            
assign_object_id()
# clear_to_send()