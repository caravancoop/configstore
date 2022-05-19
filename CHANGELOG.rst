~~~~~~~~~~~~~~~~~~~~~~~~~~~
 changelog for configstore
~~~~~~~~~~~~~~~~~~~~~~~~~~~


v0.8
====

Test with Python 3.9 and Python 3.10.
Support interpolation with more than one variable.


v0.7
====

Add asbool param to get_setting.
Add DictBackend for tests or defaults.


v0.6.1
======

Make get_setting support non-string default values.


v0.6
====

Add interpolation for settings.


v0.5
====

Package library with flit.


v0.4
====

New backend to get config from AWS SSM Parameter Store.


v0.3
====

Added Store.add_backend method.


v0.2
====

Introducing Store class with configurable backends instead of function.


v0.1
====

First release!

The get_config function finds values in environment variables
or Docker secrets.
