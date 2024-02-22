# The purpose of this commons.py is to provide the common used methods, imports and other useful functions

import os
import openai # this will require pip install openai
import tiktoken # this will require pip install tiktoken
import requests
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# On Your Data Settings
DATASOURCE_TYPE = os.environ.get("DATASOURCE_TYPE", "AzureCognitiveSearch")
SEARCH_TOP_K = os.environ.get("SEARCH_TOP_K", 5)
SEARCH_STRICTNESS = os.environ.get("SEARCH_STRICTNESS", 3)
SEARCH_ENABLE_IN_DOMAIN = os.environ.get("SEARCH_ENABLE_IN_DOMAIN", "true")

# ACS Integration Settings
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.environ.get("AZURE_SEARCH_USE_SEMANTIC_SEARCH", "false")
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default")
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", SEARCH_TOP_K)
AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get("AZURE_SEARCH_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN)
AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")
AZURE_SEARCH_VECTOR_COLUMNS = os.environ.get("AZURE_SEARCH_VECTOR_COLUMNS")
AZURE_SEARCH_QUERY_TYPE = os.environ.get("AZURE_SEARCH_QUERY_TYPE")
AZURE_SEARCH_PERMITTED_GROUPS_COLUMN = os.environ.get("AZURE_SEARCH_PERMITTED_GROUPS_COLUMN")
AZURE_SEARCH_STRICTNESS = os.environ.get("AZURE_SEARCH_STRICTNESS", SEARCH_STRICTNESS)

# AOAI
AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
AZURE_OPENAI_SYSTEM_MESSAGE = os.environ.get("AZURE_OPENAI_SYSTEM_MESSAGE", "You are an AI assistant that helps people find information.")

AZURE_OPENAI_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS")
AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE")
AZURE_OPENAI_CHAT_COMPLETION_MODEL = os.environ.get("AZURE_OPENAI_CHAT_COMPLETION_MODEL")
AZURE_OPENAI_CHAT_COMPLETION_ENGINE = os.environ.get("AZURE_OPENAI_CHAT_COMPLETION_ENGINE")

openai.api_key  = AZURE_OPENAI_KEY
openai.api_type = "azure"
openai.api_version = "2023-08-01-preview"
openai.api_base = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"

def print_required_variables(debug=True):
    if debug:
        print(f"AZURE_SEARCH_SERVICE: {AZURE_SEARCH_SERVICE}")
        print(f"AZURE_SEARCH_INDEX: {AZURE_SEARCH_INDEX}")
        print(f"AZURE_SEARCH_KEY: {AZURE_SEARCH_KEY}")
        print(f"AZURE_SEARCH_USE_SEMANTIC_SEARCH: {AZURE_SEARCH_USE_SEMANTIC_SEARCH}")
        print(f"AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG: {AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG}")
        print(f"AZURE_SEARCH_TOP_K: {AZURE_SEARCH_TOP_K}")
        print(f"AZURE_SEARCH_ENABLE_IN_DOMAIN: {AZURE_SEARCH_ENABLE_IN_DOMAIN}")
        print(f"AZURE_SEARCH_CONTENT_COLUMNS: {AZURE_SEARCH_CONTENT_COLUMNS}")
        print(f"AZURE_SEARCH_FILENAME_COLUMN: {AZURE_SEARCH_FILENAME_COLUMN}")
        print(f"AZURE_SEARCH_TITLE_COLUMN: {AZURE_SEARCH_TITLE_COLUMN}")
        print(f"AZURE_SEARCH_URL_COLUMN: {AZURE_SEARCH_URL_COLUMN}")
        print(f"AZURE_SEARCH_VECTOR_COLUMNS: {AZURE_SEARCH_VECTOR_COLUMNS}")
        print(f"AZURE_SEARCH_QUERY_TYPE: {AZURE_SEARCH_QUERY_TYPE}")
        print(f"AZURE_SEARCH_PERMITTED_GROUPS_COLUMN: {AZURE_SEARCH_PERMITTED_GROUPS_COLUMN}")
        print(f"AZURE_SEARCH_STRICTNESS: {AZURE_SEARCH_STRICTNESS}")
        print(f"AZURE_OPENAI_RESOURCE: {AZURE_OPENAI_RESOURCE}")
        print(f"AZURE_OPENAI_KEY: {AZURE_OPENAI_KEY}")
        print(f"AZURE_OPENAI_MODEL: {AZURE_OPENAI_MODEL}")
        print(f"AZURE_OPENAI_SYSTEM_MESSAGE: {AZURE_OPENAI_SYSTEM_MESSAGE}")
    else:
        print(f"No variables to print")

def beautify_json(json_to_process): 
    return json.dumps(json_to_process, indent=4)

def get_completion_from_messages(messages,
                                 ds_role_value="",
                                 debug=False,
                                 show_completion=False,
                                 show_input=True,
                                 return_completion=False) :
    if debug:
        print_required_variables(debug)
        print(f"messages: {messages}")
    
    def setup_byod(deployment_id: str) -> None:
        """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.
        :param deployment_id: The deployment ID for the model to use with your own data.
        To remove this configuration, simply set openai.requestssession to None.
        """

        class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

            def send(self, request, **kwargs):
                request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
                return super().send(request, **kwargs)

        session = requests.Session()

        # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
        session.mount(
            prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
            adapter=BringYourOwnDataAdapter()
        )
        
        openai.requestssession = session

    if ds_role_value == "" :
        ds_role_value = AZURE_OPENAI_SYSTEM_MESSAGE
        
    setup_byod(AZURE_OPENAI_MODEL)
    search_endpoint = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"
    
    if show_input:
        print(f"Data source role information : {ds_role_value}")
        print(f"messages : {beautify_json(messages)}")
    
    completion = openai.ChatCompletion.create(
        messages=messages,
        deployment_id=AZURE_OPENAI_MODEL,
        dataSources=[  # camelCase is intentional, as this is the format the API expects
            {
                "type": DATASOURCE_TYPE,
                "parameters": {
                    "endpoint": search_endpoint,
                    "key": AZURE_SEARCH_KEY,
                    "indexName": AZURE_SEARCH_INDEX,
                    "fieldsMapping": {
                        "contentFields": AZURE_SEARCH_CONTENT_COLUMNS.split("|") if AZURE_SEARCH_CONTENT_COLUMNS else [],
                        "titleField": AZURE_SEARCH_TITLE_COLUMN if AZURE_SEARCH_TITLE_COLUMN else None,
                        "urlField": AZURE_SEARCH_URL_COLUMN if AZURE_SEARCH_URL_COLUMN else None,
                        "filepathField": AZURE_SEARCH_FILENAME_COLUMN if AZURE_SEARCH_FILENAME_COLUMN else None,
                        "vectorFields": AZURE_SEARCH_VECTOR_COLUMNS.split("|") if AZURE_SEARCH_VECTOR_COLUMNS else []
                    },
                    "inScope": True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
                    "topNDocuments": AZURE_SEARCH_TOP_K,
                    "queryType": AZURE_SEARCH_QUERY_TYPE,
                    "semanticConfiguration": AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG if AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG else "",
                    "roleInformation": ds_role_value,
                    "strictness": int(AZURE_SEARCH_STRICTNESS)
                }
            }
        ]
    )

    if show_completion:
        print(completion)
        
    if return_completion:
        return completion

    return completion.choices[0].message["content"]

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