# Need to make 2 classes, Simulation Varibles and Simulation Asset

class AssetVariable:
    # Represents the varibles as a persentage of the asset
    def __init__(self, name, expected_return, standard_deviation):
        self.name = name
        self.expected_return = expected_return
        self.standard_deviation = standard_deviation

class SimulationAsset:
    # Represents the asset (e.g. House, portfolietc...)
    def __init__(self, name, initial_value):
        self.name = name
        self.initial_value = initial_value
        self.variables = []

    def add_varibes(self, varible: AssetVariable):
        # adds the Asset varible to the asset
        self.variables.append(varible)