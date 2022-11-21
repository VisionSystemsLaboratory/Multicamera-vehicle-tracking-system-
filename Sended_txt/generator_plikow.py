for i in range(7, 200):
	file_csv = open("PD_"+str(i)+".csv", "w")
	file_csv.write("Plik z RPI "+ str(i))
	file_csv.close()  
