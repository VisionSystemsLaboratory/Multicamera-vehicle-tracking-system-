#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import random
import csv

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
            yield histogram


hist1, hist2, hist3 = tuple(load_hists())
print(hist1)
print(hist2)
print(hist3)


def assign_object_id(target):
    # target - current processed histogram
    """Druga która przyjmuje histogramy z programu, historam obecnie przetwarzany,
     nadany numer pojazdu - porównuje który histogram jest najbardziej podobny. - zwroci który to jest obiekt

    Identyfikuje, sprawdza czy jest w bazie jak nie ma to dodaje do bazy
     i w pliku do wysłania bo jak już jest to nic nie rób.  """


    # Tu chyba nie do końca ogarniam o jakie bazy chodzi, jest jedna z rodzajem samochodu/kolorem. Ale OCB z tą drugą,
    # która identyfikuje obiekt jako taki. Jak ma być przetwarzana????
    pass