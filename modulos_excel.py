import os
import time
from openpyxl import Workbook as work
from openpyxl import load_workbook as lw
from os.path import exists
import pandas as pd
import os 
import json
from re import search
import pyautogui
import subprocess
import psutil

def obtener_nombre_proceso(nombre_parcial_aplicacion):
	nombres_encontrados = []
	for proc in psutil.process_iter(['pid', 'name']):
		if nombre_parcial_aplicacion.lower() in proc.info['name'].lower():
			nombres_encontrados.append(proc.info['name'])
	return nombres_encontrados

def cerrar_proceso_windows(nombre_proceso):
	"""
	Intenta terminar un proceso por su nombre en Windows.
	Ejemplo: Si sabes que la aplicación se llama "mi_aplicacion.exe"
		cerrar_proceso_windows("mi_aplicacion.exe")
	"""
	try:
		subprocess.run(['taskkill', '/F', '/IM', f'{nombre_proceso}'], check=True)
	except subprocess.CalledProcessError as e:
		print(f"Error al intentar terminar el proceso '{nombre_proceso}': {e}")
	except FileNotFoundError:
		print("El comando 'taskkill' no se encontró (esto debería ser raro en Windows).")


def limpiar_pantalla():
	"""
	Esta función solo sirve para el sistema operativo de Windows cmd.
	Facilita la visualización de los datos pero, a no ser que se tengan almacenados los datos de antemano, se perderan.

	"""
	os.system('cls' if os.name == 'nt' else 'clear')
	
def pedir_numero_int(numero = None, mensaje = "Numero: "):
	"""
	Esta función se emplea en situaliones en las que es necesario obtener un numero entero.
	"""
	if numero:
		num_match = search(r"\d+",numero)
	else:
		num_match = None
	while not num_match or num_match.group() != numero:
		numero = input(mensaje)
		num_match = search(r"\d+",numero)
		#print(numero,num_match)
		
		if not num_match == None and num_match.group() == numero:
			break
	return int(numero)
	
def abrir_archivo(ruta_archivo,nombre_parcial  = None): 
	"""
	Literalmente una función que abre y luego cierra automaticamente un archivo desde el sistema operativo de windows.
	Declaración de variables:
		ruta_archivo: Reemplaza con la ruta real de tu archivo con el formato r'*Ruta_especifica*' 
	"""
	print("Presione enter si desea poner un cronometro especifico, \"5\" si desea que solo espere los 5 minutos preestablesidos o cualquier otra tecla no realizar el proceso.")
	sn = input(">>> ")
	if sn == "":
		n = int(input("Introduzca el tiempo de espera en minutos. \n>>> "))
	elif sn == "5":
		n = None
	else:
		n = ""
	try:
		os.startfile(ruta_archivo)
		print(f"Abriendo el archivo: {ruta_archivo}")
	except FileNotFoundError:
		print(f"El archivo no fue encontrado: {ruta_archivo}")
	except OSError as e:
		print(f"No se pudo abrir el archivo. Error: {e}")
	
	if nombre_parcial:
		procesos = obtener_nombre_proceso(nombre_parcial)
	elif n != "":
		print("No se introdujo el nombre de la aplicación.")
		return
	
	if not n and procesos:
		pausar()
		for i in range(len(procesos)):
			cerrar_proceso_windows(procesos[i])
		print(f"Archivo {ruta_archivo} cerrado")
	elif n != "" and procesos:
		pausar(n)
		for i in range(len(procesos)):
			cerrar_proceso_windows(procesos[i])
		print(f"Archivo {ruta_archivo} cerrado")
	

def pausar(n = None):
	if not n:
		print("Tiene 5 minutos.")
		for i in range(5):
			time.sleep(60)
	elif n:
		for i in range(n):
			time.sleep(60)
		

