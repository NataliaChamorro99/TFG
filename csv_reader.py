import csv
import numpy

# Abrir el archivo CSV en modo lectura
ECG_csv = 'ECG1.csv'

Ecg_uV = []

with open(ECG_csv, 'r', newline='', encoding='utf-8') as archivo:
    csv_reader = csv.reader(archivo, delimiter=';')
    for fila in csv_reader:
        Ecg_uV.append(int(fila[0]))


for fila in Ecg_uV:
    print(fila)

#Convertir a 10 bit
valorMaxV= 2000
rango_original = (0,valorMaxV)
rango_objetivo = (0, 1024)
ECG_Bit= numpy.round(numpy.interp(Ecg_uV,rango_original,rango_objetivo)).astype(int)
print(ECG_Bit)

