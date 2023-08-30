from fastapi import FastAPI


app = FastAPI(
    title="Learning app",
)


@app.get('/', response_model=list[str])
def hello():
    return ["Hello, world"]