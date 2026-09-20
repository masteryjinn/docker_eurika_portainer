import os
from fastapi import FastAPI
import py_eureka_client.eureka_client as eureka_client

app = FastAPI(title="User Service")

EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka/")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8001))
SERVICE_NAME = os.getenv("SERVICE_NAME", "user-service")

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

@app.get("/users")
def get_users():
    return [{"id": 1, "name": "Ірина"}, {"id": 2, "name": "Олександр"}]