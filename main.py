from fastapi import FastAPI
from routes.component import router as component_router
from routes.user import router as user_router
import uvicorn
import os
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Component Tracking")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173", "https://192.168.1.180:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPONENT_PHOTOS_DIR = os.path.join(BASE_DIR, "static", "components_photos")
app.mount("/components_photos", StaticFiles(directory=COMPONENT_PHOTOS_DIR), name="components_photos")

app = FastAPI()

app.include_router(component_router, prefix="/component", tags=["component"])
app.include_router(user_router, prefix="/user", tags=["user"])

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

