from fastapi import FastAPI
from .routers import proxy, dolphin, automation

app = FastAPI()

app.include_router(proxy.router, prefix="/proxy", tags=["proxy"])
app.include_router(dolphin.router, prefix="/dolphin", tags=["dolphin"])
app.include_router(automation.router, prefix="/automation", tags=["automation"])

@app.get("/")
def read_root():
    return {"message": "Amazon Automator API is running"}
