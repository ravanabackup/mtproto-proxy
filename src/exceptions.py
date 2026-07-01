from __future__ import annotations

from pathlib import Path
from typing import Any


class BaseError(Exception):
    def __init__(self, message: str = "", *, context: dict[str, Any] | None = None):
        self.message = message
        self.context = context

        super().__init__(self._format())

    def _format(self) -> str:
        if not self.context:
            return self.message
        ctx = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
        return f"{self.message} [{ctx}]" if self.message else ctx
    

# ---------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------

class ConfigError(BaseError):
    """Config errors"""


class MissingEnvVarError(ConfigError):
    """Required environment variable is missing"""

    def __init__(self, var_name: str):
        super().__init__(
            f"required environment variable {var_name} is not set",
            context={"var": var_name},
        )
        self.var_name = var_name


class InvalidConfigValueError(ConfigError):
    """Environment variable exists, but has invalid value"""

    def __init__(self, var_name: str, value: Any, reason: str):
        super().__init__(
            f"invalid value for {var_name!r}: {reason}",
            context={"var": var_name, "value": value, "reason": reason}
        )
        self.var_name = var_name
        self.value = value