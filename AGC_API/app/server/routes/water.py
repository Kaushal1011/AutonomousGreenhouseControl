from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.models.agent import agent_endpoint, environment_endpoint, ResponseModel, teamnindex_endpoint
from server.AGCRLEnvWater import AGCRLEnv
from server.database import (
    conn,
    insertaction,
    insertobs,
    insertreward,
    updateaction,
    updatereward,
    deleteaction,
    deleteobs,
    deleterewards,
    UPDATEDB

)
import numpy as np
import tensorflow
import pickle

app = APIRouter()

with open('./server/observations.pickle', 'rb') as handle:
    obs = pickle.load(handle)
with open('./server/actions.pickle', 'rb') as handle:
    actions = pickle.load(handle)

water_rl_actionspace = np.linspace(0, 2000, 9)
env_water = AGCRLEnv(obs, actions, "water_sup_intervals_sp_min",
                     water_rl_actionspace)

env_water_random = AGCRLEnv(obs, actions, "water_sup_intervals_sp_min",
                            water_rl_actionspace)

water_model = tensorflow.keras.models.load_model(
    './server/tfmodels/water.model')

cursor = conn.cursor()

obsglob = []
actions = []
actionsrandom = []
origactions = []
rewards = [0]
randomrewards = [0]


@app.post("/predict")
def predict(body: agent_endpoint):
    arr = [value for value in dict(body).values()]
    print(len(arr))
    prediction = water_model.predict([arr])
    data = np.argmax(prediction[0])
    actions.append(data)
    # prediction = 0
    return ResponseModel(data=int(data), message="action for step ")


@app.post("/environment")
def water_env(body: environment_endpoint):

    obs, reward, done = env_water.step(body.action)
    dict = {
        "obs": list(obs),
        "reward": float(reward),
        "done": bool(done)
    }
    obsglob.append(list(obs))
    rewards.append(reward+rewards[-1])
    return ResponseModel(data=dict, message="obs,reward,last step values")


@app.get("/reset")
def reset_water_env():
    setglobalvars()
    if UPDATEDB:
        cursor.execute(deleteaction)
        cursor.execute(deleteobs)
        cursor.execute(deleterewards)
    conn.commit()
    obs = list(env_water.resetinit())
    env_water_random.resetinit()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.get("/reset_team")
def reset_water_env_team():
    setglobalvars()
    if UPDATEDB:
        cursor.execute(deleteaction)
        cursor.execute(deleteobs)
        cursor.execute(deleterewards)
    conn.commit()
    obs = list(env_water.reset())
    env_water_random.reset()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.post("/teamnindex")
def set_teamnindex(body: teamnindex_endpoint):
    env_water.index = body.index
    env_water.teamindex = body.team
    return ResponseModel(data=body, message="team and index set")


@app.get("/randomstep")
def randomstep():
    # return random action orignal action & random action
    randomaction = np.random.randint(0, len(env_water.action_space))
    action = int(env_water_random.actions[env_water.teamindex]
                 [env_water.action_parameter][env_water.index]/env_water.interval)
    obs, reward, done = env_water.step(randomaction)
    data = {
        "randomaction": float(randomaction),
        "action": float(action),
        "randomreward": float(reward)
    }
    actionsrandom.append(randomaction)
    randomrewards.append(reward+randomrewards[-1])
    origactions.append(action)
    return ResponseModel(data=data, message="team and index set")


@app.get("/updatetableau")
def updatetableau():
    # print(obsglob, rewards, actions)
    for i in obsglob:
        cursor.execute(insertobs.format(*i))
    for i in range(len(rewards)-1):
        cursor.execute(insertreward.format(rewards[i], randomrewards[i], i))
    for i in range(len(actions)-1):
        cursor.execute(insertaction.format(
            actions[i], origactions[i], actionsrandom[i], i))
    conn.commit()
    setglobalvars()
    return ResponseModel(data=True, message="successfully updated to tableau")


def setglobalvars():

    global obsglob
    global actions
    global actionsrandom
    global origactions
    global rewards
    global randomrewards
    obsglob = []
    actions = []
    actionsrandom = []
    origactions = []
    rewards = [0]
    randomrewards = [0]

    return True
