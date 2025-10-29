from metaflow import step, Config, Parameter
from obproject import ProjectFlow
import os


class ConfigOverrideTestFlow(ProjectFlow):

    base_config = Config(
        "config", default=os.path.join(os.path.dirname(__file__), "config.json")
    )
    lr = Parameter(
        name="lr",
        default=0.001,
        type=float,
        help="Override for the lr value in config.json's train_args.",
        required=False,
    )

    def _resolve_config(self):
        train_args_config = dict(self.base_config["train_args"])
        # Cast to dict because ConfigValue is immutable.
        if self.lr:
            train_args_config["lr"] = self.lr
        self.config = train_args_config

    @step
    def start(self):
        self._resolve_config()
        self.next(self.end)

    @step
    def end(self):
        print("Resolved config:", self.config)


if __name__ == "__main__":
    ConfigOverrideTestFlow()
