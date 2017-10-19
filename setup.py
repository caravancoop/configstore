from setuptools import setup

setup(name='configstore',
      version='0.1',
      description='Retrieve config from different backends',
      url='https://github.com/caravancoop/configstore.git',
      author='Antoine Reversat',
      author_email='antoine@caravan.coop',
      license='MIT',
      packages=['configstore'],
      test_suite='nose.collector',
      test_require=['nose'],
      zip_safe=False)
