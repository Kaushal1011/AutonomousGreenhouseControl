import psycopg2

conn = psycopg2.connect(
    host="database-1.cvq7vtnqted7.ap-south-1.rds.amazonaws.com",
    port="5432",
    database="WorkDB",
    user="postgres",
    password="aobdagc123")

UPDATEDB = False

insertobs = """INSERT INTO public.observations( 
	"time", "Assimlight", "BlackScr", "CO2air", "Cum_irr", "EC_drain_PC", "EnScr", "HumDef", "PipeGrow", "PipeLow", "Rhair", "Tair", "Tot_PAR", "Tot_PAR_Lamps", "VentLee", "Ventwind", co2_dos, "pH_drain_PC", water_sup, "ProdA", "ProdB", avg_nr_harvested_trusses, "Truss_development_time", "Nr_fruits_ClassA", "Weight_fruits_ClassA", "Nr_fruits_ClassB", "Weight_fruits_ClassB", "Flavour", "TSS", "Acid", "Juice", "Bite", "Weight", "DMC_fruit", "Stem_elong", "Stem_thick", "Cum_trusses", stem_dens, plant_dens)
VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})
"""

deleteobs = """DELETE FROM public.observations
	WHERE true;"""

insertreward = """INSERT INTO public.reward(
	agent_reward, random_reward, index)
	VALUES ({}, {}, {});"""

updatereward = """UPDATE public.reward
	SET random_reward={}
	WHERE index={};"""

deleterewards = """DELETE FROM public.reward
	WHERE true"""

insertaction = """INSERT INTO public.actions(
	agent_actions, original_actions, random_actions, index)
	VALUES ({}, {}, {}, {});"""

updateaction = """UPDATE public.actions
	SET original_actions={}, random_actions={}
	WHERE index={};"""

deleteaction = """DELETE FROM public.actions
	WHERE true"""

if __name__ == "__main__":
    # print(conn)
    cursor = conn.cursor()
    a = cursor.execute(insertaction.format(0, 0, 0, 0))
    conn.commit()
