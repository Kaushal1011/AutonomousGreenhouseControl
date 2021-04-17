from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.models.agent import agent_endpoint, environment_endpoint, ResponseModel, teamnindex_endpoint
from server.AGCRLEnv import AGCRLEnv
import numpy as np
import tensorflow
import pickle

app = APIRouter()

with open('./server/observations.pickle', 'rb') as handle:
    obs = pickle.load(handle)
with open('./server/actions.pickle', 'rb') as handle:
    actions = pickle.load(handle)

theat_rl_actionspace = np.linspace(0, 25, 26)
env_heat = AGCRLEnv(obs, actions, "t_heat_sp", theat_rl_actionspace)

heat_model = tensorflow.keras.models.load_model(
    './server/tfmodels/heat.model')


@app.post("/predict")
def predict(body: agent_endpoint):
    arr = [value for value in dict(body).values()]
    print(len(arr))
    prediction = heat_model.predict([arr])
    data = np.argmax(prediction[0])
    # prediction = 0
    return ResponseModel(data=int(data), message="action for step ")


@app.post("/environment")
def heat_env(body: environment_endpoint):

    obs, reward, done = env_heat.step(body.action)
    dict = {
        "obs": list(obs),
        "reward": float(reward),
        "done": bool(done)
    }
    return ResponseModel(data=dict, message="obs,reward,last step values")


@app.get("/reset")
def reset_heat_env():
    obs = env_heat.resetinit()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.get("/reset_team")
def reset_heat_env_team():
    obs = env_heat.reset()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.post("/teamnindex")
def set_teamnindex(body: teamnindex_endpoint):
    data = {}
    return ResponseModel(data=data, message="team and index set")