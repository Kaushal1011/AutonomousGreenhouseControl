from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.models.agent import (
    agent_endpoint,
    environment_endpoint,
    ResponseModel,
    teamnindex_endpoint,
)
from server.database import (
    conn,
    insertaction,
    insertobs,
    insertreward,
    updateaction,
    updatereward,
    deleteaction,
    deleteobs,
    deleterewards

)
from server.AGCRLEnv import AGCRLEnv
import numpy as np
import tensorflow
import pickle
import random
app = APIRouter()

with open("./server/observations.pickle", "rb") as handle:
    obs = pickle.load(handle)
with open("./server/actions.pickle", "rb") as handle:
    actions = pickle.load(handle)

UPDATEDB = False

assim_rl_actionspace = np.linspace(0, 100, 21)
env_assim = AGCRLEnv(obs, actions, "assim_sp", assim_rl_actionspace)
env_assim_random = AGCRLEnv(obs, actions, "assim_sp", assim_rl_actionspace)

assim_model = tensorflow.keras.models.load_model(
    "./server/tfmodels/assim.model")

cursor = conn.cursor()

obsglob = []
actions = []
actionsrandom = []
origactions = []
rewards = [0]
randomrewards = [0]


@app.post("/predict")
def predict(body: agent_endpoint):
    # i get action here so insert action cursor
    arr = [value for value in dict(body).values()]
    print(len(arr))
    prediction = assim_model.predict([arr])
    data = np.argmax(prediction[0])
    actions.append(data)
    # prediction = 0
    return ResponseModel(data=int(data), message="action for step ")


@app.post("/environment")
def assim_env(body: environment_endpoint):
    # i get observation here so insert observation
    obs, reward, done = env_assim.step(body.action)
    dict = {"obs": list(obs), "reward": float(reward), "done": bool(done)}
    obsglob.append(list(obs))
    rewards.append(reward+rewards[-1])
    return ResponseModel(data=dict, message="obs,reward,last step values")


@app.get("/reset")
def reset_assim_env():
    # delete action observation reward
    setglobalvars()
    if UPDATEDB:
        cursor.execute(deleteaction)
        cursor.execute(deleteobs)
        cursor.execute(deleterewards)
    conn.commit()
    obs = list(env_assim.resetinit())
    env_assim_random.resetinit()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.get("/reset_team")
def reset_assim_env_team():
    # delete action observation reward
    setglobalvars()
    if UPDATEDB:
        cursor.execute(deleteaction)
        cursor.execute(deleteobs)
        cursor.execute(deleterewards)
    conn.commit()
    obs = list(env_assim.reset())
    env_assim_random.reset()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.post("/teamnindex")
def set_teamnindex(body: teamnindex_endpoint):
    env_assim.index = body.index
    env_assim.teamindex = body.team
    return ResponseModel(data=body, message="team and index set")


@app.get("/randomstep")
def randomstep():
    # return random action orignal action & random action
    # update action and reward call
    index = env_assim_random.index
    randomaction = random.choice([0, 20])
    action = int(env_assim_random.actions[env_assim.teamindex]
                 [env_assim.action_parameter][env_assim.index]/env_assim.interval)
    obs, reward, done = env_assim.step(randomaction)
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
