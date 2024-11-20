from fastapi import FastAPI
from routers import api_router
from sberai_settings import ai_client


app = FastAPI(
    title="Analyzer Service",
    description="Created by Toporov Denis",
)

app.include_router(router=api_router)


@app.on_event("startup")
async def startup_event():
    await ai_client.authorization()
