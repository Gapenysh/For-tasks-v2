from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from database import origins
from users.view import router as users_router
from tasks.view import router as tasks_router

app = FastAPI(echo=False)
app.include_router(users_router, tags=["Users"])
app.include_router(tasks_router, tags=["Tasks"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_index():
    return {"message": "Hello index!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.3", port=9000, reload=True)
