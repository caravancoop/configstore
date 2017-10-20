from ..backends.env_var import EnvVarBackend


def test_env_var_success(monkeypatch):
    monkeypatch.setenv('APP_ENVIRONMENT', 'STAGING')

    b = EnvVarBackend()
    value = b.get_config('APP_ENVIRONMENT')

    assert value == 'STAGING'


def test_env_var_missing(monkeypatch):
    monkeypatch.delenv('APP_DEBUG', raising=False)

    b = EnvVarBackend()
    value = b.get_config('APP_DEBUG')

    assert value is None
