import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import model_loader
from .dependencies.config import conf
from .routers import orders, order_details, menu_items

app = FastAPI()

app.include_router(orders.router)
app.include_router(order_details.router)
app.include_router(menu_items.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)