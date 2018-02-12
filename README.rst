~~~~~~~~~~~~~
 configstore
~~~~~~~~~~~~~

This module accepts many backends and tries to read the config value from all of them in the order they are defined.

The main pain point this tries to solve is:

Assume you have your config in environment variables but you want to store your secrets in something else.
How do you mix having a secret backend for your secrets but still keep everything else in environment variables?
With this module you can use both. Let's say you use ``DATABASE_PASSWORD`` as your database password env variable.
This will first try to find this in your first backend (let's say docker secrets) and if it fails will fall back on the env variable.


See ``example.py`` for some example code.


Available backends
------------------

configstore.EnvVarBackend finds settings in environment variables.  This is the classic
12-factor approach, which main drawback is that it's easy for outside tools or sub-processes
to inspect the environment and access sensitive data.  This backend is still useful for
settings that are not secrets.

configstore.DockerSecretBackend can read `Docker secrets`_.
This is a secure storage with first-class support in the Docker runtime and related
tooling.

configstore.DotenvBackend lets you put settings in a key-value format file, using the
`dotenv module`_, which is useful for local development.
This backend requires an optional dependency, so use a requirement like ``configstore[dotenv]``
to get everything installed.

.. _docker secrets: https://docs.docker.com/engine/swarm/secrets/
.. _dotenv module: https://github.com/jpadilla/django-dotenv


Contributors
------------

Original author: Antoine Reversat @crevetor

Current maintainer: Éric Araujo @merwok

Project sponsored by Caravan Coop @caravancoop
