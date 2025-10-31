from functools import lru_cache
import urllib.request
import json

try:
    from importlib.metadata import version, metadata
except ImportError:
    from importlib_metadata import version, metadata  # Python < 3.8


def get_local_pkg_version():
    """
    Get the current version from the installed package metadata.
    
    Returns:
        str: The version string (e.g., "0.1.5")
    """
    try:
        return version("min-obproject")
    except Exception as e:
        raise ValueError(f"Could not determine min-obproject version: {e}")


def get_pkg_name():
    """
    Get the package name from the installed package metadata.
    
    Returns:
        str: The package name (e.g., "min-obproject")
    """
    try:
        meta = metadata("min-obproject")
        return meta["Name"]
    except Exception as e:
        raise ValueError(f"Could not determine package name: {e}")


@lru_cache(maxsize=1)
def get_pkg_version(package_name=None, fallback_to_local=True):
    """
    Get the latest published version of a package from PyPI.
    
    Args:
        package_name: The name of the package on PyPI (default: None, uses name from pyproject.toml)
        fallback_to_local: If True, fall back to local pyproject.toml on error (default: True)
    
    Returns:
        str: The latest version string (e.g., "0.1.5")
    """
    if package_name is None:
        package_name = get_pkg_name()
    
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            version = data["info"]["version"]
            return version
    except Exception as e:
        if fallback_to_local:
            # Fall back to local version if PyPI lookup fails
            return get_local_pkg_version()
        else:
            raise RuntimeError(f"Failed to fetch version from PyPI: {e}") from e

