# Simulador de Producción Solar con Informe Automático

Este proyecto en Python permite al usuario estimar la producción mensual de energía eléctrica mediante un sistema fotovoltaico, utilizando coordenadas geográficas proporcionadas por una dirección, y genera un reporte automatizado en Excel con gráficas y estadísticas.

---

## Funcionalidades

- Obtiene **coordenadas** a partir de una dirección con la API de [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org).
- Consulta la **producción solar estimada** con la API pública [PVGIS](https://re.jrc.ec.europa.eu/pvg_tools/es/tools.html).
- Permite trabajar **sin conexión a internet** usando un respaldo local (`prueba.json`).
- Exporta un archivo Excel `.xlsx` con:
  - Energía mensual estimada (kWh)
  - Ahorro mensual estimado (MXN)
  - Gráfica de producción mensual
  - Gráfica de ahorro
  - Estadísticas básicas: media, mediana, moda y desviación estándar

---

## Estructura de archivos

```
.
├── main.py                 # Script principal (orquestador)
├── modulos.py             # Funciones auxiliares (API, validaciones, exportaciones)
├── prueba.json            # Archivo JSON de respaldo (coordenadas y datos simulados)
├── grafica_energia.png    # Generado automáticamente
├── grafica_ahorro.png     # Generado automáticamente
└── informe_solar.xlsx     # Reporte final generado
```

---

## Requisitos

- Python 3.8 o superior
- Librerías necesarias:

```bash
pip install requests openpyxl matplotlib
```

---

## Cómo usarlo

1. Clona el repositorio o descarga los archivos.
2. Ejecuta `main.py`:

```bash
python main.py
```

3. Sigue las instrucciones en consola:
   - Ingresa una dirección (ej. `"Av. Universidad, Monterrey"`)
   - Elige una opción de la lista sugerida
   - Ingresa la potencia del sistema en kW

4. Se generará un archivo `informe_solar.xlsx` con toda la información.

---

## Ejemplo de salida en Excel

- Producción mensual:
  ```
  enero     → 123.4 kWh
  febrero   → 142.1 kWh
  ...
  ```

- Ahorro mensual (calculado a $2.50 MXN/kWh)

- Estadísticas:
  - Media, mediana, moda y desviación estándar de energía y ahorro

- Gráficas incrustadas en el Excel 📊

---

## Lógica interna destacada

- Validación de entrada con **expresiones regulares**
- Soporte para trabajar **sin conexión**
- Gráficas dinámicas generadas con `matplotlib`
- Informe automático usando `openpyxl` y `ExcelImage`

---

## Licencia

MIT — Puedes usar y modificar este proyecto libremente, siempre que des crédito al autor original.

---



