import configstore

# Create a store object with a stack of backends to look for settings
# in environment first, then docker secrets, then a .env file
store = configstore.Store([
    configstore.GoogleSecretManagerBackend("my-test-project", True),
    configstore.GoogleRuntimeConfiguratorBackend("my-test-project", "general", True),
    configstore.EnvVarBackend(),
    configstore.DockerSecretBackend(),
])

# Add backend to read Docket secrets
configstore.DotenvBackend('/path/to/env/file'),

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
