MeteoCaracas Valeria Guedez 

requisitos: Python 3 y Librerías: requests, pandas, matplotlib, numpy

Para Instalar las dependecias: ejecutar: pip install requests pandas matplotlib numpy

Como ejecutar el programa : Desde la carpeta meteocaracas ejecutar: python main.py

Estructura del proyecto

meteocaracas/
 main.py                   punto de entrada, menu principal

 datos/
    zonas_caracas.json     localidades por municipio

 modelos/
    municipio.py           clase Municipio
    localidad.py           clase Localidad
    clima.py               clase Clima
    
 servicios/
    carga_datos.py         lectura del json y reporte de carga
    busqueda.py            busqueda de municipios y localidades
    clima_api.py           consulta del clima en tiempo real
    estadisticas.py        ranking, promedio y cobertura geografica
    historicos.py          consulta y analisis de clima histórico

README.md                  instrucciones e instalación
