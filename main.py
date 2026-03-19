import uvicorn
from fastapi import FastAPI, WebSocket
from payloads import SpamCheckRequest
from env import config
from llm_ops import OpenAISPAMCheck


app = FastAPI()

@app.post("/spam_check")
async def spam_check(spam_check_request: SpamCheckRequest):
    spam_check = OpenAISPAMCheck(config.api_key).spam_check
    response = spam_check(spam_check_request.mail_text, spam_check_request.additional_context)
    
    return {response}

@app.websocket("/spam_describe")
async def spam_describe(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        spam_stream_describe = OpenAISPAMCheck(config.api_key).spam_stream_describe
        
        for event in spam_stream_describe(data):
            if hasattr(event, 'delta'):
                await ws.send_text(event.delta)

if __name__ == "__main__":
    spam_stream_describe = OpenAISPAMCheck(config.api_key).spam_stream_describe
    
    uvicorn.run(app, host=config.hostname, port=9804)
