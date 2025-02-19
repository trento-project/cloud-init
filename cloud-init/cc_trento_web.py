"""Cloud-init Module for Trento Web"""

import logging
import os.path

from cloudinit import util
from cloudinit.cloud import Cloud
from cloudinit.config import Config
from cloudinit.config.schema import MetaSchema
from cloudinit.settings import PER_ALWAYS

LOG = logging.getLogger(__name__)

trento_web_config_path = "/etc/trento/trento-web"

meta: MetaSchema = {
    "id": "cc_trento_web",
    "distros": ["suse"],
    "frequency": PER_ALWAYS,
    #"activate_by_schema_keys": ["trento"]
}

_DEFAULT_SETTINGS = {
    "ACCESS_TOKEN_ENC_SECRET": {
        "path": "trento/web/secrets/access_token_signer",
        "required": True,
    },
    "ADMIN_PASSWORD": {
        "path": "trento/web/admin/password",
        "required": True,
    },
    "ADMIN_USER": {
        "path": "trento/web/admin/user",
        "required": False,
    },
    "ALERT_RECIPIENT": {
        "path": "trento/web/alerting/recipient",
        "required": False,
    },
    "ALERT_SENDER": {
        "path": "trento/web/alerting/sender",
        "required": False,
    },
    "AMQP_URL": {
        "path": "trento/web/amqp/url",
        "required": True,
    },
    "CHARTS_ENABLED": {
        "path": "trento/web/charts",
        "required": False,
    },
    "CHECKS_INTERVAL": {
        "path": "trento/web/checks/interval",
        "required": False,
    },
    "CHECKS_SERVICE_BASE_URL": {
        "path": "trento/web/checks_service/url",
        "required": False,
    },
    "DATABASE_URL": {
        "path": "trento/web/database/url",
        "required": True,
    },
    "DATABASE_POOL_SIZE": {
        "path": "trento/web/database/pool_size",
        "required": False,
    },
    "ENABLE_ALERTING": {
        "path": "trento/web/alerting",
        "required": False,
    },
    "ENABLE_API_KEY": {
        "path": "trento/web/api/enable_key",
        "required": False,
    },
    "ENABLE_OAUTH2": {
        "path": "trento/web/auth/enable_oauth2",
        "required": False,
    },
    "ENABLE_OIDC": {
        "path": "trento/web/auth/enable_oidc",
        "required": False,
    },
    "ENABLE_SAML": {
        # TODO: Add SAML configuration
        "path": "trento/web/auth/enable_saml",
        "required": False,
    },
    "EVENTSTORE_URL": {
        "path": "trento/web/eventstore/url",
        "required": True,
    },
    "EVENTSTORE_POOL_SIZE": {
        "path": "trento/web/eventstore/pool_size",
        "required": False,
    },
    "OIDC_BASE_URL": {
        "path": "trento/web/auth/oidc/base_url",
        "required": False,
    },
    "OIDC_CALLBACK_URL": {
        "path": "trento/web/auth/oidc/callback_url",
        "required": False,
    },
    "OIDC_CLIENT_ID": {
        "path": "trento/web/auth/oidc/client_id",
        "required": False,
    },
    "OIDC_CLIENT_SECRET": {
        "path": "trento/web/auth/oidc/client_secret",
        "required": False,
    },
    "OAUTH2_AUTHORIZE_URL": {
        "path": "trento/web/auth/oauth2/authorize_url",
        "required": False,
    },
    "OAUTH2_BASE_URL": {
        "path": "trento/web/auth/oauth2/base_url",
        "required": False,
    },
    "OAUTH2_CLIENT_ID": {
        "path": "trento/web/auth/oauth2/client_id",
        "required": False,
    },
    "OAUTH2_CLIENT_SECRET": {
        "path": "trento/web/auth/oauth2/client_secret",
        "required": False,
    },
    "OAUTH2_CALLBACK_URL": {
        "path": "trento/web/auth/oauth2/callback_url",
        "required": False,
    },
    "OAUTH2_SCOPES": {
        "path": "trento/web/auth/oauth2/scopes",
        "required": False,
    },
    "OAUTH2_TOKEN_URL": {
        "path": "trento/web/auth/oauth2/token_url",
        "required": False,
    },
    "OAUTH2_USER_URL": {
        "path": "trento/web/auth/oauth2/user_url",
        "required": False,
    },
    "PORT": {
        "path": "trento/web/api/port",
        "required": False,
    },
    "PROMETHEUS_URL": {
        "path": "trento/web/prometheus/url",
        "required": False,
    },
    "REFRESH_TOKEN_ENC_SECRET": {
        "path": "trento/web/secrets/refresh_token_signer",
        "required": True,
    },
    "SECRET_KEY_BASE": {
        "path": "trento/web/secrets/secret_key_base",
        "required": True,
    },
    "SMTP_SERVER": {
        "path": "trento/web/smtp/server",
        "required": False,
    },
    "SMTP_PORT": {
        "path": "trento/web/smtp/port",
        "required": False,
    },
    "SMTP_USER": {
        "path": "trento/web/smtp/user",
        "required": False,
    },
    "SMTP_PASSWORD": {
        "path": "trento/web/smtp/password",
        "required": False,
    },
    "TRENTO_WEB_ORIGIN": {
        "path": "trento/web/api/origin",
        "required": True,
    },
}

def _cfg_get_checked(cfg: Config, path: str, required: bool) -> any:
    _, key = os.path.split(path)
    value = util.get_cfg_by_path(cfg, path, None)
    if value is None and required:
        raise ValueError(f"Key \"{key}\" at XPath \"/{path}\" required, but not found")
    return value


def _handle_web(name: str, cfg: Config, cloud: Cloud, args: list) -> None:
    if util.get_cfg_by_path(cfg, "trento/web", None) is None:
        LOG.debug("Not configuring trento-web. Missing key \"web\" in section \"trento\"")
        return

    try:
        LOG.debug("Removing old configuration")
        os.remove(trento_web_config_path)
    except FileNotFoundError:
        pass

    try:
        trento_config_dir, _ = os.path.split(trento_web_config_path)
        os.makedirs(trento_config_dir, exist_ok=True)
        with open(trento_web_config_path, "wt") as config_file:
            for setting_key in _DEFAULT_SETTINGS:
                setting_value = _DEFAULT_SETTINGS[setting_key]
                config_value = _cfg_get_checked(cfg, setting_value["path"], setting_value["required"])
                if config_value is not None:
                    config_file.write(f"{setting_key}={config_value}\n")
    except Exception as e:
        util.logexc(LOG, e)
        raise


def handle(name: str, cfg: Config, cloud: Cloud, args: list) -> None:
    LOG.debug("Configuring Trento Web")

    if not "trento" in cfg:
        LOG.debug(
            "Skipping module \"%s\". Key \"trento\" not in configuration",
            name,
        )
        return

    _handle_web(name, cfg, cloud, args)
