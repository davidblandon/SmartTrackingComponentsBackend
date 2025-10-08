from fastapi import FastAPI
from routes.component import router
import uvicorn

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello HTTPS!"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",             
        host="0.0.0.0",
        port=443,               
        ssl_certfile="C:\\certs\\cert.pem",
        ssl_keyfile="C:\\certs\\key.pem"
    )

