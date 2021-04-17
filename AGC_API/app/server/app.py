import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle

from server.routes.light import app as LightRouter
from server.routes.water import app as WaterRouter
from server.routes.heat import app as HeatRouter

import tensorflow
import numpy as np


app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# theat_rl_actionspace = np.linspace(0, 25, 26)
# env_heat = AGCRLEnv(obs, actions, "t_heat_sp", theat_rl_actionspace)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this AGC RL Backend API! Visit /docs for api doc"}

app.include_router(LightRouter, tags=["Light Simulation"], prefix="/light")
app.include_router(WaterRouter, tags=["Water Simulation"], prefix="/water")
app.include_router(HeatRouter, tags=["Heat Simulation"], prefix="/heat")
