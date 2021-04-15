import numpy as np
from fastapi import FastAPI
import pickle
from server.models.agent import agent_endpoint, environment_endpoint, ResponseModel
from server.AGCRLEnv import AGCRLEnv
import tensorflow
import numpy as np

app = FastAPI()

with open('./server/observations.pickle', 'rb') as handle:
    obs = pickle.load(handle)
with open('./server/actions.pickle', 'rb') as handle:
    actions = pickle.load(handle)

assim_rl_actionspace = np.linspace(0, 100, 21)
env_assim = AGCRLEnv(obs, actions, "assim_sp", assim_rl_actionspace)

theat_rl_actionspace = np.linspace(0, 25, 26)
env_heat = AGCRLEnv(obs, actions, "t_heat_sp", theat_rl_actionspace)

assim_model = tensorflow.keras.models.load_model(
    './server/tfmodels/assim.model')


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this AGC RL Backend API! Visit /docs for api doc"}


@app.post("/predict_theat_sp")
def predict(body: agent_endpoint):

    arr = [value for value in dict(body).values()]
    pass


@app.post("/t_heat_environment")
def heat_env(body: environment_endpoint):
    obs, reward, done = env_heat.step(body.action)
    dict = {
        "obs": list(obs),
        "reward": float(reward),
        "done": bool(done)
    }
    return ResponseModel(data=dict, message="obs,reward,last step values")


@app.get("/reset_t_heat_environment")
def reset_heat_env():
    obs = env_heat.resetinit()
    return ResponseModel(data=obs, message="heat environment reset successful")


@app.get("/reset_t_heat_environment_team")
def reset_heat_env_team():
    obs = env_assim.reset()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.post("/predict_assim_sp")
def predict(body: agent_endpoint):
    arr = [value for value in dict(body).values()]
    print(len(arr))
    prediction = assim_model.predict([arr])
    data = np.argmax(prediction[0])
    # prediction = 0
    return ResponseModel(data=int(data), message="action for step ")


@app.post("/assim_environment")
def assim_env(body: environment_endpoint):

    obs, reward, done = env_assim.step(body.action)
    dict = {
        "obs": list(obs),
        "reward": float(reward),
        "done": bool(done)
    }
    return ResponseModel(data=dict, message="obs,reward,last step values")


@app.get("/reset_assim_environment")
def reset_assim_env():
    obs = env_assim.resetinit()
    return ResponseModel(data=obs, message="luminance environment reset successful")


@app.get("/reset_assim_environment_team")
def reset_assim_env_team():
    obs = env_assim.reset()
    return ResponseModel(data=obs, message="luminance environment reset successful")
