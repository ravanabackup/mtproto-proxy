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


# ---------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------

class ProviderError(BaseError):
    """Provider errors"""


class ProviderFetchError(ProviderError):
    """Unable to fetch data using provider"""

    def __init__(self, url: str, reason: str):
        super().__init__(
            f"Failed to fetch provider: {reason}",
            context={"url": url, "reason": reason},
        )
        self.url = url


class ProviderParseError(ProviderError):
    """Content has fetched, but could not extract proxy from one"""

    def __init__(self, url: str, reason: str):
        super().__init__(
            f"Failed to parse provider response: {reason}",
            context={"url": url, "reason": reason},
        )
        self.url = url


# ---------------------------------------------------------------------
# Proxy URL parsing
# ---------------------------------------------------------------------


class ProxyParseError(BaseError):
    """Proxy URL parsing errors"""


class InvalidProxyURLError(ProxyParseError):
    """Invalid Proxy URL format"""

    def __init__(self, url: str, reason: str = "malformed URL"):
        super().__init__(
            f"invalid proxy URL: {reason}",
            context={"url": url, "reason": reason},
        )
        self.url = url


class MissingProxyFieldError(ProxyParseError):
    """No required query-parameter in Proxy URL"""

    def __init__(self, url: str, field: str):
        super().__init__(
            f"missing required field {field!r} in Proxy URL",
            context={"url": url, "field": field},
        )
        self.url = url
        self.field = field


# ---------------------------------------------------------------------
# Checker
# ---------------------------------------------------------------------


class ProxyCheckerError(BaseError):
    """Proxy checker errors"""


class ProxyConnectionError(ProxyCheckerError):
    """Could not established TCP-connection"""

    def __init__(self, host: str, port: int, reason: int):
        super().__init__(
            f"connection failed: {reason}",
            context={"host": host, "port": port, "reason": reason},
        )
        self.host = host
        self.port = port


class ProxyTimeoutError(ProxyCheckerError):
    """Proxy connecting timeout"""

    def __init__(self, host: str, port: int, timeout: float):
        super().__init__(
            "connection timed out",
            context={"host": host, "port": port, "timeout": timeout},
        )
        self.host = host
        self.port = port
        self.timeout = timeout


# ---------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------

class StorageError(BaseError):
    """File storage errors"""


class FileReadError(StorageError):
    """Unable to read file"""

    def __init__(self, path: Path | str, reason: str):
        super().__init__(
            f"failed to read file: {reason}",
            context={"path": str(path), "reason": reason},
        )
        self.path = path


class FileWriteError(StorageError):
    """Unable to write file"""

    def __init__(self, path: Path | str, reason: str):
        super().__init__(
            f"failed to write file: {reason}",
            context={"path": str(path), "reason": reason},
        )
        self.path = path


class InvalidStorageDataError(StorageError):
    """File is read, but data is invalid"""

    def __init__(self, path: Path | str, reason: str):
        super().__init__(
            f"invalid data in file: {reason}",
            context={"path": str(path), "reason": reason},
        )
        self.path = Path(path)


# ---------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------

class RenderError(BaseError):
    """Rendering error (README, Telegram message)"""


# ---------------------------------------------------------------------
# Telegram
# ---------------------------------------------------------------------

class TelegramError(BaseError):
    """Telegram API errors"""


class TelegramAuthError(TelegramError):
    """Invalid Telegram Bot token / unauthorized"""

    def __init__(self, status_code: int, reason: str):
        super().__init__(
            f"telegram auth failed: {reason}",
            context={"status_code": status_code, "reason": reason},
        )
        self.status_code = status_code


class TelegramAPIError(TelegramError):
    """Other Telegram API errors"""

    def __init__(self, status_code: int | None, reason: str):
        super().__init__(
            f"telegram API error: {reason}",
            context={"status_code": status_code, "reason": reason}
        )
        self.status_code = status_code