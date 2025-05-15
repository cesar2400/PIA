import modulos as mo
import prueba_excel as pe

def main():
    # Primero verificamos si hay internet
    if mo.hay_internet():
        # Usamos flujo interactivo para obtener coordenadas desde OpenStreetMap
        lat, lon, ubi = mo.obtener_coordenadas_interactivas()
        potencia_kw = float(input("Ingrese la potencia de su sistema: "))
        perdidas = 14
        if lat is None or lon is None:
            print("No se pudo convertir la dirección en coordenadas.")
            return
    else:
        # Sin internet, cargamos lat/lon desde archivo local (como prueba.json)
        print("No hay conexión a internet. Usando datos locales de respaldo...")
        datos_locales = mo.cargar_json_local()
        if datos_locales is None:
            print("❌ No se pudo cargar el archivo local.")
            return
        try:
            lat = datos_locales["inputs"]["location"]["latitude"]
            lon = datos_locales["inputs"]["location"]["longitude"]
        except KeyError:
            print("❌ El archivo local no contiene coordenadas válidas.")
            return

    # Pedimos la potencia (esto se puede hacer siempre, tenga o no internet)
    

    if mo.hay_internet():
        print("Conexión detectada. Consultando PVGIS...")
        datos = mo.obtener_datos_pvgis(lat, lon, potencia_kw, perdidas)
    else:
        print("Sin conexión. Cargando nuevamente los datos locales...")
        datos = mo.cargar_json_local()

    if datos:
        energia_mensual = mo.extraer_energia_mensual(datos)
        print(" Energía mensual estimada (kWh):")
        for mes, energia in energia_mensual.items():
            print(f"{mes.capitalize()}: {energia:.2f}")
        mo.graficar_energia_mensual(energia_mensual)
    else:
        print("No se pudieron obtener los datos del sistema.")

    pe.exportar_a_excel(energia_mensual, ubi, nombre_archivo="informe_solar.xlsx")

main()
