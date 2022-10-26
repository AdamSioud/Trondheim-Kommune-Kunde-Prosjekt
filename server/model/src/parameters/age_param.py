from server.model.src.parameters.slider_param import SliderParam
from server.model.src.data.data import Data


class AgeParam(SliderParam):

    def __init__(self, data):
        super().__init__(data)
        self.INPUT_NAME = "age_input"

    def __give_score(self, price, budget):
        return super()._give_score(price, budget, False)

    def calculate_score(self, input_: dict):
        result = self.data.DFS.get('Ages').copy()
        budget = input_['percent'] / 100
        print(budget)
        clms = []
        for sel in input_['selected']:
            clms.append(sel + ".Andel")
        weight = input_['weight']
        # should .round(2) be here. result becomes different ... ??
        result['Score'] = result[clms].sum(axis=1).round(2)\
            .apply(lambda price: self.__give_score(price, budget) * weight)
        return result.filter(items=['Levekårsnavn', 'Score'])


'''
age_input = {
    "selected": ['underage (0-17)', 'young adult (18-34)'],
    "percent": 50,
    "weight": 1
}
data = Data()
ages_param = AgeParam(data)
print(ages_param.calculate_score(age_input))
'''
