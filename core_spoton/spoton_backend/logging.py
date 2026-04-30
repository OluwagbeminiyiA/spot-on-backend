import os

from core_spoton.spoton_backend.settings import BASE_DIR

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": ">>> {levelname} {asctime} {module} {process:d} {thread:d} {message}", "style": "{"},
        "simple": {"format": ">>> {levelname} {module} {name} {message} {lineno}", "style": "{"},
        "standard": {"format": ">>> {asctime} {levelname} {name} {message}", "style": "{"},
    },
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "debug_only": {"()": "core_spoton.spoton_backend.logging_filters.DebugOnlyFilter"},
        "info_only": {
            "()": "core_spoton.spoton_backend.logging_filters.InfoOnlyFilter",
        },
        "warning_only": {"()": "core_spoton.spoton_backend.logging_filters.WarningOnlyFilter"},
        "error_only": {"()": "core_spoton.spoton_backend.logging_filters.ErrorOnlyFilter"},
        "critical_only": {"()": "core_spoton.spoton_backend.logging_filters.CriticalOnlyFilter"},
    },
    "handlers": {
        "debug_console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "info_console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "filters": ["info_only", "require_debug_true"],
        },
        "warning_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "warning.log"),
            "maxBytes": 10485760,
            "backupCount": 10,
            "level": "WARNING",
            "formatter": "standard",
            "filters": ["warning_only", "require_debug_true"],
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "error.log"),
            "maxBytes": 10485760,
            "backupCount": 10,
            "level": "ERROR",
            "formatter": "standard",
            "filters": ["error_only"],
        },
        "critical_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "critical.log"),
            "maxBytes": 10485760,
            "backupCount": 10,
            "level": "CRITICAL",
            "formatter": "standard",
            "filters": ["critical_only"],
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "level": "ERROR",
            "include_html": True,
            "filters": ["require_debug_false"],
        },
    },
    "loggers": {
        "core_spoton": {
            "handlers": [
                "debug_console",
                "info_console",
                "warning_file",
                "error_file",
                "critical_file",
                "mail_admins",
            ],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}
