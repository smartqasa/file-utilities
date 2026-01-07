import os
from typing import Iterable


class PathValidationError(ValueError):
    """Raised when a path is unsafe or not permitted."""


def validate_path(path: str, allowed_roots: Iterable[str], default_root: str = "/config") -> str:
    """
    Validate and normalize a filesystem path.

    - Relative paths are rooted at default_root
    - Absolute paths must fall under allowed_roots
    - Symlinks and traversal are resolved before validation

    Returns resolved absolute path.
    """
    if not path:
        raise PathValidationError("Path is required")

    # Apply default root for relative paths
    if not os.path.isabs(path):
        path = os.path.join(default_root, path)

    resolved = os.path.realpath(path)

    for root in allowed_roots:
        root_real = os.path.realpath(root)
        if resolved == root_real or resolved.startswith(root_real + os.sep):
            return resolved

    raise PathValidationError(f"Access denied for path: {path}")
