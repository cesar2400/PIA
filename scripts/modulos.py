import requests
import json
import matplotlib.pyplot as plt

def obtener_datos_pvgis(lat, lon, potencia_kw, perdidas):
    url = "https://re.jrc.ec.europa.eu/api/v5_3/PVcalc"
    params = {
        "lat": lat,
        "lon": lon,
        "peakpower": potencia_kw,
        "loss": perdidas,
        "outputformat": "json"
    }
    response = requests.get(url, params)
    if response.status_code == 200:
        try:
            return response.json()
        except Exception as e:
            print("Error al procesar JSON:", e)
    else:
        print(f"Error en la API: código {response.status_code}")
    return None

def extraer_energia_mensual(data_json):
    meses_nombre = {
        1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
        5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto',
        9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
    }
    energia_mensual = {}
    meses = data_json['outputs']['monthly']['fixed']
    for diccionario in meses:
        mes = diccionario['month']
        energia = diccionario['E_m']
        nombre_mes = meses_nombre[mes]
        energia_mensual[nombre_mes] = energia
    return energia_mensual

def graficar_energia_mensual(energia_mensual):
    meses = list(energia_mensual.keys())
    energia = list(energia_mensual.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(meses, energia)
    plt.xlabel('Mes')
    plt.ylabel('Energía mensual (kWh)')
    plt.title('Producción mensual de energía')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def main():
    datos = obtener_datos_pvgis(25.67, -100.32, 1, 14)
    if datos:
        energia_mensual = extraer_energia_mensual(datos)
        print(energia_mensual)
        graficar_energia_mensual(energia_mensual)
    else:
        print("No se pudieron obtener los datos de la API.")

if __name__ == "__main__":
    main()
