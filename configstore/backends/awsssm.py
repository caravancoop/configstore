try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:  # pragma: no cover
    boto3 = None


class AwsSsmBackend(object):
    """Backend for AWS System Manager Parameter Store.

    You can create an instance with a prefix:

        AwsSsmBackend('/myapp/pre-prod/')

    so that a call like store.get_setting('DEBUG') will
    try to get a parameter named `/myapp/pre-prod/DEBUG`.
    """

    def __init__(self, name_prefix=''):
        if boto3 is None:
            raise ImportError('install configstore[awsssm] to use the AWS SSM backend')

        self.name_prefix = name_prefix

    def get_setting(self, param):
        client = boto3.client('ssm')
        name = self.name_prefix + param
        try:
            res = client.get_parameter(Name=name, WithDecryption=True)
        except ClientError as exc:
            if exc.response['Error']['Code'] == 'ParameterNotFound':
                return None
            else:
                raise

        return res['Parameter']['Value']
