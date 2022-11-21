#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import pandas as pd
import numpy as np
import difflib


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
            yield reader

def assign_object_id(target, histbase):
    # target - current processed histogram
    """
    Druga która przyjmuje histogramy z programu, historam obecnie przetwarzany,
     nadany numer pojazdu - porównuje który histogram jest najbardziej podobny. - zwroci który to jest obiekt

    Identyfikuje, sprawdza czy jest w bazie jak nie ma to dodaje do bazy
     i w pliku do wysłania bo jak już jest to nic nie rób.
     """

    """porównuje z bazą i mówi jaki to rodzaj, nadaje numer id, id w formacie kolor_numer,
     trzymać w pamięci te, które są na obrazie żeby nie nadawać im różnych numerów"""

    target = pd.DataFrame(target)

    for histogram in histbase:
        label = histogram.iloc[0]
        histogram = histogram
        similarity = np.linalg.norm(histogram - target)

        if similarity > 0.7: # spróbować dodać próg
            return label
            pass
    pass

hist_base = tuple(load_hists())
print(hist_base)
car = np.zeros((256, 3))
# assign_object_id(car, hist_base)