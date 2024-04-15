from bs4 import BeautifulSoup

def extraer_informacion(contenido, tipo_pagina):

    info = []
    paginas = {
        'Divisiones' : []
    }

    if tipo_pagina == '?expand=body.view':
        contenido_general = contenido['body']['view']['value']
        soup = BeautifulSoup(contenido_general, 'html.parser')
        texto = soup.get_text().replace('\n', ' ')
        info.extend([{'contenido': texto}])
    
    elif tipo_pagina == '/child/page':
        for contenido_general in contenido['results']:
            id = contenido_general['id']
            titulo = contenido_general['title']
            link = contenido_general['_links']['self']
            pagina = {
                'id' : id,
                'División' : titulo,
                'URL' : link
            }
            paginas['Divisiones'].append(pagina)
        info.extend([paginas])
    
    else:
        autor = contenido['version']['by']['displayName']
        titulo = contenido['title']
        info.extend([{
                'autor': autor,
                'titulo': titulo
            }])
    
    return info

def extraer_informacion_hijos(contenido, titulo, secundario, nivel, nivel_anterior):

    paginas = {
        secundario : titulo,
        nivel : [
             {
                'id': contenido_general['id'],
                nivel_anterior: contenido_general['title'],
                'URL': contenido_general['_links']['self']
            }
            for contenido_general in contenido['results']
        ]
    }

    return [paginas]

def extraer_contenido(contenido, objeto, nivel):

    contenido_general = contenido['body']['view']['value']
    soup = BeautifulSoup(contenido_general, 'html.parser')
    texto = soup.get_text()
    
    objeto.pop(nivel)
    objeto["contenido"] = texto
    
    return objeto
   
def verificar_nivel(profundidad):
    if profundidad == 1:
        nivel = 'Clientes'
    elif profundidad >= 2:
        nivel = 'Proyectos'
    else:
        nivel = 'Industrias'
    return nivel

def verificar_nivel_anterior(profundidad):
    if profundidad == 0:
        nivel = 'Cliente'
    elif profundidad >= 1:
        nivel = 'Proyecto'
    else:
        nivel = 'Industria'
    return nivel

def generar_texto_final(contenido, indice):
    if 'contenido' in contenido and contenido['contenido']:
        if 'Proyecto' in contenido:
            info = contenido['Proyecto']
        else:
            info = list(contenido.values())[0]
        parte_contenido = contenido['contenido']
        return f'{info} contiene la siguiente información {parte_contenido} \n'
    
    subindice = indice[:-1]
    indices = ', '.join([d[subindice] for d in contenido[0][indice]])
    
    if indice == 'Industrias':
        indice_principal = contenido[0]['División']
        return f'La empresa Baufest para Comercial cuenta en su cartera con la división *{indice_principal}* y dicha división cuenta con los siguientes industrias: *{indices}* \n'
    elif indice == 'Clientes':
        indice_principal = contenido[0]['Industria']
        return f'La empresa Baufest para Comercial cuenta en su cartera con la industria *{indice_principal}* y dicha industria cuenta con los siguientes clientes: *{indices}* \n'
    else:
        if 'Proyecto' in contenido[0]:
            indice_principal = contenido[0]['Proyecto']
            return f'La empresa Baufest para Comercial cuenta en su cartera con el proyecto *{indice_principal}* y para ese proyecto se cuenta con los siguientes subproyectos: *{indices}* \n'
        else:
            indice_principal = contenido[0]['Cliente']
            return f'La empresa Baufest para Comercial cuenta en su cartera con el cliente *{indice_principal}* y para ese cliente se cuenta con los siguientes proyectos: *{indices}* \n'

def guardar_archivo(contenido, nombre_archivo, indice, nivel):
    if indice in ['Industrias', 'Clientes', 'Proyectos']:
        texto_final = generar_texto_final(contenido, indice)
        print(f"Todo el contenido se ha guardado en '{nombre_archivo}'")
    else:
        parte_contenido = contenido[1]['contenido']
        divisiones = ', '.join([d['División'] for d in contenido[2]['Divisiones']])
        texto_final = f'contenido: {parte_contenido}\n La empresa Baufest para Comercial cuenta con las siguientes divisiones empresariales: {divisiones} \n'
        nombre_archivo = f'textos/{nombre_archivo}'
    
    tipo_archivo = 'w' if nivel == 0 else 'a'
    
    with open(nombre_archivo, tipo_archivo, encoding='utf-8') as archivo:
        archivo.write(texto_final)