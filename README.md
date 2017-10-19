configstore
===========

This module accepts many backends and tries to read the config value from all of them in the order they are defined.

The main pain point this tries to solve is :

Assume you have your config in environment variables but you want to store your secrets in something else.
How do you mix having a secret backend for your secrets but still keep everything else in environment variables ?
With this module you can use both. Let's say you use DATABASE_PASSWORD as your database password env variable.
This will first try to find this in your first backend (let's say docker secrets) and if it fails will fall back on the env variable.


See ```example.py``` for some example code.
