from ..settings import ProductSettings
from hyperlocal_platform.core.utils.settings_initializer import init_settings
from ..constants import ENV_PREFIX,SERVICE_NAME

SETTINGS:ProductSettings=init_settings(settings=ProductSettings,service_name=SERVICE_NAME,env_prefix=ENV_PREFIX)