# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:55:26 2022

@author: kxkfg2
"""

import os
import random
import csv
import numpy as np
from file_management import generate_random_histogram, load_hists, assign_object_id

def tosend(car_id, car_type):
    file_csv = open("Sended_txt/PD_"+str(car_id)+".csv", 'w')
    csv.writer(file_csv).writerow([car_id, car_type])
    file_csv.close()
    # file_csv = open("Sended_txt/PD_"+str(car_id)+".csv", 'r')
def clear_to_send(car_id):
    if os.path.exists("Sended_txt/PD_"+str(car_id)+".csv"):
        os.remove("Sended_txt/PD_"+str(car_id)+".csv")
            
tosend(5, "czerwony")
# clear_to_send(5)