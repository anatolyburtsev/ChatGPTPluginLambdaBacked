import json
import logging
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from gen_ideas import generate_ideas, get_links
from langchain import GoogleSearchAPIWrapper
from langchain.chat_models import ChatOpenAI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
search = GoogleSearchAPIWrapper()


def load_env_vars():
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", region_name=session.region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId="BotCreds")
    except ClientError as e:
        raise Exception("Couldn't retrieve the secret") from e
    else:
        secret = json.loads(get_secret_value_response["SecretString"])
        os.environ["OPENAI_API_KEY"] = secret["OPENAI_API_KEY"]
        os.environ["GOOGLE_CSE_ID"] = secret["GOOGLE_CSE_ID"]
        os.environ["GOOGLE_API_KEY"] = secret["GOOGLE_API_KEY"]


def main1(event, context):
    query = event["query"]
    load_env_vars()
    gift_ideas = generate_ideas(llm, query)
    item_links = [get_links(llm, search, idea) for idea in gift_ideas]
    response = {
        "ideas": [
            {"idea": idea, "items": details}
            for idea, details in zip(gift_ideas, item_links)
        ]
    }
    return response


def main2(event, context):
    return {"body": "Hello world2"}
