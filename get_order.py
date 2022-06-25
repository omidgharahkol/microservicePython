import uvicorn
from fastapi import FastAPI, Response, status
import json

import pika

app = FastAPI()




@app.get("/order/{username}")
def get_order(username: str, order_type: str, name: str, response: Response):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    if order_type in ["books", "cloths"]:
        info = {"username": username, "group": order_type, "product": name}
        channel.queue_declare(queue="order")
        channel.basic_publish(exchange='', routing_key='order', body=json.dumps(info))
        print("message sent")
        connection.close()
        response.status_code = status.HTTP_200_OK
        return {
            "status_code": response.status_code,
            "result":"The order was registered"}

    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"status_code": response,
                "result": "the order group doesn't exist"}


if __name__ == "__main__":
    uvicorn.run(app, port=4000)
