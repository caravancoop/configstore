import configstore

store = configstore.Store([
    configstore.DockerSecretBackend(),
    configstore.EnvVarBackend(),
])

# Will raise an exception if APP_SECRET_KEY isn't found in any backend
SECRET_KEY = store.get_setting('APP_SECRET_KEY')

# Will use 'defaultvalue' if APP_SECRET_KEY isn't found
SECRET_KEY = store.get_setting('APP_SECRET_KEY', 'defaultvalue')

del store
