## Justificación de la estructura de datos utilizada

En este proyecto, se utilizaron **diccionarios** y **listas** como estructuras principales para procesar los resultados obtenidos de la API de PVGIS. Esta elección se justifica tanto por la **naturaleza del formato JSON** de la respuesta, como por la **facilidad que ofrecen estas estructuras para la manipulación y visualización de datos**.

###  Diccionario (`dict`)

* La API devuelve los datos en formato JSON, que es análogo a un diccionario en Python.
* Se utilizó un diccionario llamado `energia_mensual` para almacenar la **energía mensual generada**, donde:

  * La **clave** es el nombre del mes (ej. `"enero"`)
  * El **valor** es la energía producida ese mes (`E_m`, en kWh)
* Esto facilita el acceso directo a la energía de un mes específico mediante su nombre, y mejora la **legibilidad del código**.

```python
energia_mensual = {
    "enero": 90.3,
    "febrero": 102.1,
    ...
}
```

### Lista (`list`)

* Posteriormente, se extraen las claves y valores del diccionario para almacenarlos en listas separadas (`meses` y `energia`), lo cual es más conveniente para graficar:

```python
meses = list(energia_mensual.keys())
energia = list(energia_mensual.values())
```

* Las listas permiten recorrer los datos secuencialmente y ordenarlos fácilmente para su uso en **visualizaciones con matplotlib**.

---
Esta combinación de **diccionario + listas** ofrece una estructura eficiente, clara y funcional:

* El diccionario estructura y asocia los datos semánticamente.
* Las listas permiten visualizar los datos de forma ordenada y directa.
* Además, se minimiza la necesidad de estructuras complejas, lo cual es adecuado para un procesamiento y visualización de datos relativamente simple como este.
