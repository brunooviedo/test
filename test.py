import geopy
from geopy.distance import geodesic
from unittest import result
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import urllib.request
import pandas as pd

tiempo = datetime.today().strftime('%Y/%m/%Y%m%d')

e = urllib.request.urlopen(f"http://www.sismologia.cl/sismicidad/catalogo/{tiempo}.html").read()
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

dataset[["Latitud", "Longitud"]] = dataset["Latitud / Longitud"].str.split(r",", expand=True)

dataset[["Latitud", "Longitud"]] = dataset[["Latitud", "Longitud"]].apply(pd.to_numeric)

dataset_filter = dataset[
            (-27.100 <= dataset["Latitud"])
            & (dataset["Latitud"] <= -21.680)
            & (-72.150 <= dataset["Longitud"])
            & (dataset["Longitud"] <= -66.180)
            ]



tranque = (-24.39,-69.14)

latitud1 = dataset_filter['Latitud'].values[0]
longitud1 = dataset_filter['Longitud'].values[0]
profundidad = dataset_filter['Profundidad'].values[0]
magnitud = dataset_filter['Magnitud (2)'].values[0]
magnitud2 = magnitud.split(' ')
magnitud3 = float(magnitud2[0])
magnitud4 = magnitud2[1]
delhi = (latitud1, longitud1)
distancia = int(round((geodesic(tranque, delhi).km)))

print (magnitud3)
print (distancia)

# dataset.to_excel("test.xlsx")
# dataset[["Fecha Local", "Lugar"]] = dataset["Fecha Local / Lugar"].str.replace(" ","", 1)

dataset_filter.to_excel("test.xlsx")

# dataset[["Latitud", "Longitud"]] = dataset[["Latitud", "Longitud"]].apply(pd.to_numeric)
# dataset_filter = dataset[
#             (-27.100 <= dataset["Latitud"])
#             & (dataset["Latitud"] <= -21.680)
#             & (-72.150 <= dataset["Longitud"])
#             & (dataset["Longitud"] <= -66.180)
#             ]

print (dataset_filter)
