from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from core.config import origins


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается")
    yield
    print("Приложение останавливается")


app = FastAPI(lifespan=lifespan)

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
