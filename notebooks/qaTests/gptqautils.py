# The purpose of gptqautils.py is to provide utilities functions to help to evaluate model completions against human completions

import openai
import os
import json

AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE")
AZURE_OPENAI_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS")
AZURE_OPENAI_CHAT_COMPLETION_MODEL = os.environ.get("AZURE_OPENAI_CHAT_COMPLETION_MODEL")
AZURE_OPENAI_CHAT_COMPLETION_ENGINE = os.environ.get("AZURE_OPENAI_CHAT_COMPLETION_ENGINE")

openai.api_key  = AZURE_OPENAI_KEY
openai.api_type = "azure"
openai.api_version = "2023-08-01-preview"
openai.api_base = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"    

def get_completion(input_prompt, 
                   debug = False, 
                   returnWholeObject = False):
    if debug: print(f"get_completion : input_prompt : {input_prompt}")
    completion = openai.Completion.create(
        prompt=input_prompt, 
        model=AZURE_OPENAI_CHAT_COMPLETION_MODEL,
        engine=AZURE_OPENAI_CHAT_COMPLETION_ENGINE, 
        temperature=float(AZURE_OPENAI_TEMPERATURE), 
        max_tokens=int(AZURE_OPENAI_MAX_TOKENS), 
        stop=["<|im_end|>", "<|im_start|>"])

    if debug: print(f"get_completion : completion : {completion}")
        
    if returnWholeObject:
        return completion
    else:
        return completion["choices"][0]["text"]

def transform_open_ai_compare_to_json(input_string, debug=False):
    data = []
    if debug: print(f"transform_open_ai_compare_to_json : input to process : {input_string}")
    parts = input_string.replace("\n", "").replace("\r", "").split("Question-")
    if debug: print(f"parts : {parts}")
    for i, part in enumerate(parts, start=1):
        if part:
            info = part.split("--")
            if debug: print(f"transform_open_ai_compare_to_json : i: {i} part: {part} info: {info}")
            test_id = info[0]
            test = info[1]
            result = 1 if info[2] == "YES" else 0
            reason = info[3]
            item = {
                "test_id": test_id,
                "test": test,
                "result": result,
                "reason": reason
            }
            if debug: print(f"transform_open_ai_compare_to_json : Item to add : {item}")
            data.append(item)
    if debug: print(f"transform_open_ai_compare_to_json : data to json : {data}")
    return json.dumps(data, indent=2)

def evaluate_responses(robot_answer, human_answer, debug=False):
    qa_guidelines = """<|im_start|>user
    Compare the robot response versus human response. The robot response is delimited by ###ROBOT### and 
    the human response is delimited by ###HUMAN###.
    Answer the next questions:
    Question-1 : Is the robot's response correct?
    Question-2 : Is the robot's response similar to the human answer?
    For your responses follow the next format:
    Question-1--Correctness--YES or NO--Summarize your arguments in 10 words
    Question-2--Similarity--YES or NO--Summarize your arguments in 10 words
    
    ###ROBOT###
    {robot_response}
    ###ROBOT###
    
    ###HUMAN###
    {human_response}
    ###HUMAN###
    <|im_end|>"""
    assistant_prompt = """<|im_start|>assistant"""
    prompt = qa_guidelines.format(robot_response=robot_answer, human_response=human_answer) + assistant_prompt
    if debug: print(f"evaluate_responses : prompt : {prompt}")
    
    completion = get_completion(input_prompt=prompt,debug=debug)
    result_as_json = transform_open_ai_compare_to_json(input_string=completion,debug=debug)
    if debug: print(f"evaluate_responses : result : {result_as_json}") 
    return result_as_json
    
def evaluate_query_responses(user_query, robot_answer, human_answer, debug=False):
    qa_guidelines = """<|im_start|>user
    Evaluate the robot response against the query.
    Evaluate the human response against the query.
    Compare the robot response versus human response.
    The query is delimited by ###QUERY###.
    The robot response is delimited by ###ROBOT###. 
    The human response is delimited by ###HUMAN###.
    Answer the next questions:
    Question-1 : Is the robot's response similar to the human answer?
    Question-2 : Is the robot's response correct?
    Question-3 : Is the human's response correct?
    For your responses follow the next format:
    Question-1--Similarity--YES or NO--Summarize your arguments in 10 words
    Question-2--Robot Correctness--YES or NO--Summarize your arguments in 10 words
    Question-3--Human Correctness--YES or NO--Summarize your arguments in 10 words

    ###QUERY###
    {query}
    ###QUERY###

    ###ROBOT###
    {robot_response}
    ###ROBOT###
    
    ###HUMAN###
    {human_response}
    ###HUMAN###
    <|im_end|>"""
    assistant_prompt = """<|im_start|>assistant"""
    prompt = qa_guidelines.format(robot_response=robot_answer, human_response=human_answer,query=user_query) + assistant_prompt
    if debug: print(f"evaluate_query_responses : prompt : {prompt}")
    
    completion = get_completion(input_prompt=prompt,debug=debug)
    result_as_json = transform_open_ai_compare_to_json(input_string=completion,debug=debug)
    if debug: print(f"evaluate_query_responses : result : {result_as_json}") 
    return result_as_json
