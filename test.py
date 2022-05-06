import geopy
from geopy.distance import geodesic
from unittest import result
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time
import pandas as pd
from urllib.request import urlopen
import urllib

tiempo = datetime.today().strftime('%Y/%m/%Y%m%d')
web = "http://www.sismologia.cl/sismicidad/catalogo/"
ext = ".html"
resultado = web + tiempo + ext
# page = urlopen("http://www.sismologia.cl/sismicidad/catalogo/2022/05/20220505.html")
# soup =  BeautifulSoup(web, "html.parser")
# e = urllib.request.urlopen(f"{web}{tiempo}.html").read()
e = urllib.request.urlopen(resultado).read()
soup = BeautifulSoup(e, 'html.parser')



      # Obtenemos la tabla

tabla_sismos = soup.find('table', attrs={'class':'sismologia detalle'})

# Obtenemos todas las filass
rows = tabla_sismos.find_all('tr')

# output_data = []
# for row in rows:
#     cells = row.find_all('th')
#     output_dat = []
#     if len(cells) > 0:
#         for cell in cells:
#             output_data.append(cell.text)
#             output_data.append(output_dat)

# dataset = pd.DataFrame(output_data)

delimiter = ","                          # unambiguous string
for line_break in soup.findAll('br'):       # loop through line break tags
    line_break.replaceWith(delimiter)       # replace br tags with delimiter
strings = soup.get_text().split(delimiter)  # get list of strings

output_rows = []
for row in rows:
        # obtenemos todas las columns
    cells = row.find_all("td")
    output_row = []
    if len(cells) > 0:
        for cell in cells:
            output_row.append(cell.get_text())
            output_rows.append(output_row)

dataset = pd.DataFrame(output_rows).drop_duplicates()


dataset.columns = [
        "Fecha Local / Lugar",
        "Fecha UTC",
        "Latitud / Longitud",
        "Profundidad",
        "Magnitud (2)",
    ]

# dataset[["Fecha Local / Lugar"]] = dataset[["Fecha Local / Lugar"]].astype(str)

# dataset["Fecha Local / Lugar"].str.replace(" ","", 1)


dataset[["Fecha Local", "Lugar"]] = dataset["Fecha Local / Lugar"].str.split(r",", expand=True)

dataset[["Latitud", "Longitud"]] = dataset["Latitud / Longitud"].str.split(r",", expand=True).apply(pd.to_numeric)

# dataset[["Latitud", "Longitud"]] = dataset[["Latitud", "Longitud"]].apply(pd.to_numeric)

dataset_filter = dataset[
            (-27.100 <= dataset["Latitud"])
            & (dataset["Latitud"] <= -21.680)
            & (-72.150 <= dataset["Longitud"])
            & (dataset["Longitud"] <= -66.180)
            ]

dataset_filter = dataset_filter.reindex(columns=['Fecha Local','Fecha UTC','Latitud','Longitud','Profundidad','Magnitud (2)','Lugar'])

tranque = (-24.39,-69.14)

latitud1 = dataset_filter['Latitud'].agg(lambda x: x.value_counts().index[0])
longitud1 = dataset_filter['Longitud'].agg(lambda x: x.value_counts().index[0])
profundidad = dataset_filter['Profundidad'].agg(lambda x: x.value_counts().index[0])
magnitud = dataset_filter['Magnitud (2)'].agg(lambda x: x.value_counts().index[0])
magnitud2 = magnitud
magnitud3 = float(magnitud2[0])
magnitud4 = magnitud2[1]
delhi = (latitud1, longitud1)
distancia = int(round((geodesic(tranque, delhi).km)))

print (magnitud3)
print (distancia)
print (latitud1)


def bot_send_text(bot_message):
    
    bot_token = '5231406261:AAE1lr7A9feeiv9Ejt3awEyigwzpxtyoqRo'  #'5242107370:AAGiBaDihZbdphDhybneHT0pU_4bJGDVWkk' <mel
    bot_chatID = '-796627951'     #-713984361' <mel
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def sismo_scraping():  
    string="A ocurrido un sismo en las cercanías del Tranque Laguna Seca" "\n""\n" "*Datos del sismo:*" "\n" #titulo con salto de linea
    
    for column in dataset_filter.head(1).columns:
        string += column +  " : " + str(dataset_filter[column].values[0]) + "\n"
          
    return string

def distancias():       
    string2="El sismo se registro a una *DISTANCIA* de  "  f'{str(distancia)}' "Km del Tranque Laguna seca, y una *MAGNITUD* de " f'{str(magnitud3)}' "" f'{str(magnitud4)}'
    return string2

# def amarillo():
#     msg1 = 5
#     dist = 15
#     # msg3 = "NO Aplica para activar protocolo"
#     if msg1 <= 7 or dist <= 100:
#         msg = "Alerta *MORADA*"
#         print("Alerta *MORADA*")
#     elif msg1 <= 7 or dist <= 120:
#         msg = "Alerta *ROJA*"
#         print("Alerta *ROJA*")
#     elif msg1 >=4 or dist <= 10:
#         msg = "Alerta *NARANJA*"
#         print("Alerta *NARANJA*")
#     elif msg1 <=5 or dist <= 50:
#         msg = "Alerta *NARANJA*"
#         print("Alerta *NARANJA*")
#     elif msg1 <=6 or dist <= 120:
#         msg = "Alerta *NARANJA*"
#         print("Alerta *NARANJA*")
#     elif msg1 <= 3.9:
#         msg = "Alerta *AMARILLA*"
#         print("Alerta *AMARILLA*")
#     else:
#         msg = "NO APLICA PARA ACTIVAR PROTOCOLO"
#         print ("NO APLICA PARA ACTIVAR PROTOCOLO")
#     return msg


        
def main():
    ultimo_sismo = None
    # text3 = f'{amarillo()}'
    while True:
        text = f'{sismo_scraping()}'
        text2 = f'{distancias()}'
        if text != ultimo_sismo:
            bot_send_text(text)
            ultimo_sismo = text
            bot_send_text(text2)
            # bot_send_text(text3)
        time.sleep(5) 

if __name__ == '__main__':

    main()
