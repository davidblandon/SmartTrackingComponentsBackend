from fastapi import FastAPI
from routes.component import router
import uvicorn
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPONENT_PHOTOS_DIR = os.path.join(BASE_DIR, "static", "components_photos")
app.mount("/components_photos", StaticFiles(directory=COMPONENT_PHOTOS_DIR), name="components_photos")

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

