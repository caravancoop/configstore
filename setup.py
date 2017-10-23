from setuptools import setup

long_description = '''
configstore is a small pluggable library that lets you retrieve settings
or secrets from a variety of storage systems to configure your app.
'''

setup(
    name='configstore',
    version='0.2',
    description='Retrieve config from different backends',
    long_description=long_description,
    url='https://github.com/caravancoop/configstore',
    author='Antoine Reversat',
    author_email='antoine@caravan.coop',
    packages=[
        'configstore', 'configstore.backends',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    extras_require={
        # This does not depend on django in any way
        'dotenv': ['django-dotenv'],
    },
)
