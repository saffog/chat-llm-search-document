from dotenv import load_dotenv
import os
import utils_commercial
import utils_general

dominio_confluence = os.getenv('Dominio_confluence')
usuario = os.getenv('Usuario_confluence')
page_id = '903413870' 
token = os.getenv('Token_ID')

urls = [
    f'https://{dominio_confluence}/wiki/rest/api/content/{page_id}',
    f'https://{dominio_confluence}/wiki/rest/api/content/{page_id}?expand=body.view',
    f'https://{dominio_confluence}/wiki/rest/api/content/{page_id}/child/page',
]

ruta_base = urls[0]
rutas = [url.replace(ruta_base, '') for url in urls]

contenido = []

for url, tipo_pagina in zip(urls, rutas):
    peticion = utils_general.solicitud_get(url, usuario, token)
    contenido.extend(utils_commercial.extraer_informacion(peticion, tipo_pagina))

nombre_archivo = 'contenido_confluence.txt'
indice = 'Divisiones'
utils_commercial.guardar_archivo(contenido, nombre_archivo, indice, 0)

contenido_hijos = []

def procesar_objeto(contenido, principal, secundario, objetos_procesados={}, profundidad=0, orden=''):
    
    for pagina in contenido[principal]:

        if profundidad == 0:
            orden = ''
        
        if secundario in pagina and "URL" in pagina:
            pagina_titulo = str(pagina[secundario]).replace("/","-")
            nombre_archivo = f"textos/contenido_{pagina_titulo}.txt"
            peticion_hijos = utils_general.solicitud_get(pagina['URL']  + '/child/page?limit=58', usuario, token)
            
            nivel = utils_commercial.verificar_nivel(profundidad)
            nivel_anterior = utils_commercial.verificar_nivel_anterior(profundidad-1)

            contenido_hijos = utils_commercial.extraer_informacion_hijos(peticion_hijos, pagina[secundario], secundario, nivel, nivel_anterior)
            
            for objeto in contenido_hijos:
                if objeto[nivel]:
                    if orden == '': 
                        utils_commercial.guardar_archivo(contenido_hijos, nombre_archivo, nivel, profundidad)
                    else:
                        utils_commercial.guardar_archivo(contenido_hijos, orden, nivel, profundidad)
            
            clave_objeto = f"{profundidad}_{pagina[secundario]}"
            objetos_procesados[clave_objeto] = contenido_hijos
            
            for obj in contenido_hijos:
                if nivel in obj and obj[nivel]:
                    if profundidad == 0 :
                        orden = f"textos/contenido_{pagina[secundario]}.txt"
                    procesar_objeto(obj, nivel, nivel_anterior, objetos_procesados, profundidad + 1, orden)
                else:
                    peticion_pagina = utils_general.solicitud_get(pagina['URL']  + '?expand=body.view', usuario, token)
                    contenido_pagina = utils_commercial.extraer_contenido(peticion_pagina, obj, nivel)

                    if orden != '':
                        utils_commercial.guardar_archivo(contenido_pagina, orden, nivel, profundidad)
                    else:
                        utils_commercial.guardar_archivo(contenido_pagina, nombre_archivo, nivel, profundidad)

    return objetos_procesados

resultado_final = procesar_objeto(contenido[2], indice, 'División')