import os
import json

def cargar_json_local():
    """
    Carga y retorna el contenido del archivo JSON ubicado en 'datos/prueba.json'.
    Si el archivo no existe o es inválido, se muestra un mensaje de error.
    """
    

    try:
        with open("prueba.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except FileNotFoundError:
        print("⚠️ El archivo 'prueba.json' no se encontró.")
        return None

    except json.JSONDecodeError:
        print("⚠️ El archivo no contiene un JSON válido.")
        return None


print(cargar_json_local())
