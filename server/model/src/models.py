# folder that contains all the data base model classes with constraints
import geopandas as gpd
from server.model.src.parameters.age_param import AgeParam
from server.model.src.parameters.culture_param import CultureParam
from server.model.src.parameters.distance_param import DistanceParam
from server.model.src.parameters.grocery_param import GroceryParam
from server.model.src.parameters.outdoor_param import OutdoorParam
from server.model.src.parameters.price_param import PriceParam
from server.model.src.parameters.safety_param import SafetyParam
from server.model.src.parameters.transport_param import TransportParam
from server.model.src.parameters.walkway_param import WalkwayParam
from server.model.src.parameters.well_being_param import WellBeingParam
from server.model.src.parameters.noise_param import NoiseParam
from server.model.src.data.data import Data


class Model:
    def __init__(self):
        self.data = Data()
        self.parameters = [
            PriceParam(self.data),
            AgeParam(self.data),
            DistanceParam(self.data),
            WellBeingParam(self.data),
            SafetyParam(self.data),
            CultureParam(self.data),
            OutdoorParam(self.data),
            TransportParam(self.data),
            WalkwayParam(self.data),
            GroceryParam(self.data),
            SafetyParam(self.data),
            NoiseParam(self.data)
        ]

    def make_df_copy(self):
        res = self.data.GENERAL_DF.copy().filter(items=['Levekårsnavn', 'Score'])
        with open("general_df.json", "w") as outfile:
            outfile.write(res.head().to_json())
        return self.data.GENERAL_DF.copy().filter(items=['Levekårsnavn', 'Score'])

    def calculate_scores(self, param_input: dict):
        result = self.make_df_copy()
        result['Score'] = 0
        for param in self.parameters:
            if param.INPUT_NAME in param_input.keys():
                inp = param_input[param.INPUT_NAME]
                tmp = param.calculate_score(inp)
                result['Score'] = result['Score'].add(tmp['Score'], fill_value=0)
            elif 'environment' in param_input.keys():
                if param.INPUT_NAME in param_input['environment'].keys():
                    inp = param_input['environment'][param.INPUT_NAME]
                    tmp = param.calculate_score(inp)
                    result['Score'] = result['Score'].add(tmp['Score'], fill_value=0)
        # result['Score'] = pd.qcut(result['Score'], 5, labels=False, duplicates='drop')
        result['Score'] = result['Score'].astype(float)
        return result

    def generate_map(self, param_input: dict):
        result = self.calculate_scores(param_input)
        return gpd.GeoDataFrame(result, geometry=self.data.GEOMETRY)

    def get_zone_by_id(self, i: int):
        return self.data.get_zone_by_id(i)
