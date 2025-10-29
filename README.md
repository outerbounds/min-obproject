# min-obproject

Reusable Outerbounds flow templates. Demonstrates how to build ML projects with complex configurations in an extensible way.

## Quick Start

```bash
# 1. Install editable package
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e .

# 2. Run example flow locally
python flows/02-projectflow-inheritance/flow.py run --lr 0.5

# 3. Run on Kubernetes (requires @pypi_base uncommented + published to PyPI)
python flows/02-projectflow-inheritance/flow.py --environment=fast-bakery run --with kubernetes --lr 0.5
```

## Key Features

- **Base configs with overrides**: `NeuralNetworkFlow` template automatically loads `config.json` from the flow's directory.  Override specific config values via CLI Parameters without flow boilerplate.
- **Reusable templates**: Write flow logic once, inherit across flows and projects.
- **Fast changing _and_ consistent dependencies**: Toggle `@pypi_base` for local dev (editable install) vs. remote (PyPI install).

## The `@pypi_base` Toggle Pattern

**Core concept**: Comment/uncomment one decorator to switch between local and remote execution.

**Important**: `@pypi_base` requires `--environment=fast-bakery` flag. Local runs without the decorator don't need this flag.

**Local development** (decorator commented out):
```python
# @pypi_base(packages={"min-obproject": ""})
class MyFlow(ProjectFlow, NeuralNetworkFlow):
    ...
```
- Uses editable install from `uv pip install -e .`
- Faster iteration, no publishing required --> comment out @pypi_base in the workflows since we don't want to reinstall.
- Avoids platform-specific wheel issues with @pypi on workstation environment that doesn't match prod (e.g., mac vs linux).

**Remote execution** (decorator uncommented + `--environment=fast-bakery`):
```python
@pypi_base(packages={"min-obproject": ""})  # "" = latest, or pin: "0.1.1"
class MyFlow(ProjectFlow, NeuralNetworkFlow):
    ...
```
- Installs from PyPI in remote containers
- Requires package published to PyPI, as demonstrated with `uv publish` in this document
- Use `""` for latest or pin to specific version for stability
- `--environment=fast-bakery` enables `@pypi_base` decorator

## Repository Structure

```
min-obproject/
├── src/
│   └── flow_templates.py         # NeuralNetworkFlow base template
├── flows/
│   ├── 01-config-override/       # Basic config + parameter override
│   └── 02-projectflow-inheritance/ # Template inheritance example
├── pyproject.toml
└── obproject.toml
```

## Example Flows

### Flow 1: Config Override (`01-config-override/`)

Basic pattern showing config loading and parameter overrides.

```python
from metaflow import FlowSpec, step, Config, Parameter

class ConfigOverrideFlow(FlowSpec):
    base_config = Config("config", default="config.json")
    lr = Parameter('lr', default=None, type=float)
    
    def _resolve_config(self):
        train_args = dict(self.base_config['train_args'])
        if self.lr:
            train_args['lr'] = self.lr
        self.config = train_args
    
    @step
    def start(self):
        self._resolve_config()
        print(f"Config: {self.config}")
        self.next(self.end)
    
    @step
    def end(self):
        pass
```

Run:
```bash
python flows/01-config-override/flow.py run --lr 0.01
```

### Flow 2: Template Inheritance (`02-projectflow-inheritance/`)

Reuses `NeuralNetworkFlow` template - no need to redefine config logic.

```python
from metaflow import step, pypi_base
from obproject import ProjectFlow
from src.flow_templates import NeuralNetworkFlow

# Toggle for local/remote execution
# @pypi_base(packages={"min-obproject": ""})
class CustomizedTrainingFlow(ProjectFlow, NeuralNetworkFlow):
    
    @step
    def start(self):
        self._resolve_config()  # Inherited method
        self.next(self.end)
    
    @step
    def end(self):
        print(f"Config: {self.config}")
```

**`config.json`** (same directory as flow):
```json
{
    "train_args": {
        "lr": 0.001,
        "optimizer": "lbfgs"
    }
}
```

Run:
```bash
# Local
python flows/02-projectflow-inheritance/flow.py run --lr 1.2

# Remote (uncomment @pypi_base first)
python flows/02-projectflow-inheritance/flow.py --environment=fast-bakery run --with kubernetes --lr 1.2
```

## Publishing for Remote Execution

When you need to run on Kubernetes/AWS Batch:

```bash
# Build and publish
uv build
uv publish

# Or test PyPI first
uv publish --publish-url https://test.pypi.org/legacy/
```

Then uncomment `@pypi_base` in your flow and run with `--environment=fast-bakery run --with kubernetes`.

## Deploy to Argo Workflows

```bash
# Ensure @pypi_base is uncommented, then:
python flows/02-projectflow-inheritance/flow.py --environment=fast-bakery argo-workflows create
```

Trigger from Outerbounds UI after overriding learning rate -> `CustomizedTrainingFlow` will launch a new run.

## Benefits of This Pattern

1. **Complex configs** - Manage [hundreds of parameters](https://github.com/meta-pytorch/torchtune/blob/67ab86b94de9e7ac7dd9850113ebe69e2bbd307c/recipes/configs/qwen3/14B_to_8B_KD_lora_single_device.yaml) via JSON files
2. **Selective overrides** - Change specific params via CLI without modifying flows
3. **Centralized logic** - Write config resolution once in `NeuralNetworkFlow`, inherit everywhere
4. **No boilerplate** - Flows that inherit the template get config handling for free

## Requirements

- Python 3.12
- `uv pip install -e .` for local development
- Published to PyPI for remote execution
