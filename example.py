import configstore

backends = [
    configstore.DockerSecretBackend(),
    configstore.EnvVarBackend()
]

store = configstore.Store(backends)
# Will throw an exception if APP_SECRET_KEY can't be found in any backend
SECRET_KEY = store.get_setting('APP_SECRET_KEY')
# Will set the default value as the value if APP_SECRET_KEY can't be found
# in any backend
SECRET_KEY = store.get_setting('APP_SECRET_KEY', 'defaultvalue')
