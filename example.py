import configstore

store = configstore.Store([
    configstore.DockerSecretBackend(),
    configstore.EnvVarBackend(),
])

# Will raise an exception if APP_SECRET_KEY isn't found in any backend
SECRET_KEY = store.get_setting('APP_SECRET_KEY')

# Will use 'defaultvalue' if APP_SECRET_KEY isn't found
SECRET_KEY = store.get_setting('APP_SECRET_KEY', 'defaultvalue')

# Setting values and default values can reference other settings
BROKER_URL = store.get_setting('BROKER_URL', '${REDIS_URL}/7')

# Helper param for bool strings (true, false, on, off, yes, no, 1, 0)
DEBUG_MODE = store.get_setting('DEBUG_MODE', 'off', asbool=True)

# Example for list/tuple/etc
# setting value is whitespace-separated: "bob  alice \n marcel"
ADMINS = store.get_setting('ADMINS').split()

del store
