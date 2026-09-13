from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import categories,posts,users,comments







Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Blog API",
    description="REST API for a Blog Management System",
    version="1.0.0"
)
app.include_router(categories.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(comments.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Yeh line file ke bilkul end par paste kar den
app = app 
