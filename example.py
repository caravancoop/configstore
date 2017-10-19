import configstore

configstore.enabled_backends = [
    configstore.DockerSecretBackend(),
    configstore.EnvVarBackend()
]

# Will throw an exception if APP_SECRET_KEY can't be found in any backend
SECRET_KEY = configstore.get_config('APP_SECRET_KEY')
# Will set the default value as the value if APP_SECRET_KEY can't be found
# in any backend
SECRET_KEY = configstore.get_config('APP_SECRET_KEY', 'defaultvalue')
