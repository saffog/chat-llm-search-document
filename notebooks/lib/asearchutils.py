# The purpose of this asearchutils.py is to provide the Azure search ai utilities methods
import os
import json
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# On Your Data Settings
SEARCH_TOP_K = os.environ.get("SEARCH_TOP_K", 5)
SEARCH_STRICTNESS = os.environ.get("SEARCH_STRICTNESS", 3)

# ACS Integration Settings
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default")
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", SEARCH_TOP_K)
AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")
AZURE_SEARCH_VECTOR_COLUMNS = os.environ.get("AZURE_SEARCH_VECTOR_COLUMNS")
AZURE_SEARCH_QUERY_TYPE = os.environ.get("AZURE_SEARCH_QUERY_TYPE")

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
    else:
        print(f"No variables to print")


def process_as_json_search_results(results):
    json_list = [json.dumps({"title": doc[AZURE_SEARCH_TITLE_COLUMN], "url": doc[AZURE_SEARCH_URL_COLUMN], "content": doc[AZURE_SEARCH_CONTENT_COLUMNS].replace("\n", "").replace("\r", ""), "filename": doc[AZURE_SEARCH_FILENAME_COLUMN]}) for doc in results]
    merged_string = "["+",\n".join(json_list)+"]"
    return merged_string


def get_azure_search_by_query(user_query,debug=False,resultAsJson=True):
    service_endpoint = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"
    index_name = f"{AZURE_SEARCH_INDEX}"
    key = f"{AZURE_SEARCH_KEY}"
    credential = AzureKeyCredential(key)
    client = SearchClient(service_endpoint, index_name, credential)
    
    if debug: print(f"get_azure_search_by_query : user_query : {user_query}")
    results = client.search(
        search_text=user_query,
        query_type=AZURE_SEARCH_QUERY_TYPE,
        semantic_configuration_name=AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG,
        top=AZURE_SEARCH_TOP_K
        )
    if resultAsJson:
        return process_as_json_search_results(results)
    else:
        return results
