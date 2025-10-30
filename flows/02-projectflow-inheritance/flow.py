from metaflow import step, pypi
from obproject import ProjectFlow
from src.flow_templates import NeuralNetworkFlow

### Uncomment @pypi for remote execution (Kubernetes/Batch).
pypi = pypi(packages={"min-obproject": "0.1.3"}) # remote   

### Uncomment out local development (with `uv pip install -e .`).
# pypi = pypi(disabled=True) # local 

class CustomizedTrainingFlow(ProjectFlow, NeuralNetworkFlow):

    @pypi
    @step
    def start(self):
        self._resolve_nn_config()  # via NeuralNetworkFlow.
        self.next(self.end)

    @pypi
    @step
    def end(self):
        # stdout should show your override value and another default value.
        print("Resolved config:", self.config)


if __name__ == "__main__":
    CustomizedTrainingFlow()
