from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.routes.incidents import router as incidents_router

from app.dependencies import get_db

app = FastAPI()


@app.get("/health")
def health(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }

app.include_router(incidents_router)