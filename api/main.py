from fastapi import FastAPI

app = FastAPI()


@app.get("/{name}")
def read_root(name):
    return {"message": f"Hello, {name}?"}
