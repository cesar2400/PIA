import os
import time
from openpyxl import Workbook as work
from openpyxl import load_workbook as lw
from os.path import exists
import pandas as pd
import os 
import json
from re import search

def limpiar_pantalla():
	os.system('cls' if os.name == 'nt' else 'clear')
	
def pedir_numero_int(numero = None, mensaje = "Numero: "):
	num_match = search(r"\d+",numero)
	while num_match == None or num_match.group() != numero:
		numero = input(mensaje)
		num_match = search(r"\d+",numero)
		#print(numero,num_match)
		
		if not num_match == None and num_match.group() == numero:
			break
	return int(numero)
	
def abrir_cerrar_archivo(ruta_archivo): # Reemplaza con la ruta real de tu archivo
	try:
		os.startfile(ruta_archivo)
		print(f"Abriendo el archivo: {ruta_archivo}")
	except FileNotFoundError:
		print(f"El archivo no fue encontrado: {ruta_archivo}")
	except OSError as e:
		print(f"No se pudo abrir el archivo. Error: {e}")
	n = int(input("Introduzca el tiempo de espera en minutos. \n>>> "))
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

def crear_tabla(datos: dict or list,nombre_hoja = None,nombre_archivo = None,nueva_hoja = None):
	archivo,hoja = abrir_crear(nombre_archivo,nombre_hoja,nueva_hoja)
	
	df = pd.DataFrame(datos)
	
	archivo.save(nombre_archivo)

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
	nombre_archivo = 'excel_usuario.xlsx'
	nombre_hoja = 'Usuarios'
	
	datos = contenido_excel(nombre_archivo,nombre_hoja)
	#input(datos)
	
	datos1 = extraer_datos('prueba.json')
	
	datos.append(datos1)
		
	#input(datos)
	guardar_excel(nombre_archivo,nombre_hoja,datos)
	
	datos = contenido_excel(nombre_archivo,nombre_hoja)
	#input(datos)
	
	ruta_archivo = r'excel_usuario.xlsx' 
	abrir_cerrar_archivo(ruta_archivo)
