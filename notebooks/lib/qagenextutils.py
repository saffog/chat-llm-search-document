# The purpose of this qagenextutils.py is to generate the robot responses using open ai extensions utilities methods (aoaiextutils)

import json
import aoaiextutils
import os

from datetime import datetime

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

BAUCHAT_TEMPLATE_USER_MESSAGE = os.environ.get("BAUCHAT_TEMPLATE_USER_MESSAGE","""{user_question}""")
BAUCHAT_DEBUG = os.environ.get("BAUCHAT_DEBUG","")

def print_required_variables(debug=True):
    if debug:
        print(f"BAUCHAT_DEBUG: {BAUCHAT_DEBUG}")       
        print(f"BAUCHAT_TEMPLATE_USER_MESSAGE: {BAUCHAT_TEMPLATE_USER_MESSAGE}")       
    else:
        print("Nothing to print")

def get_chat_completion(question):
    user_message = BAUCHAT_TEMPLATE_USER_MESSAGE.format(user_question=question)
    return aoaiextutils.get_extension_chat_completion(user_message)


def generate_robot_responses_with_chat_completion(filename_to_test,debug=BAUCHAT_DEBUG,printResult=True):
    
    filename_to_read =  f"{filename_to_test}.json"
    with open(filename_to_read,encoding='utf-8') as file_read:
        datos = json.load(file_read)

    results_with_robot_answer = []
    for questions_answers_item in datos["questions_answers"]:
        if questions_answers_item:
            question_to_test = questions_answers_item.get("question")
            if question_to_test:
                 questions_answers_item['robot_answer'] = get_chat_completion(question_to_test)
        if debug: print(questions_answers_item)
        results_with_robot_answer.append(questions_answers_item)
    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Construct the filename with the current date and time
    filename_to_write = f"result_{filename_to_test}_{current_datetime}.json"

    json_data = {
        "template_to_test":BAUCHAT_TEMPLATE_USER_MESSAGE,
        "results":results_with_robot_answer
    }

    json_string = json.dumps(json_data)
    if debug: print(f"filename_to_write: {filename_to_write} result : {aoaiextutils.beautify_json(json_data)}")
        
    if printResult: print(f"{aoaiextutils.beautify_json(json_data)}")

    # Writing the dictionary to a JSON file with the current date and time in the filename
    with open(filename_to_write, 'w') as file_write:
        file_write.write(json_string)