from .settings_comon import *
import environ



env = environ.Env(
    DEBUG=(bool, False)
)

if env('SETTINGS') == 'local':
    from .settings_local import *
    print('settings_local')
else:
    from .settings_prod import *
    print('settings_prod')
