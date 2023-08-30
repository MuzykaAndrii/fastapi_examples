from fastapi import FastAPI


app = FastAPI(
    title="Learning app",
)


@app.get('/')
def hello():
    return "Hello, world"