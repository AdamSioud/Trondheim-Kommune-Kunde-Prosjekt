from server.model.src.parameters.environment_param_interface import EnvironmentParam


class CultureParam(EnvironmentParam):

    def __init__(self, data):
        super().__init__(data, 'tilgjengelighet kultur')
        self.INPUT_NAME = 'culture_input'
