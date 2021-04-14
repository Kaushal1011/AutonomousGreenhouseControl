import numpy as np
from fastapi import FastAPI

from app.server.models.agent import enviorenment_endpoint

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

@app.post("/predict")
def predict(body: enviorenment_endpoint):
    data = np.array(body.to_array())

    probas = clf.predict_proba(data)
    predictions = probas.argmax(axis=1)

    return {
        "predictions": (
            np.tile(clf.classes_, (len(predictions), 1))[
                np.arange(len(predictions)), predictions
            ].tolist()
        ),
        "probabilities": probas[np.arange(len(predictions)), predictions].tolist(),
    }