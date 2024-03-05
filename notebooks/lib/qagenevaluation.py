# The purpose of qagenevaluation.py is to evaluate the responses using open ai through qaoaievalutils
import qaoaievalutils
import qasmevalutils
import json
from datetime import datetime

def evaluate_responses(filename_to_eval,
                       response_a_field,
                       response_b_field,
                       debug=False, 
                       printResult=False,
                       filename_result="",
                       includeSMEval=False):
    
    filename_to_read =  f"{filename_to_eval}"
    with open(filename_to_read,encoding='utf-8') as file_read:
        datos = json.load(file_read)
        
    results_with_evaluation = []
    for questions_answers_item in datos["questions_answers"]:
        if questions_answers_item:
            question_to_eval = questions_answers_item.get("question")
            response_a_to_eval = questions_answers_item.get(response_a_field)
            response_b_to_eval = questions_answers_item.get(response_b_field)
            if question_to_eval and response_a_to_eval and response_b_to_eval:
                questions_answers_item['response_a'] = response_a_field
                questions_answers_item['response_b'] = response_b_field                
                questions_answers_item['evaluate_with_AOAI_result'] = qaoaievalutils.evaluate_query_better_response(user_query=question_to_eval,response_a=response_a_to_eval,response_b=response_b_to_eval,debug=debug)
                if includeSMEval:
                    questions_answers_item['evaluate_with_SM_result'] = qasmevalutils.sm_matching_test(response_a_to_eval, response_b_to_eval, debug=debug)
            if debug: print(questions_answers_item)
            results_with_evaluation.append(questions_answers_item)
    
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Extract templates
    used_templates = datos["used_templates"]

    if filename_result:
        filename_to_write=filename_result
    else:
        # Construct the filename with the current date and time
        filename_to_write = f"result_{filename_to_eval}_{current_datetime}.json"

    json_data = {
        "used_templates": used_templates,
        "questions_answers":results_with_evaluation
    }

    json_string = json.dumps(json_data)
    if debug: print(f"filename_to_write: {filename_to_write} result : {json_string}")
        
    if printResult: print(f"{json_data}")

    # Writing the dictionary to a JSON file with the current date and time in the filename
    with open(filename_to_write, 'w') as file_write:
        file_write.write(json_string)
    
    return filename_to_write
