# GCP Log

## Install and config

### Cloud Logging

`pip install google-cloud-logging`

** Logs Writer 角色 **: https://cloud.google.com/logging/docs/setup/python

### Auth 说明

参照 `google.auth`的认证方式:


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

