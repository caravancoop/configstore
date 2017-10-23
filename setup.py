from setuptools import setup

setup(
    name='configstore',
    version='0.1',
    description='Retrieve config from different backends',
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
    zip_safe=False,
)
