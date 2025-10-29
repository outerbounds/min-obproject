from metaflow import FlowSpec, Config, Parameter
import os
import inspect


class NeuralNetworkFlow(FlowSpec):

    lr = Parameter(
        name="lr",
        default=None,
        type=float,
        help="Override for the train_args.lr value in config.json's.",
        required=False,
    )

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Only set base_config if the subclass hasn't already defined it
        if "base_config" not in cls.__dict__:
            # Get the module where the subclass is defined
            module = inspect.getmodule(cls)
            if module and hasattr(module, "__file__"):
                # Compute the path to config.json relative to the subclass file
                # FIXME (Eddie): config.json should be configurable.
                config_path = os.path.join(
                    os.path.dirname(module.__file__), "config.json"
                )
                # Dynamically create the Config for this subclass
                cls.base_config = Config("config", default=config_path)

    def _resolve_nn_config(self):
        # Cast to dict because ConfigValue is immutable.
        train_args_config = dict(self.base_config["train_args"])
        if self.lr and self.lr is not None and self.lr != "null" and self.lr > 0:
            train_args_config["lr"] = self.lr
        self.config = train_args_config
