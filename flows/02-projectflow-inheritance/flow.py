from metaflow import step, pypi_base
from obproject import ProjectFlow
from src.flow_templates import NeuralNetworkFlow

# Uncomment @pypi_base for remote execution (Kubernetes/Batch).
# Comment out for local development (use `uv pip install -e .` instead).
@pypi_base(packages={"min-obproject": ""})
class CustomizedTrainingFlow(ProjectFlow, NeuralNetworkFlow):

    @step
    def start(self):
        self._resolve_config()
        self.next(self.end)

    @step
    def end(self):
        # stdout should show your override value and another default value.
        print("Resolved config:", self.config)


if __name__ == "__main__":
    CustomizedTrainingFlow()
