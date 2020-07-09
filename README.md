# GCP Log

## Install and config

``` Shell
pip install gcp-mixed-logging
or 
pip install -i https://pypi.org/project gcp-mixed-logging
```

### Cloud Logging

**Logs Writer**: https://cloud.google.com/logging/docs/setup/python

### Fluentd

TODO

## Usage

``` Python
from gcp_mixed_logging import MixedLogging

# using on GCE with local fluent
log = MixedLogging('module', stage='prod')

# using with credential and remote fluent host
log = MixedLogging(
    'module', stage='prod',
    fluent_host='ip or dns', fluent_port=24224,
    project='project-id', credentials=Credentials(),
    )

# cloud logging: plain text
log.debug("this is a debug message")
log.info("this is a info message")
log.warn("this is a warn message")
log.error("this is a error message")

# cloud logging: struct message
log.info({
    "user": "Mark",
    "age": 25
})

# fluent:
# 1. time append to log
# 2. send to fluent with tag: 'module-prod.user-info'
log.persist("user-info", {
    "user": "Mark",
    "age": 25
})

```

## More

### Auth 说明

Refer to `google.auth`:


1. If the environment variable ``GOOGLE_APPLICATION_CREDENTIALS`` is set
    to the path of a valid service account JSON private key file, then it is
    loaded and returned. The project ID returned is the project ID defined
    in the service account file if available (some older files do not
    contain project ID information).
2. If the `Google Cloud SDK`_ is installed and has application default
    credentials set they are loaded and returned.

    To enable application default credentials with the Cloud SDK run::

        `gcloud auth application-default login`

    If the Cloud SDK has an active project, the project ID is returned. The
    active project can be set using::

        `gcloud config set project`

3. If the application is running in the `App Engine standard environment`_
    then the credentials and project ID from the `App Identity Service`_
    are used.
4. If the application is running in `Compute Engine`_ or the
    `App Engine flexible environment`_ then the credentials and project ID
    are obtained from the `Metadata Service`_.
5. If no credentials are found,
    :class:`~google.auth.exceptions.DefaultCredentialsError` will be raised.

