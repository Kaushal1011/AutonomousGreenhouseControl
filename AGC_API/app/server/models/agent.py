from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class agent_endpoint(BaseModel):
    AssimLight: float= Field(...)

    class Config:
        schema_extra = {
            "example": {
                "AssimLight": 100.0,

            }
        }

class Updateagent_endpoint(BaseModel):
    AssimLight: Optional[float]

    class Config:
        schema_extra = {
             "example": {
                "AssimLight": 100.0,
            }
        }



class enviorenment_endpoint(BaseModel):
    Juice: float=Field(...)
    time: float=Field(...)
    Acid: float=Field(...)
    AssimLight: float=Field(...)
    Bite: float=Field(...)
    BlackScr: float=Field(...)
    CO2_cons: float=Field(...)
    CO2air: float=Field(...)
    Cum_irr: float=Field(...)
    Cum_trusses: float=Field(...)
    DMC_fruit: float=Field(...)
    Drain: float=Field(...)
    EC_drain_PC: float=Field(...)
    EC_slab1: float=Field(...)
    EC_slab2: float=Field(...)
    ElecHigh: float=Field(...)
    ElecLow: float=Field(...)
    EnScr: float=Field(...)
    Flavour: float=Field(...)
    Heat_cons: float=Field(...)
    HumDef: float=Field(...)
    Irr: float=Field(...)
    Nr_fruits_ClassA: float=Field(...)
    Nr_fruits_ClassB: float=Field(...)
    PipeGrow: float=Field(...)
    PipeLow: float=Field(...)
    ProdA: float=Field(...)
    ProdB: float=Field(...)
    Rhair: float=Field(...)
    Stem_elong: float=Field(...)
    Stem_thick: float=Field(...)
    TSS: float=Field(...)
    Tair: float=Field(...)
    Tot_PAR: float=Field(...)
    Tot_PAR_Lamps: float=Field(...)
    Truss_development_time: float=Field(...)
    VentLee: float=Field(...)
    Ventwind: float=Field(...)
    WC_slab1: float=Field(...)
    WC_slab2: float=Field(...)
    Weight: float = Field(...)
    Weight_fruits_ClassA: float=Field(...)
    Weight_fruits_ClassB: float=Field(...)
    avg_nr_harvested_trusses: float=Field(...)
    co2_dos: float=Field(...)
    water_sup: float=Field(...)
    t_slab1: float=Field(...)
    t_slab2: float=Field(...)
    pH_drain_PC: float=Field(...)
    plant_dens: float=Field(...)
    stem_dens: float=Field(...)

    class Config:
        schema_extra = {
            "example": {
                "Juice": 100.0,
                "time": 100.0,
                "Acid": 100.0,
                "AssimLight": 100.0,
                "Bite": 100.0,
                "BlackScr": 100.0,
                "CO2_cons": 100.0,
                "CO2air": 100.0,
                "Cum_irr": 100.0,
                "Cum_trusses": 100.0,
                "DMC_fruit": 100.0,
                "Drain": 100.0,
                "EC_drain_PC": 100.0,
                "EC_slab1": 100.0,
                "EC_slab2": 100.0,
                "ElecHigh": 100.0,
                "ElecLow": 100.0,
                "EnScr": 100.0,
                "Flavour": 100.0,
                "Heat_cons": 100.0,
                "HumDef": 100.0,
                "Irr": 100.0,
                "Nr_fruits_ClassA": 100.0,
                "Nr_fruits_ClassB": 100.0,
                "PipeGrow": 100.0,
                "PipeLow": 100.0,
                "ProdA": 100.0,
                "ProdB": 100.0,
                "Rhair": 100.0,
                "Stem_elong": 100.0,
                "Stem_thick": 100.0,
                "TSS": 100.0,
                "Tair": 100.0,
                "Tot_PAR": 100.0,
                "Tot_PAR_Lamps": 100.0,
                "Truss_development_time": 100.0,
                "VentLee": 100.0,
                "Ventwind": 100.0,
                "WC_slab1": 100.0,
                "WC_slab2": 100.0,
                "Weight": 100.0,
                "Weight_fruits_ClassA": 100.0,
                "Weight_fruits_ClassB": 100.0,
                "avg_nr_harvested_trusses": 100.0,
                "co2_dos": 100.0,
                "water_sup": 100.0,
                "t_slab1": 100.0,
                "t_slab2": 100.0,
                "pH_drain_PC": 100.0,
                "plant_dens": 100.0,
                "stem_dens": 100.0,

            }
        }

