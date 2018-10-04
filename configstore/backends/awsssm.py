from botocore.exceptions import ClientError
try:
    import boto3
except ImportError:
    boto3 = None


class AwsSsmBackend(object):

    def __init__(self, name_prefix=''):
        if boto3 is None:
            raise ImportError('install configstore[awsssm] to use '
                              'the awsssm backend')
        self.name_prefix = name_prefix

    def get_setting(self, param):
        client = boto3.client('ssm')
        try:
            res = client.get_parameter(
                Name=self.name_prefix + param,
                WithDecryption=True
            )
        except ClientError as exc:
            if exc.response['Error']['Code'] == 'ParameterNotFound':
                return None
            else:
                raise

        return res['Parameter']['Value']
