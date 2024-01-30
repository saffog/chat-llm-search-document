# Building Block Code for web app chat that uses Azure Open AI LLM and Azure Search to provide relevant data from documents 


> This project is based on the next project: 

## Project Structure

```
\
app.py       --> Holds all the logic related to Azure Open AI consumption and responses for the frontend
++ backend   --> Holds logic related to Cosmos DB & authentication
++ frontend  --> Holds the visual chat 
```

## To run this project locally

1. Ensure you setup all the required environment values
2. Execute in powershell `start.cmd`

The app should display here: http://127.0.0.1:5000

## To run jupyter notebooks locally

As prerequisit ensure you installed [Anaconda](https://www.anaconda.com/download/) before

1. `cd \notebooks`
2. `pip install jupyterlab`
3. `jupyter notebook`

## To deploy this project to an existing resource

Prerequisites: 

- Ensure you have installed [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- Login to your Azure account using `az login` 

Check the prerequisites above.

1. Build the app code with `start.cmd` or `start.sh` before you deploy, otherwise your changes will not be picked up.
2. Setup to allow deployment from local: `az webapp config appsettings set -g <resource-group-name> -n <existing-app-name> --settings WEBSITE_WEBDEPLOY_USE_SCM=false`
3. Deploy APP: `az webapp up --runtime <runtime-stack> --sku <sku> --name <existing-app-name> --resource-group <resource-group-name>`
   1. For this project is enough to deploy app: `az webapp up --name <existing-app-name> --resource-group <resource-group-name>`.
   2. Review as well the config file at: __.azure\config__ since it that file there are default values, so you will need to adjust values if deployment web app is different than the first deployment



### Setup environment values

To setup variables use the next:

```
$Env:AZURE_OPENAI_RESOURCE = <required value>

# For example:

$Env:AZURE_OPENAI_RESOURCE = 'cog-whatever'

# if you want to list the environment variables you can use

Get-ChildItem Env: | Format-Table -AutoSize

```

Required environment variables: 

- Azure Open AI
  - `$Env:AZURE_OPENAI_RESOURCE` 
  - `$Env:AZURE_OPENAI_MODEL` 
  - `$Env:AZURE_OPENAI_KEY`
  - `$Env:AZURE_OPENAI_MODEL_NAME`
  - `$Env:AZURE_OPENAI_TEMPERATURE`

- Azure Search
  - `$Env:AZURE_SEARCH_SERVICE`
  - `$Env:AZURE_SEARCH_INDEX`
  - `$Env:AZURE_SEARCH_KEY`
  - `$Env:AZURE_SEARCH_USE_SEMANTIC_SEARCH`
  - `$Env:AZURE_SEARCH_QUERY_TYPE`
  - `$Env:AZURE_SEARCH_ENABLE_IN_DOMAIN`
  - `$Env:AZURE_SEARCH_STRICTNESS`
  - `$Env:AZURE_SEARCH_CONTENT_COLUMNS`
  - `$Env:AZURE_SEARCH_FILENAME_COLUMN`
  - `$Env:AZURE_SEARCH_TITLE_COLUMN`
  - `$Env:AZURE_SEARCH_URL_COLUMN`

- Other
  - `$Env:DATASOURCE_TYPE`
  - `$Env:DEBUG`

### Deployment known issues

#### 1. An attempt was made to access a socket in a way forbidden by its access permissions

To solve this search for the process that uses port 5000 and kill the process:

```pwsh
netstat -ano | findstr :5000
# System will return something like:
#  TCP    127.0.0.1:5000         0.0.0.0:0   LISTENING       4400
#  TCP    [::1]:5000             [::]:0      LISTENING       4400
# Then we can use taskkill or open Task manager
taskkill /PID 4400
```

#### 2. localhos:5000 shows a message asking for Authentication
To solve this issue simply change **localhost** for **127.0.0.1** 
