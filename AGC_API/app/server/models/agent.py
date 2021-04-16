from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class environment_endpoint(BaseModel):
    action: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "action": 0,

            }
        }


class teamnindex_endpoint(BaseModel):
    team: int = Field(...)
    index: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "team": 0,
                "index": 10,

            }
        }


class agent_endpoint(BaseModel):
    time: float = Field(...)
    AssimLight: float = Field(...)
    BlackScr: float = Field(...)
    CO2air: float = Field(...)
    Cum_irr: float = Field(...)
    EC_drain_PC: float = Field(...)
    EnScr: float = Field(...)
    HumDef: float = Field(...)
    PipeGrow: float = Field(...)
    PipeLow: float = Field(...)
    Rhair: float = Field(...)
    Tair: float = Field(...)
    Tot_PAR: float = Field(...)
    Tot_PAR_Lamps: float = Field(...)
    VentLee: float = Field(...)
    Ventwind: float = Field(...)
    co2_dos: float = Field(...)
    pH_drain_PC: float = Field(...)
    water_sup: float = Field(...)
    ProdA: float = Field(...)
    ProdB: float = Field(...)
    avg_nr_harvested_trusses: float = Field(...)
    Truss_development_time: float = Field(...)
    Nr_fruits_ClassA: float = Field(...)
    Weight_fruits_ClassA: float = Field(...)
    Nr_fruits_ClassB: float = Field(...)
    Weight_fruits_ClassB: float = Field(...)
    Flavour: float = Field(...)
    TSS: float = Field(...)
    Acid: float = Field(...)
    Juice: float = Field(...)
    Bite: float = Field(...)
    Weight: float = Field(...)
    DMC_fruit: float = Field(...)
    Stem_elong: float = Field(...)
    Stem_thick: float = Field(...)
    Cum_trusses: float = Field(...)
    stem_dens: float = Field(...)
    plant_dens: float = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "time": 43815.000000,
                "AssimLight": 100.0,
                "BlackScr": 35.0,
                "CO2air": 509.0,
                "Cum_irr": 31.600000,
                "EC_drain_PC": 0.3,
                "EnScr": 96.0,
                "HumDef": 8.8,
                "PipeGrow": 0.0,
                "PipeLow": 49.900002,
                "Rhair": 51.900002,
                "Tair": 21.000000,
                "Tot_PAR": 0.0,
                "Tot_PAR_Lamps": 0.0,
                "VentLee": 1.0,
                "Ventwind": 0.0,
                "co2_dos": 0.0000,
                "pH_drain_PC": 6.5,
                "water_sup": 263.0,
                "ProdA": 0.050000,
                "ProdB": 0.100000,
                "avg_nr_harvested_trusses": 0.100000,
                "Truss_development_time": 50.000000,
                "Nr_fruits_ClassA": 0.000000,
                "Weight_fruits_ClassA": 70.000000,
                "Nr_fruits_ClassB": 0.000000,
                "Weight_fruits_ClassB": 0.000000,
                "Flavour": 78.000000,
                "TSS": 8.600000,
                "Acid": 13.300000,
                "Juice": 68.000000,
                "Bite": 193.000000,
                "Weight": 9.500000,
                "DMC_fruit": 8.770000,
                "Stem_elong": 15.000000,
                "Stem_thick": 8.000000,
                "Cum_trusses": 1.000000,
                "stem_dens": 2.600000,
                "plant_dens": 1.300000
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
