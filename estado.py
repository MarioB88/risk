class State:
    def __init__(self, riskmap, total_map):
        self.riskmap = riskmap
        self.total_map = total_map
        self.acciones = []

    def set_acciones(self, acciones):
        self.acciones = acciones.copy()
        return self.acciones