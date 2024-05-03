import uuid

from fastapi import FastAPI, Request, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from api.config_parser import ConfigParser
from api.chat_service import ChatGptService
from api.create_openai_client import get_client
import traceback

import boto3


# class RequestModel(BaseModel):
#     request: dict

SESSION = boto3.Session(profile_name="viswa-admin", region_name="us-east-1")
CHAT_GPT_KEY = ConfigParser(session=SESSION).load_config(
    parameter_name="/hoabot/chatgpt/apikey"
)
OPEN_AI_CLIENT = get_client(openai_key=CHAT_GPT_KEY)


app = FastAPI()
# lambda_handler = Mangum(app) #doesnot work in local machine , use app instead


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
        response = ChatGptService.get_completion(
            client=OPEN_AI_CLIENT, prompt=user_message
        )

    except:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"response": response, "status_code": 200}