class Updateenviorenment_endpoint(BaseModel):
    Juice: Optional[float]
    time: Optional[float]
    Acid: Optional[float]
    AssimLight: Optional[float]
    Bite: Optional[float]
    BlackScr: Optional[float]
    CO2_cons: Optional[float]
    CO2air: Optional[float]
    Cum_irr: Optional[float]
    Cum_trusses: Optional[float]
    DMC_fruit: Optional[float]
    Drain: Optional[float]
    EC_drain_PC: Optional[float]
    EC_slab1: Optional[float]
    EC_slab2: Optional[float]
    ElecHigh: Optional[float]
    ElecLow: Optional[float]
    EnScr: Optional[float]
    Flavour: Optional[float]
    Heat_cons: Optional[float]
    HumDef: Optional[float]
    Irr: Optional[float]
    Nr_fruits_ClassA: Optional[float]
    Nr_fruits_ClassB: Optional[float]
    PipeGrow: Optional[float]
    PipeLow: Optional[float]
    ProdA: Optional[float]
    ProdB: Optional[float]
    Rhair: Optional[float]
    Stem_elong: Optional[float]
    Stem_thick: Optional[float]
    TSS: Optional[float]
    Tair: Optional[float]
    Tot_PAR: Optional[float]
    Tot_PAR_Lamps: Optional[float]
    Truss_development_time: Optional[float]
    VentLee: Optional[float]
    Ventwind: Optional[float]
    WC_slab1: Optional[float]
    WC_slab2: Optional[float]
    Weight: Optional[float]
    Weight_fruits_ClassA: Optional[float]
    Weight_fruits_ClassB: Optional[float]
    avg_nr_harvested_trusses: Optional[float]
    co2_dos: Optional[float]
    water_sup: Optional[float]
    t_slab1: Optional[float]
    t_slab2: Optional[float]
    pH_drain_PC: Optional[float]
    plant_dens: Optional[float]
    stem_dens: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "Juice": 100.0,
                "time": 100.0,
                "Acid": 100.0,
                "AssimLight": 100.0,
                "Bite": 100.0,
                "BlackScr": 100.0,
                "CO2_cons": 100.0,
                "CO2air": 100.0,
                "Cum_irr": 100.0,
                "Cum_trusses": 100.0,
                "DMC_fruit": 100.0,
                "Drain": 100.0,
                "EC_drain_PC": 100.0,
                "EC_slab1": 100.0,
                "EC_slab2": 100.0,
                "ElecHigh": 100.0,
                "ElecLow": 100.0,
                "EnScr": 100.0,
                "Flavour": 100.0,
                "Heat_cons": 100.0,
                "HumDef": 100.0,
                "Irr": 100.0,
                "Nr_fruits_ClassA": 100.0,
                "Nr_fruits_ClassB": 100.0,
                "PipeGrow": 100.0,
                "PipeLow": 100.0,
                "ProdA": 100.0,
                "ProdB": 100.0,
                "Rhair": 100.0,
                "Stem_elong": 100.0,
                "Stem_thick": 100.0,
                "TSS": 100.0,
                "Tair": 100.0,
                "Tot_PAR": 100.0,
                "Tot_PAR_Lamps": 100.0,
                "Truss_development_time": 100.0,
                "VentLee": 100.0,
                "Ventwind": 100.0,
                "WC_slab1": 100.0,
                "WC_slab2": 100.0,
                "Weight": 100.0,
                "Weight_fruits_ClassA": 100.0,
                "Weight_fruits_ClassB": 100.0,
                "avg_nr_harvested_trusses": 100.0,
                "co2_dos": 100.0,
                "water_sup": 100.0,
                "t_slab1": 100.0,
                "t_slab2": 100.0,
                "pH_drain_PC": 100.0,
                "plant_dens": 100.0,
                "stem_dens": 100.0,

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