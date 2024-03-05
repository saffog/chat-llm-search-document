# The purpose of qagraphutils.py is to provide bar graphics and other tools to visualize evaluations
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

def extract_data_for_bar(json_data, target_test_id):
    df = pd.DataFrame(json_data["questions_answers"])
    if df.empty: 
        
        print(f"There is no data for 'questions_answers'")
    if df['evaluate_with_AOAI_result'].empty:
        print(f"There is no data for 'evaluate_with_AOAI_result'")
        
    x_values = df['id_question']
    y_values_str = df['evaluate_with_AOAI_result'].apply(lambda x: next(item['result'] for item in x if item['test_id'] == target_test_id))
    labels = df['evaluate_with_AOAI_result'].apply(lambda x: next(item['test'] for item in x if item['test_id'] == target_test_id))
    
    y_values = pd.to_numeric(y_values_str, errors='coerce').astype(int)
    
    return {
        'categories':x_values, 
        'series':y_values, 
        'label':labels.iloc[0], 
        'response_a':df['response_a'].iloc[0], 
        'response_b':df['response_b'].iloc[0]
    }

def show_plot_similarity_correctnes_score(json_data):
    
    similarity_data = extract_data_for_bar(json_data, target_test_id="1")
    correctness_a = extract_data_for_bar(json_data, target_test_id="2")
    correctness_b = extract_data_for_bar(json_data, target_test_id="3")
    score_a = extract_data_for_bar(json_data, target_test_id="5")
    score_b = extract_data_for_bar(json_data, target_test_id="6")
    
    categories = similarity_data['categories']
    series_A = similarity_data['series']
    series_B = correctness_a['series']
    series_C = correctness_b['series']
    series_D = np.array(score_a['series'])/10
    series_E = np.array(score_b['series'])/10
    
    # Crear la gráfica de barras
    bar_width = 0.15
    index = np.arange(len(categories))
    
    fig, ax = plt.subplots()
    bar_A = ax.bar(index, series_A, bar_width, label=f"{similarity_data['label']}", color='blue')
    bar_B = ax.bar(index + bar_width, series_B, bar_width, label=f"{correctness_a['label']}", color='orange')
    bar_C = ax.bar(index + 2 * bar_width, series_C, bar_width, label=f"{correctness_b['label']}", color='green')
    bar_D = ax.bar(index + 3 * bar_width, series_D, bar_width, label=f"{score_a['label']}", color='red')
    bar_E = ax.bar(index + 4 * bar_width, series_E, bar_width, label=f"{score_b['label']}", color='purple')
    
    # Configurar etiquetas y título
    ax.set_xlabel('Preguntas')
    ax.set_ylabel('Evaluación')
    ax.set_title(f"A: {similarity_data['response_a']} vs B: {similarity_data['response_b']}")
    ax.set_xticks(index + 2 * bar_width)
    ax.set_xticklabels(categories)
    ax.legend()

    # Mostrar la gráfica
    plt.show()
    
def show_evaluate_responses_as_bar_graph(filename_to_eval, debug=False):
    
    filename_to_read =  f"{filename_to_eval}"
    with open(filename_to_read,encoding='utf-8') as file_read:
        datos = json.load(file_read)
    show_plot_similarity_correctnes_score(datos)

       

