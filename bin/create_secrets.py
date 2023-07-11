import json

import boto3

secretsmanager = boto3.client("secretsmanager")

secret_name = "BotCreds"
secret_values = {
    "OPENAI_API_KEY": "FILL_ME",
    "GOOGLE_CSE_ID": "FILL_ME",
    "GOOGLE_API_KEY": "FILL_ME",
}

response = secretsmanager.create_secret(
    Name=secret_name, SecretString=json.dumps(secret_values)
)

print(response)
