import requests

# Dirección que quieres convertir
direccion = "Universidad Autonoma de Nuevo Leon, San Nicolas de los Garza, Nuevo Leon"


# Parámetros para la API
params = {
    "q": direccion,
    "format": "json"
}

# Encabezado con User-Agent obligatorio si haces varias peticiones
headers = {
    "User-Agent": "MiAppDeGeocodificacion/1.0 (alejandro.alanisgrrr@gmail.com)"
}

# Hacer la solicitud
response = requests.get("https://nominatim.openstreetmap.org/search", params=params, headers=headers)
data = response.json()

# Mostrar resultado
if data:
    "Resultados: "
    for i in range(0,len(data)):
        if i <= 10:
            print(f"{i+1}. {data[i]['display_name']}\n")

    """
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    print(f"Latitud: {lat}")
    print(f"Longitud: {lon}")
    """
else:
    print("No se encontraron resultados.")
