import time
import board
import busio
import digitalio
import numpy
import csv
import neurokit2

SCK = board.SCK
MOSI = board.MOSI
CS = board.D5 

cs = digitalio.DigitalInOut(CS)
Ecg_uV = []

spi = busio.SPI(SCK, MOSI)

def read_cs(csvFile):
    with open(csvFile, 'r', newline='', encoding='utf-8') as archivo:
        csv_reader = csv.reader(archivo, delimiter=';')
        for fila in csv_reader:
            Ecg_uV.append(int(fila[0]))

def convert_to_10(valorMaxV,Ecg_uV):
    #Convertir a 10 bit
    rango_original = (0,valorMaxV)
    rango_objetivo = (0, 1024)
    ECG_Bit= numpy.round(numpy.interp(Ecg_uV,rango_original,rango_objetivo)).astype(int)
    return ECG_Bit

x=0

ECG_csv = 'ECG1.csv'
read_cs(ECG_csv)
ECG_Bit = convert_to_10(1000,Ecg_uV)

def setOutput(value):
    # Ajusta los bits de control y datos segun el MCP4911
    highByte =(value>>6 & 0b1111)|0b00110000  # Puedes ajustar esto para configurar el canal y la ganancia
    lowByte = (value<<2 & 0b11111100)
    datos_a_enviar = bytearray([highByte,lowByte])
    return datos_a_enviar

ecgsim = neurokit2.ecg_simulate(duration=10,noise= 0, heart_rate=50)
amplitud =  max(ecgsim) - min(ecgsim)
offset = min(ecgsim)
#print(min(ecgsim))
#print(max(ecgsim))
#while x<0x0ffffffffffff:
while x<len(ecgsim):
    #value = ECG_Bit[(x%len(ECG_Bit))]
    value = int(((ecgsim[x]-offset)*1023)/amplitud)
    spi.write(setOutput(value))
    #spi.write(setOutput((x%2)*1023))

    print(value)
    #print(bin(setOutput(value)[0]))
    #print(bin(setOutput(value)[1]))
    
    x=x+1
    time.sleep(0.001)