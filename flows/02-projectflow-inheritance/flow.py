from metaflow import step, pypi
from obproject import ProjectFlow
from src.flow_templates import NeuralNetworkFlow


# Uncomment @pypi_base for remote execution (Kubernetes/Batch).
# Comment out for local development (use `uv pip install -e .` instead).
# @pypi_base(packages={"min-obproject": ""})
class CustomizedTrainingFlow(ProjectFlow, NeuralNetworkFlow):

    @pypi(packages={"min-obproject": "0.1.3"})
    @step
    def start(self):
        self._resolve_nn_config()  # via NeuralNetworkFlow.
        self.next(self.end)

    @pypi(packages={"min-obproject": "0.1.3"})
    @step
    def end(self):
        # stdout should show your override value and another default value.
        print("Resolved config:", self.config)


if __name__ == "__main__":
    CustomizedTrainingFlow()
