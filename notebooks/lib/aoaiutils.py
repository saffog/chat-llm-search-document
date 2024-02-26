# The purpose of this aoaiutils.py is to provide the open ai utilities methods

import openai
import os

AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE")
AZURE_OPENAI_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS")
AZURE_OPENAI_CHAT_COMPLETION_MODEL = os.environ.get("AZURE_OPENAI_CHAT_COMPLETION_MODEL")
AZURE_OPENAI_CHAT_COMPLETION_ENGINE = os.environ.get("AZURE_OPENAI_CHAT_COMPLETION_ENGINE")

def print_required_variables(debug=True):
    if debug:
        print(f"AZURE_OPENAI_RESOURCE: {AZURE_OPENAI_RESOURCE}")
        print(f"AZURE_OPENAI_KEY: {AZURE_OPENAI_KEY}")
        print(f"AZURE_OPENAI_TEMPERATURE: {AZURE_OPENAI_TEMPERATURE}")
        print(f"AZURE_OPENAI_MAX_TOKENS: {AZURE_OPENAI_MAX_TOKENS}")
        print(f"AZURE_OPENAI_CHAT_COMPLETION_MODEL: {AZURE_OPENAI_CHAT_COMPLETION_MODEL}")
        print(f"AZURE_OPENAI_CHAT_COMPLETION_ENGINE: {AZURE_OPENAI_CHAT_COMPLETION_ENGINE}")
    else:
        print(f"No variables to print")

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
