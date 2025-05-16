# PIA
Programa creado para el Proyecto Integrador de Aprendizaje de la clase Programación Básica

## EQUIPO FORMADO POR:
* **Cesar Alanis**
* **Jorge Sanchez**
* **Ximena Rocha**
* **Carlos Gomez**
* **Manuel Puente**

## Planteamiento del problema

### Problema: Predicción de cuánta energía va a producir un sistema fotovoltaico en un año, de acuerdo con su ubicación geográfica.

En los últimos años, las altas temperaturas registradas en México —especialmente en el estado de Nuevo León— han hecho indispensable el uso de sistemas de aire acondicionado en los hogares, permitiendo a las familias mantener un ambiente cómodo y seguro. No obstante, estos sistemas representan un alto consumo energético, lo que se traduce en un incremento considerable en la tarifa eléctrica.

Afortunadamente, el avance en tecnologías basadas en semiconductores ha hecho que los sistemas fotovoltaicos (paneles solares) sean hoy más accesibles que nunca. Hasta finales de 2023, México se posicionó como el segundo país de América Latina con mayor capacidad instalada de energía solar fotovoltaica, alcanzando un total de 10.8 GW, solo por detrás de Brasil, con 37.5 GW (Intersolar México, 2023). Este crecimiento ha sido constante en los últimos años, pasando de 7.4 GW en 2021 a más de 10.8 GW en 2023 (Intersolar México, 2023). Además, el país cuenta con uno de los mayores potenciales solares del mundo debido a su alta irradiación solar promedio, lo que lo convierte en un actor clave en la transición energética regional (Trade.gov, 2023).

El crecimiento de los sistemas fotovoltaicos no solo permite mitigar el impacto económico del consumo eléctrico doméstico, sino que también representa una alternativa ambientalmente sostenible. En México, gran parte de la electricidad sigue generándose mediante combustibles fósiles; por lo tanto, el uso de energía solar contribuye significativamente a la reducción de emisiones de carbono.

La creciente demanda de sistemas fotovoltaicos de generación distribuida ha puesto sobre la mesa la necesidad de que las empresas automatizen el proceso de cotización y análisis energético. Automatizar esta etapa no solo agiliza la atención al cliente, sino que también reduce errores humanos, mejora la presentación de resultados y permite tomar decisiones más rápidas y fundamentadas. Este software representa un gran paso hacia esa automatización, ya que permite estimar la generación energética mensual a partir de una dirección y potencia ingresadas, y genera un informe completo con análisis económico, visualizaciones gráficas y estadísticas clave. Utilizando la API de PVGIS, se simula la producción energética anual del sistema, permitiendo comparar dicha generación contra consumos históricos, mejorar la toma de decisiones y facilitar la evaluación de viabilidad económica para los usuarios finales.

## PVGIS

Este proyecto emplea la API PVGIS (Photovoltaic Geographical Information System), desarrollada por el Joint Research Centre (JRC) de la Comisión Europea, para estimar la producción energética de un sistema fotovoltaico residencial en Monterrey, Nuevo León.

Se utilizó específicamente el endpoint PVcalc de la versión 5.2 de la API, que permite simular la generación de energía mensual y anual de un sistema fotovoltaico basado en los siguientes parámetros:

Latitud y longitud del sitio: 25.67, -100.31

Potencia pico instalada: 3.99 kW

Pérdidas del sistema: 14%

Ángulo de inclinación: 20° 

Orientación: 180° (hacia el sur)

Formato de salida: JSON

La consulta se realiza mediante el método HTTP GET utilizando la biblioteca requests en Python. Los datos obtenidos incluyen la producción mensual estimada (en kWh), que posteriormente se agrupan en bimestres y se comparan con los consumos reales proporcionados por el usuario a partir de sus recibos de CFE.

Además, se generan visualizaciones comparativas que permiten al usuario identificar de forma clara si el sistema es capaz de cubrir su consumo, así como el ahorro económico estimado.

En caso de no contar con conexión a internet, el script incluye un mecanismo de respaldo que permite utilizar una consulta previa guardada localmente (prueba.json).

Para más información sobre la API de PVGIS y sus especificaciones técnicas, puedes consultar la documentación oficial en el siguiente enlace: [Documentación API PVGIS](https://joint-research-centre.ec.europa.eu/photovoltaic-geographical-information-system-pvgis/getting-started-pvgis/api-non-interactive-service_en).

## API Nominatim – OpenStreetMap

Nominatim es un servicio de geocodificación desarrollado por OpenStreetMap (OSM) que permite convertir direcciones físicas en coordenadas geográficas (latitud y longitud) y viceversa. Es ampliamente utilizado para aplicaciones de mapeo, navegación, análisis espacial y automatización de ubicaciones.

### Funcionalidades principales:
Geocodificación directa: convierte una dirección como "Av. Universidad, Monterrey" en coordenadas (lat, lon).

Geocodificación inversa: a partir de coordenadas geográficas, devuelve una dirección aproximada.

Búsquedas estructuradas: permite enviar partes de una dirección (ciudad, país, calle) como parámetros separados.

Resultados detallados: entrega el nombre completo (display_name) del lugar, el tipo de ubicación y su jerarquía administrativa (país, estado, municipio, etc.).

[Documentación oficial:](https://nominatim.org/release-docs/latest/api/Overview/)


