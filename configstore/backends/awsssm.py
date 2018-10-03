try:
    import boto3
except ImportError:
    boto3 = None


class AwsSsmBackend(object):

    def __init__(self):
        if boto3 is None:
            raise ImportError('install configstore[awsssm] to use '
                              'the awsssm backend')

    def get_setting(self, param):
        client = boto3.client('ssm')
        response = client.get_parameter(Name=param)
        return response['Parameter']['Value']
