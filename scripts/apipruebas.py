import requests
import json
import matplotlib.pyplot as plt

url = "https://re.jrc.ec.europa.eu/api/v5_3/PVcalc"

params = {
    "lat": 25.67,
    "lon": -100.32,
    "peakpower": 1,
    "loss": 14,
    "outputformat": "json"
}

response = requests.get(url, params)

if response.status_code == 200:
	try: 
		response = response.json()
	except Exception as e:
		print("Error al procesar JSON:", e)
		
else:
	print(f"Error en la API: código {response.status_code}")
outputs = response["outputs"]

print(response) 	



energia_mensual={} #diccionario que contiene la energia mensual 

meses_nombre = {
    1: 'enero',
    2: 'febrero',
    3: 'marzo',
    4: 'abril',
    5: 'mayo',
    6: 'junio',
    7: 'julio',
    8: 'agosto',
    9: 'septiembre',
    10: 'octubre',
    11: 'noviembre',
    12: 'diciembre'
}



# codigo para llenar el diccionario
meses = outputs['monthly']['fixed']
for diccionario in meses:
	mes = diccionario['month']
	energia = diccionario['E_m']
	nombre_mes = meses_nombre[mes]
	energia_mensual[nombre_mes]=energia

print(energia_mensual)
meses = list(energia_mensual.keys())
energia = list(energia_mensual.values())

	
# Gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(meses, energia)
plt.xlabel('Mes')
plt.ylabel('Energía mensual (kWh)')
plt.title('Producción mensual de energía')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()		
	
		
	

	
