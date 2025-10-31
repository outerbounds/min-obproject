import sys
from metaflow import StepMutator
from .utils import get_pkg_version, get_pkg_name


class smart_pypi(StepMutator):

    '''
    Selectively add @pypi decorator based on the presence of @kubernetes decorator.
    Actively disable the step if it is run locally, to avoid reinstalling the packages 
    already installed using pip install -e .
    The only automatically added contents are those that match the /src module.
    Users interact with the same API as @pypi if they want to add extra packages.
    '''

    def init(self, *args, **kwargs):
        self.python = kwargs.get("python", None)
        self.packages = kwargs.get("packages", {})
        self.package_name = get_pkg_name()
        self.min_obproject_version = kwargs.get("min_obproject_version", get_pkg_version())
    
    def mutate(self, mutable_step):
        has_k8s_deco = False
        for s in mutable_step.decorator_specs:
            if s[0] == 'kubernetes':
                has_k8s_deco = True
                break

        deco_kwargs = {}
        if has_k8s_deco or 'kubernetes' in ' '.join(sys.argv) or 'argo-workflows' in ' '.join(sys.argv):
            packages = self.packages | {self.package_name: self.min_obproject_version}
            deco_kwargs = {"python": self.python, "packages": packages}
        else:
            if self.python is None and self.packages is None:
                deco_kwargs = {"disabled": True}
            elif self.python is not None:
                deco_kwargs = {"packages": {self.package_name: self.min_obproject_version}}
                if self.python is not None:
                    deco_kwargs["python"] = self.python
            else:
                packages = self.packages | {self.package_name: self.min_obproject_version}
                deco_kwargs = {"packages": packages}
                if self.python is not None:
                    deco_kwargs["python"] = self.python

        mutable_step.add_decorator("pypi", deco_kwargs=deco_kwargs)