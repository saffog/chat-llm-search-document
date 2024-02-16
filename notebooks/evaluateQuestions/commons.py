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
