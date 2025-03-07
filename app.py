from fastapi import FastAPI
from chainlit.utils import mount_chainlit

app = FastAPI()


@app.get("/")
def read_main():
    return {"message": "Hello World from FastAPI app"}


mount_chainlit(app=app, target="ashwini_mitra.py", path="/ashwini-mitra")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
