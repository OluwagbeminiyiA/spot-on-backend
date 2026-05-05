import os

from core_spoton.spoton_backend.settings import BASE_DIR

# --- Ensure logs directory exists ---
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# --- Detect CI environment ---
IS_CI = os.getenv("CI", "").lower() == "true"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
            "secondary_log_colors": {},
            "style": "%",
        },
        "verbose": {
            "format": ">>> {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": ">>> {levelname} {module} {name} {message} {lineno}",
            "style": "{",
        },
        "standard": {
            "format": ">>> {asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "debug_only": {"()": "core_spoton.spoton_backend.logging_filters.DebugOnlyFilter"},
        "info_only": {"()": "core_spoton.spoton_backend.logging_filters.InfoOnlyFilter"},
        "warning_only": {"()": "core_spoton.spoton_backend.logging_filters.WarningOnlyFilter"},
        "error_only": {"()": "core_spoton.spoton_backend.logging_filters.ErrorOnlyFilter"},
        "critical_only": {"()": "core_spoton.spoton_backend.logging_filters.CriticalOnlyFilter"},
    },
    "handlers": {
        "debug_console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
            "filters": ["require_debug_true"],
        },
        "info_console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "colored",
            "filters": ["info_only", "require_debug_true"],
        },
        # --- File handlers only if NOT CI ---
        **(
            {}
            if IS_CI
            else {
                "warning_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(LOG_DIR, "warning.log"),
                    "maxBytes": 10485760,
                    "backupCount": 10,
                    "level": "WARNING",
                    "formatter": "standard",
                    "filters": ["warning_only"],
                },
                "error_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(LOG_DIR, "error.log"),
                    "maxBytes": 10485760,
                    "backupCount": 10,
                    "level": "ERROR",
                    "formatter": "standard",
                    "filters": ["error_only"],
                },
                "critical_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(LOG_DIR, "critical.log"),
                    "maxBytes": 10485760,
                    "backupCount": 10,
                    "level": "CRITICAL",
                    "formatter": "standard",
                    "filters": ["critical_only"],
                },
            }
        ),
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "level": "ERROR",
            "include_html": True,
            "filters": ["require_debug_false"],
        },
    },
    "loggers": {
        "core_spoton": {
            "handlers": (
                [
                    "debug_console",
                    "info_console",
                    "mail_admins",
                ]
                + ([] if IS_CI else ["warning_file", "error_file", "critical_file"])
            ),
            "level": "DEBUG",
            "propagate": False,
        }
    },
}
