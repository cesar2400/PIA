import requests
import json
import matplotlib.pyplot as plt
import statistics
import numpy as np
import os
import sys
from requests.exceptions import ConnectionError


def obtener_produccion_anual(lat, lon, potencia_kw, perdidas, angulo=20, orientacion = 180): # Orientación Sur
    url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc"
    params = {
        "lat": lat,
        "lon": lon,
        "peakpower": potencia_kw,
        "loss": perdidas,
        "angle": angulo,
        "aspect": orientacion,
        "outputformat": "json"
    }

    try:
        response = requests.get(url, params=params)
            
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as e:
                print("Error al procesar JSON:", e)
                return None

    except ConnectionError as e:
        print(f"Error de conexión a Internet: {e}")
        print("Presione enter para continuar un un caso guardado, presione cualquier otra tecla y luego enter si decea obtener la información a utilizar.") 
        sn = input(">>> ")  
        print()
	
        
        if os.path.exists("prueba.json") and sn == "":
            with open("prueba.json", "r") as archivo:
                return json.load(archivo)
                             
        while True:    
            with open("prueba.json", "r") as archivo:
                respuesta = json.load(archivo)
            print(respuesta['outputs'])
            print()               
            print("¿Desea continuar (presione enter para continuar o cualquier otra tecla para volvar a intentar cargar los datos)? ")
            sn = input(">>> ")
            print()
            if sn != "":                       
                return obtener_produccion_anual(lat,lon,potencia_kw,perdidas,angulo,orientacion)
            else:                 
                return respuesta           
                                            
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió otro error con la solicitud: {e}")
        return None
    



"""
lat: Variable de tipo flotante.
lon: Variable de tipo flotante.
angulo: Varible de tipo flotante.
orientación: Variable de tipo flotante.
resultado: 
"""


resultado = obtener_produccion_anual(25.67, -100.31, 3.99, 14)

if not resultado:
    input("No se obtuvieron datos, se detendrá el programa")
    sys.exit()

outputs = resultado['outputs']
outputs_totals = outputs['monthly']['fixed']
produccion_anual = outputs_totals
generacion_mensual = []
for month in outputs_totals:
    generacion_mensual.append(month['E_m'])
#print(generacion_mensual)

generacion_bimestral = [generacion_mensual[i] + generacion_mensual[i+1] for i in range(0, 12, 2)]

tarifa = 2.5  # pesos por kWh
ahorro_bimestral = [round(mes*tarifa, 2) for mes in generacion_bimestral]



print(ahorro_bimestral)

meses = ["Ene-Feb", "Mar-Abr", "May-Jun",
         "Jul-Ago", "Sep-Oct", "Nov-Dic"]
cfe = [308, 524, 1449, 1713, 1325, 591]

# Crear gráfico de barras
plt.figure(figsize=(10, 5))
plt.bar(meses, ahorro_bimestral)

# Añadir títulos y etiquetas
plt.title("Ahorro mensual estimado en pesos")
plt.xlabel("Mes")
plt.ylabel("Ahorro (MXN)")
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, valor in enumerate(ahorro_bimestral):
    plt.text(i, valor + 15, f"${valor:.0f}", ha='center', va='bottom')

plt.tight_layout()
plt.show()

media = statistics.mean(ahorro_bimestral)
mediana = statistics.median(ahorro_bimestral)
moda = statistics.mode(ahorro_bimestral)  # cuidado si no hay moda única
desviacion_estandar = statistics.stdev(ahorro_bimestral)

print(media, mediana, moda, desviacion_estandar)

x = np.arange(len(meses))  # [0, 1, 2, 3, 4, 5]
ancho = 0.35  # ancho de cada barra

# Crear gráfico
plt.figure(figsize=(10, 5))
barras_gen = plt.bar(x - ancho/2, generacion_bimestral, width=ancho, label='Generación solar')
barras_con = plt.bar(x + ancho/2, cfe, width=ancho, label='Consumo CFE')

# Etiquetas y título
plt.xticks(x, meses)
plt.ylabel('Energía (kWh) o Ahorro ($)')
plt.title('Comparación Bimestral: Generación vs. Consumo')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

for barra in barras_gen:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, altura + 50, f'{altura:.0f}', ha='center', va='bottom')

for barra in barras_con:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, altura + 50, f'{altura:.0f}', ha='center', va='bottom')


# Mostrar el gráfico
plt.tight_layout()
plt.show()

