import os
from fastapi import FastAPI
import py_eureka_client.eureka_client as eureka_client

app = FastAPI(title="Order Service")

EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka/")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8002))
SERVICE_NAME = os.getenv("SERVICE_NAME", "order-service")

@app.on_event("startup")
async def startup_event():
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name=SERVICE_NAME,
        instance_port=SERVICE_PORT,
        instance_host=SERVICE_NAME
    )

@app.get("/")
def read_root():
    return {"service": SERVICE_NAME, "status": "active"}

@app.get("/orders")
def get_orders():
    return [{"order_id": 101, "item": "Книга"}, {"order_id": 102, "item": "Навушники"}]