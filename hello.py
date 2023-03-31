import cityflow

eng = cityflow.Engine("./config/heur_config.json")

eng.reset()
for i in range(75):
    eng.next_step()