def abrir_crear(nombre_archivo = None,nombre_hoja = None,nueva_hoja = None):
	if exists(nombre_archivo):
		try:
			archivo = lw(nombre_archivo)
		except Exception as e:
			archivo = work()
	else:
		archivo = work()
		
	if not (nombre_hoja and nueva_hoja):
		hoja = archivo.active
	elif nueva_hoja and nombre_hoja:
		archivo.create_sheet(nombre_hoja)
		hoja = archivo[nombre_hoja]
	elif nueva_hoja:
		archivo.create_sheet('Sheet')
		hoja = archivo['Sheet']
	elif nombre_hoja and nombre_hoja in archivo:
		hoja = archivo[nombre_hoja]
	elif nombre_hoja:
		hoja = archivo.active
		hoja.title = nombre_hoja
	else:
		hoja = archivo.active
	return archivo,hoja


def contenido_excel(nombre_archivo = None,nombre_hoja = None):
	archivo,hoja = abrir_crear(nombre_archivo,nombre_hoja)
	list_name = archivo.sheetnames
	archivo.save(nombre_archivo)

	datos = []
	for i in range(len(list_name)):
		datos.append(pd.read_excel(nombre_archivo,list_name[i]))
		datos[i] = datos[i].to_dict(orient='list')
		
	return datos	
	
def guardar_excel(nombre_archivo = None,nombre_hoja = None, datos = None):
	archivo,hoja = abrir_crear(nombre_archivo,nombre_hoja,nueva_hoja = True)
	list_name = archivo.sheetnames
	archivo.save(nombre_archivo)
	
	if type(datos) == list:
		aux = []
		for i in range(len(datos)):
			aux.append(pd.DataFrame(datos[i]))
		guardar_varios(nombre_archivo,list_name,aux)
	elif type(datos) == dict:
		df = pd.DataFrame(datos)
		with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
			df.to_excel(writer, sheet_name=nombre_hoja, index=False)
	
def guardar_varios(nombre_archivo,nombres_hojas,dataframes):
	if len(dataframes) != len(nombres_hojas):
		raise ValueError("La lista de DataFrames y la lista de nombres de hojas deben tener la misma longitud.")
	try:
		# Crear un objeto ExcelWriter para gestionar la escritura en el archivo
		with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
			# Iterar sobre los DataFrames y sus nombres de hoja correspondientes
			for i, df in enumerate(dataframes):
				nombre_hoja = nombres_hojas[i]
				df.to_excel(writer, sheet_name=nombre_hoja, index=False)  # Escribir el DataFrame en la hoja
			print(f"Se han guardado los DataFrames en el archivo '{nombre_archivo}'.")
		
	except Exception as e:
		print(f"Ocurrió un error al guardar los DataFrames en Excel: {e}")

def extraer_datos(archivo_json):
	with open(archivo_json,'r') as archivo:
		resultado = json.load(archivo)
	
	limpiar_pantalla()
	outputs = resultado['outputs']
	aux = outputs['monthly']['fixed']
	mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
	datos = []
	
	for i in range(len(aux)):
		datos.append(dict())
		datos[i]['Mes'] = mes[i] 
		for j in aux[i].keys():
			if j != "month":
				datos[i][j] = aux[i][j]
	return datos
	

if __name__ == "__main__":
	limpiar_pantalla()


	nombre_archivo = 'excel_usuario.xlsx'
	nombre_hoja = 'Usuarios'


	procesos = obtener_nombre_proceso("Excel")

	input(procesos)
	for i in range(len(procesos)):
		cerrar_proceso_windows(procesos[i])
		time.sleep(3)
	# Esta parte fue añadida para evitar que el proceso se interumpa por que el archivo esté abierto.
	
	datos = contenido_excel(nombre_archivo,nombre_hoja)
	#input(datos)
	
	datos1 = extraer_datos('prueba.json')
	
	datos.append(datos1)
		
	#input(datos)
	guardar_excel(nombre_archivo,nombre_hoja,datos)
	
	datos = contenido_excel(nombre_archivo,nombre_hoja)
	#input(datos)
	
	ruta_archivo = r'excel_usuario.xlsx' 
	abrir_archivo(ruta_archivo,"Excel")
	
	datos = contenido_excel(nombre_archivo,nombre_hoja)
	#input(datos)
	
	ruta_archivo = r'excel_usuario.xlsx' 
	abrir_cerrar_archivo(ruta_archivo)
