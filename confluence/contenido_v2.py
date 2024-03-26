import funciones_v2

dominio_confluence = 'baufest.atlassian.net'
page_id = '903413870' 
usuario = 'svilchis@baufest.com'
token = 'ATATT3xFfGF0gSwgbo70SselECLe7sXvyLPRWzn8rO6gVhXPpVAmkCZ8-tmNjpxT06wYw_PJT5A14578r4Y2rhWPzKCTdlhQt88fBy39azRC-FmD8wkTXwhWSbnSP2kQ2PbxPGqnYsbp38qdceUFVDQmj5de6yD6s9D8y3MtjEe3ieXP1oYuvtY=C545D6FD'

urls = [
    f'https://{dominio_confluence}/wiki/rest/api/content/{page_id}',
    f'https://{dominio_confluence}/wiki/rest/api/content/{page_id}?expand=body.view',
    f'https://{dominio_confluence}/wiki/rest/api/content/{page_id}/child/page',
]

ruta_base = urls[0]
rutas = [url.replace(ruta_base, '') for url in urls]

contenido = []

for url, tipo_pagina in zip(urls, rutas):
    peticion = funciones_v2.solicitud_get(url, usuario, token)
    contenido.extend(funciones_v2.extraer_informacion(peticion, tipo_pagina))

nombre_archivo = 'contenido_confluence.txt'
indice = 'Divisiones'
funciones_v2.guardar_archivo(contenido, nombre_archivo, indice, 0)

contenido_hijos = []

def procesar_objeto(contenido, principal, secundario, objetos_procesados={}, profundidad=0, orden=''):
    
    for pagina in contenido[principal]:

        if profundidad == 0:
            orden = ''
        
        if secundario in pagina and "URL" in pagina:
            pagina_titulo = str(pagina[secundario]).replace("/","-")
            nombre_archivo = f"archivos/contenido_{pagina_titulo}.txt"
            peticion_hijos = funciones_v2.solicitud_get(pagina['URL']  + '/child/page?limit=58', usuario, token)
            
            nivel = funciones_v2.verificar_nivel(profundidad)
            nivel_anterior = funciones_v2.verificar_nivel_anterior(profundidad-1)

            contenido_hijos = funciones_v2.extraer_informacion_hijos(peticion_hijos, pagina[secundario], secundario, nivel, nivel_anterior)
            
            for objeto in contenido_hijos:
                if objeto[nivel]:
                    if orden == '': 
                        funciones_v2.guardar_archivo(contenido_hijos, nombre_archivo, nivel, profundidad)
                    else:
                        funciones_v2.guardar_archivo(contenido_hijos, orden, nivel, profundidad)
            
            clave_objeto = f"{profundidad}_{pagina[secundario]}"
            objetos_procesados[clave_objeto] = contenido_hijos
            
            for obj in contenido_hijos:
                if nivel in obj and obj[nivel]:
                    if profundidad == 0 :
                        orden = f"archivos/contenido_{pagina[secundario]}.txt"
                    procesar_objeto(obj, nivel, nivel_anterior, objetos_procesados, profundidad + 1, orden)
                else:
                    peticion_pagina = funciones_v2.solicitud_get(pagina['URL']  + '?expand=body.view', usuario, token)
                    contenido_pagina = funciones_v2.extraer_contenido(peticion_pagina, obj, nivel)

                    if orden != '':
                        funciones_v2.guardar_archivo(contenido_pagina, orden, nivel, profundidad)
                    else:
                        funciones_v2.guardar_archivo(contenido_pagina, nombre_archivo, nivel, profundidad)

    return objetos_procesados

resultado_final = procesar_objeto(contenido[2], indice, 'División')