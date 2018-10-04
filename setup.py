from setuptools import setup

long_description = '''
configstore is a small pluggable library that lets you retrieve settings
or secrets from a variety of storage systems to configure your app.
'''

setup(
    name='configstore',
    version='0.4',
    description='Retrieve settings and secrets from different stores',
    long_description=long_description,
    url='https://github.com/caravancoop/configstore',
    author='Caravan Coop',
    author_email='hi@caravan.coop',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=[
        'configstore', 'configstore.backends',
    ],
    extras_require={
        # django-dotenv does not actually use or need Django
        'dotenv': ['django-dotenv'],
        'awsssm': ['boto3'],
    },
)
