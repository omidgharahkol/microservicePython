import uvicorn
from fastapi import FastAPI, Response, status
import json

import pika

app = FastAPI()

connection = pika.BlockingConnection()
channel = connection.channel()


@app.get("/process")
def process_order(response: Response):
    method, header, body = channel.basic_get(queue='order')
    response.status_code = status.HTTP_200_OK
    if method:
        return {
            "status_code": response.status_code,
            "order_detail": json.loads(body)}
    else:
        return {
            "status_code": response.status_code,
            "order_detail": "no order doesn't exist"}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=6000)
