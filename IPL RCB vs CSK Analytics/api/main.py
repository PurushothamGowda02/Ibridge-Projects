from fastapi import FastAPI
from api.routes.analytics import router as analytics_router

app = FastAPI(
    title="RCB vs CSK IPL Analytics API",
    version="1.0.0",
    description="Head-to-head analytics for IPL matches between RCB and CSK from 2008 onward.",
)

app.include_router(analytics_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "RCB vs CSK IPL Analytics API is running"}
