import os
import pickle
from typing import Annotated

import numpy as np
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

PORT = 9000
HOST = "127.0.0.1"

app = FastAPI()
model = pickle.load(open("model.pkl", "rb"))
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Item(BaseModel):
    like: int
    forward: int


@app.get("/predict", response_class=HTMLResponse)
async def show(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
async def predict_num(
    request: Request, like: Annotated[int, Form()], forward: Annotated[int, Form()]
):
    features = [like, forward]
    label = [np.array(features)]

    prediction = model.predict(label)

    output = round(prediction[0], 2)

    content = {
        "request": request,
        "prediction_text": f"浏览量 $ {output}",
        "predict_url": f"http://{HOST}:{PORT}/predict",
    }
    return templates.TemplateResponse("index.html", content)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
