# Azure Function Managed Identity Auth for Event Hub
[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://azurefunc-eventhub-managedidentity-auth.remote-containers/cloneInVolume?https://github.com/rajkalemsft/azurefunc-eventhub-managedidentity-auth)

Sample Azure Function to demonstrate ability to connect to Azure EventHub with Kafka protocol. Provides way to use client credentials Vs managed identity auth.

**Sample demonstrates**, 
1. Different authentication mechanisms for EventHub using AzureAD. 
2. Code uses VSCode devcontainer feature to run locally in an isolated environment.
3. Has docker image definition to build the image

**Sample relies on below packages**,

Azure.Identity -> For Azure AD AUTH. Please refer [defaultazurecredential](https://docs.microsoft.com/en-us/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet)

Confluent-Kafka -> To connect to EventHub using Kafka protocol

**To get going**, add below configurations to your local.settings.json or azure function configurations,

    "AZURE_AUTHORITY_HOST":"login.microsoftonline.com",
    "AZURE_CLIENT_ID":"<<AppClientIdForClientCredsAuthFlow-NotRequiredForManagedIdentityAuth>>",
    "AZURE_CLIENT_SECRET":"<<AppSecretForClientCredsAuthFlow-NotRequiredForManagedIdentityAuth>>",
    "AZURE_TENANT_ID":"<<TenantID>>",
    "EVENT_HUB_HOSTNAME":"<<EVentHubNameSpace>>",
    "EVENT_HUB_NAME":"<<EventHubName>>",
    "CONSUMER_GROUP":"<<EventHubConsumerGroupName-Typically $Default>>"
    
**To test locally**, execute azure function with azure func cli command func start on terminal window. 

**To Deploy to Azure**
1. Build the container and publish to Azure Container Registry (ACR)
    docker build -t <<ACRName>>.azurecr.io/<<RepoName>>:<<Tag>> .
  
    az login
    az acr login <<ACRName>>
  
   docker push <<ACRName>>.azurecr.io/<<RepoName>>:<<Tag>> 
  
2. Configure azure function to deploy from ACR
  
   <img width="764" alt="image" src="https://user-images.githubusercontent.com/106317605/173991147-62ac842a-f985-476b-af55-6c3f30d58cdb.png">
3. Provision EventHub RBAC role.
  1. To use ClientCreds auth flow, register an AzureAD App, create client secret and add it to configurations as mentioned above.
  2. To use ManagedIdentity authentication, create a system or user assigned identity for the azure function.
  
  Based on the above approach, provision EventHub Sender role for the Service Principal.
  
