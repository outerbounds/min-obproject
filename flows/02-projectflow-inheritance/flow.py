from metaflow import step, kubernetes
from obproject import ProjectFlow
from src.flow_templates import NeuralNetworkFlow
from src.step_decorators import smart_pypi


class CustomizedTrainingFlow(ProjectFlow, NeuralNetworkFlow):

    @smart_pypi
    @step
    def start(self):
        self._resolve_nn_config() # via NeuralNetworkFlow.
        self.next(self.end)

    @smart_pypi
    @step
    def end(self):
        print("Resolved config:", self.config)


if __name__ == "__main__":
    CustomizedTrainingFlow()
