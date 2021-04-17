from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.models.agent import (
    agent_endpoint,
    environment_endpoint,
    ResponseModel,
    teamnindex_endpoint,
)
from server.AGCRLEnv import AGCRLEnv
import numpy as np
import tensorflow
import pickle

app = APIRouter()

with open("./server/observations.pickle", "rb") as handle:
    obs = pickle.load(handle)
with open("./server/actions.pickle", "rb") as handle:
    actions = pickle.load(handle)

assim_rl_actionspace = np.linspace(0, 100, 21)
env_assim = AGCRLEnv(obs, actions, "assim_sp", assim_rl_actionspace)
env_assim_random = AGCRLEnv(obs, actions, "assim_sp", assim_rl_actionspace)

assim_model = tensorflow.keras.models.load_model(
    "./server/tfmodels/assim.model")


@app.post("/predict")
def predict(body: agent_endpoint):
    arr = [value for value in dict(body).values()]
    print(len(arr))
    prediction = assim_model.predict([arr])
    data = np.argmax(prediction[0])
    # prediction = 0
    return ResponseModel(data=int(data), message="action for step ")


@app.post("/environment")
def assim_env(body: environment_endpoint):

    obs, reward, done = env_assim.step(body.action)
    dict = {"obs": list(obs), "reward": float(reward), "done": bool(done)}
    return ResponseModel(data=dict, message="obs,reward,last step values")


@app.get("/reset")
def reset_assim_env():
    obs = list(env_assim.resetinit())
    env_assim_random.resetinit()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.get("/reset_team")
def reset_assim_env_team():
    obs = list(env_assim.reset())
    env_assim_random.resetinit()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.post("/teamnindex")
def set_teamnindex(body: teamnindex_endpoint):
    env_assim.index = body.index
    env_assim.teamindex = body.team
    return ResponseModel(data=body, message="team and index set")


@app.get("/randomstep")
def randomstep():
    # return random action orignal action & random action
    randomaction = np.random.randint(0, len(env_assim.action_space))
    action = env_assim_random.actions[env_assim.teamindex][env_assim.action_parameter][env_assim.index]
    obs, reward, done = env_assim.step(randomaction)
    data = {
        "randomaction": float(randomaction),
        "action": float(action),
        "randomreward": float(reward)
    }
    return ResponseModel(data=data, message="team and index set")
