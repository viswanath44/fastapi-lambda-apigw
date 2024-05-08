import uuid

from fastapi import FastAPI, Request, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from api.config_parser import ConfigParser
from api.chat_service import ChatService
from api.create_client import get_grok_client
import traceback

import boto3


# SESSION = boto3.Session(
#     profile_name="viswa-admin", region_name="us-east-1"
# )  # for local machine
SESSION = boto3.Session(region_name="us-east-1")  # lambda doesnt recognize profiles


# #openai client
# KEY = ConfigParser(session=SESSION).load_config(
#     parameter_name="/hoabot/chatgpt/apikey"
# )
# CLIENT = get_openai_client(api_key=CHAT_GPT_KEY)


# groq_client
KEY = ConfigParser(session=SESSION).load_config(parameter_name="/hoabot/groq/apikey")
CLIENT = get_grok_client(api_key=KEY)


app = FastAPI()
lambda_handler = Mangum(app)  # doesnot work in local machine , use app instead


@app.get("/random_id_generator")
async def root():
    return {"id": uuid.uuid4()}


@app.post("/chat")
async def chat(request: Request):

    # request ->>{"headers", "body":""}
    # {"message":"Hi, How are you?"} - sample body
    body = await request.json()
    user_message = body.get("message")
    if not user_message:
        raise HTTPException(
            status_code=400,
            detail='No message provided, please provide in this format {"message":"HI, how  are you?"}',
        )
    try:
        response = ChatService.get_groq_completion(client=CLIENT, prompt=user_message)

    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"response": response, "status_code": 200}
