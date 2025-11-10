from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Gateway", version="1.0.0")

# CORS настройки для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:4001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs микросервисов
USERS_SERVICE_URL = "http://service_users:8001"
ORDERS_SERVICE_URL = "http://service_orders:8002"

@app.get("/")
async def root():
    return {"message": "API Gateway is running", "status": "healthy"}

@app.post("/v1/auth/{path:path}")
async def auth_proxy(path: str, request: Request):
    """Проксирование запросов аутентификации в сервис пользователей"""
    try:
        async with httpx.AsyncClient() as client:
            body = await request.json()
            response = await client.post(
                f"{USERS_SERVICE_URL}/v1/auth/{path}",
                json=body,
                headers=dict(request.headers)
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code
            )
    except Exception as e:
        logger.error(f"Auth proxy error: {e}")
        raise HTTPException(status_code=500, detail="Service unavailable")

@app.get("/v1/orders")
@app.post("/v1/orders")
async def orders_proxy(request: Request):
    """Проксирование запросов заказов в сервис заказов"""
    try:
        async with httpx.AsyncClient() as client:
            if request.method == "GET":
                response = await client.get(
                    f"{ORDERS_SERVICE_URL}/v1/orders",
                    headers=dict(request.headers)
                )
            else:
                body = await request.json()
                response = await client.post(
                    f"{ORDERS_SERVICE_URL}/v1/orders",
                    json=body,
                    headers=dict(request.headers)
                )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code
            )
    except Exception as e:
        logger.error(f"Orders proxy error: {e}")
        raise HTTPException(status_code=500, detail="Service unavailable")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)