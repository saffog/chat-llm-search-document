from dotenv import load_dotenv
import os
import funciones_v1

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
    peticion = funciones_v1.solicitud_get(url, usuario, token)
    contenido.extend(funciones_v1.extraer_informacion(peticion, tipo_pagina))

nombre_archivo = 'contenido_confluence.txt'
indice = 'Divisiones'
funciones_v1.guardar_archivo(contenido, nombre_archivo, indice, 0)

contenido_hijos = []

def procesar_objeto(contenido, principal, secundario, objetos_procesados={}, profundidad=0):
    
    for pagina in contenido[principal]:
        
        if secundario in pagina and "URL" in pagina:
            pagina_titulo = str(pagina[secundario]).replace("/","-")
            nombre_archivo = f"archivos/contenido_{pagina_titulo}.txt"
            peticion_hijos = funciones_v1.solicitud_get(pagina['URL']  + '/child/page?limit=58', usuario, token)
            
            nivel = funciones_v1.verificar_nivel(profundidad)
            nivel_anterior = funciones_v1.verificar_nivel_anterior(profundidad-1)

            contenido_hijos = funciones_v1.extraer_informacion_hijos(peticion_hijos, pagina[secundario], secundario, nivel, nivel_anterior)
            
            for objeto in contenido_hijos:
                if objeto[nivel]:
                    funciones_v1.guardar_archivo(contenido_hijos, nombre_archivo, nivel)
            
            clave_objeto = f"{profundidad}_{pagina[secundario]}"
            objetos_procesados[clave_objeto] = contenido_hijos
            
            for obj in contenido_hijos:
                if nivel in obj and obj[nivel]:
                    procesar_objeto(obj, nivel, nivel_anterior, objetos_procesados, profundidad + 1)
                else:
                    peticion_pagina = funciones_v1.solicitud_get(pagina['URL']  + '?expand=body.view', usuario, token)
                    contenido_pagina = funciones_v1.extraer_contenido(peticion_pagina, obj, nivel)

                    funciones_v1.guardar_archivo(contenido_pagina, nombre_archivo, nivel)

    return objetos_procesados

resultado_final = procesar_objeto(contenido[2], indice, 'División')

'''
def obtener_info(elemento, titulo):
    archivo_nombre = "archivos/contenido_confluence_" + titulo +".txt"
    for pagina in elemento["paginas"]:
        if "titulo" in pagina and "URL" in pagina:
            peticion_hijos = funciones.solicitud_get(pagina['URL'] + '/child/page', usuario, token)
            contenido_hijos.extend(funciones.extraer_informacion_hijos(peticion_hijos, pagina['titulo']))

    confluence_hijos = json.dumps(contenido_hijos, indent=4)
    with open(archivo_nombre, 'w', encoding='utf-8') as file:
            file.write(confluence_hijos)
    print(f"Todo el contenido se ha guardado en '{archivo_nombre}'")
    return contenido_hijos

def procesar_objeto(contenido, titulo):

    for elemento in contenido:
        if 'paginas' in elemento:
            resultado = obtener_info(elemento, titulo)
            
            for obj in resultado:
                if obj["paginas"]:
                    obtener_info(obj, titulo)

            return procesar_objeto(contenido_hijos, titulo)
             
    
resultado_final = procesar_objeto(contenido, contenido[0]['titulo'])

    for obj in contenido_hijos:
    if "paginas" in obj and obj["paginas"]:
        return procesar_objeto(contenido_hijos, pagina['titulo'])
'''