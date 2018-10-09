import pretend
import pytest

from botocore.exceptions import ClientError

from configstore.backends.awsssm import AwsSsmBackend


def test_awsssm_init_bad_install(monkeypatch):
    monkeypatch.setattr('configstore.backends.awsssm.boto3', None)

    with pytest.raises(ImportError):
        AwsSsmBackend()


def test_awsssm_success(monkeypatch):
    response = {'Parameter': {
        'Value': 'postgres://localhost/app',
    }}
    fake_client = pretend.stub(
        get_parameter=pretend.call_recorder(lambda Name, WithDecryption: response),
    )
    fake_boto3 = pretend.stub(
        client=pretend.call_recorder(lambda service: fake_client),
    )
    monkeypatch.setattr('configstore.backends.awsssm.boto3', fake_boto3)

    b = AwsSsmBackend()
    value = b.get_setting('DATABASE_URL')

    assert value == 'postgres://localhost/app'
    assert fake_boto3.client.calls == [pretend.call('ssm')]
    assert fake_client.get_parameter.calls == [
        pretend.call(Name='DATABASE_URL', WithDecryption=True),
    ]


def test_awsssm_success_with_prefix(monkeypatch):
    response = {'Parameter': {
        'Value': 'off',
    }}
    fake_client = pretend.stub(
        get_parameter=pretend.call_recorder(lambda Name, WithDecryption: response),
    )
    fake_boto3 = pretend.stub(
        client=pretend.call_recorder(lambda service: fake_client),
    )
    monkeypatch.setattr('configstore.backends.awsssm.boto3', fake_boto3)

    b = AwsSsmBackend('/myapp/staging/')
    value = b.get_setting('DEBUG')

    assert value == 'off'
    assert fake_boto3.client.calls == [pretend.call('ssm')]
    assert fake_client.get_parameter.calls == [
        pretend.call(Name='/myapp/staging/DEBUG', WithDecryption=True),
    ]


def test_awsssm_missing(monkeypatch):
    error = ClientError({'Error': {'Code': 'ParameterNotFound'}}, 'get_parameter')
    fake_client = pretend.stub(
        get_parameter=pretend.raiser(error),
    )
    fake_boto3 = pretend.stub(
        client=lambda service: fake_client,
    )

    monkeypatch.setattr('configstore.backends.awsssm.boto3', fake_boto3)

    b = AwsSsmBackend()
    value = b.get_setting('/app1/TEMPLATE_DEBUG')

    assert value is None


def test_awsssm_missing_with_prefix(monkeypatch):
    error = ClientError({'Error': {'Code': 'ParameterNotFound'}}, 'get_parameter')
    fake_client = pretend.stub(
        get_parameter=pretend.raiser(error),
    )
    fake_boto3 = pretend.stub(
        client=lambda service: fake_client,
    )

    monkeypatch.setattr('configstore.backends.awsssm.boto3', fake_boto3)

    b = AwsSsmBackend('/app1/')
    value = b.get_setting('TEMPLATE_DEBUG')

    assert value is None


def test_awsssm_error(monkeypatch):
    error = ClientError({'Error': {'Code': 'SomethingBad'}}, 'get_parameter')
    fake_client = pretend.stub(
        get_parameter=pretend.raiser(error),
    )
    fake_boto3 = pretend.stub(
        client=lambda service: fake_client,
    )

    monkeypatch.setattr('configstore.backends.awsssm.boto3', fake_boto3)

    b = AwsSsmBackend('/app1/')
    with pytest.raises(ClientError):
        b.get_setting('TEMPLATE_DEBUG')
