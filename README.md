# GCP Mixed Log

GCP Mixed Log 提供了统一的日志/数据接口, 在开发中代替 Python logging 及 Fluent-logging, 并附加额外信息规范化数据.

## Getting started

### Installing from PyPI
``` Shell
pip install gcp-mixed-logging
```

### Cloud Logging

使用到了Python 版 Cloud Logging 库, 权限配置参见[官方文档](https://cloud.google.com/logging/docs/setup/python#using_the_cloud_client_library_directly)

> Tips:
> 在本地和其他位置运行时, 需要使用Service Account或下方Auth说明中的第2种方法.


### Fluentd

支持持久化日志转发至 Fluentd 或 Fluent Bit.

Fluentd / Fluent Bit安装方法参见:
- [Fluentd](https://docs.fluentd.org/)
- [Fluent Bit](https://docs.fluentbit.io/manual/)

## API

### Summary

**class gcp_mixed_logging.MixedLogging**

> `from gcp_mixed_logging import MixedLogging`

members:
- cloudlogging_name: Cloud Loging path
- is_alive: is alive

|method|abount|
|---|---|
|close()|停止接收日志, 缓存中日志写入Cloud Logging / Fluentd|
|debug(msg)|诊断日志, msg: str or dict|
|info(msg)|msg: str or dict|
|warning(msg)|msg: str or dict|
|error(msg)|msg: str or dict|
|metric(..)|todo|
|persist(tag, msg)|持久化日志, 转发至Fluent|

#### MixedLogging(module: str, stage: str...)
**Param**:

 - module: str: Module or sub-module name
 - stage: str: stage, dev/test/prod/...
 - fluent_host: str = 'localhost', fluentd host ip or dns
 - fluent_port: int = 24224, fluentd forward port
 - project: str = None, project name, if none, read from default auth
 - scopes: Optional[Collection[str]] = _DEFAULT_SCOPESS, scopes for default auth
 - resource: Resource = _GLOBAL_RESOURCE, resource of cloud logging

#### debug/info/warning/error(msg: Any)
> Send message to Cloud Logging in background thread, append information:
> - labels: module/stage/host
> - jsonPaylod: filename/function/lineno of caller frame
**Param**:
  msg: Any, text or dict message

#### persist(tag: str, msg: dict, track: bool = False, track_severity: str = "DEFAULT", **kw)
> Foward message to Fluent in background thread, append information:
> - host/timestamps
> - insert_id: increment intger per tag per host

**Param**:
 - tag: str, tag name for fluent
 - msg: dict, payload data in dict type
 - track: bool = False, both track to cloud logging
 - track_severity: str = "DEFAULT", severity of cloud logging

### Example

``` Python
from gcp_mixed_logging import MixedLogging

# using on GCE with local fluent
log = MixedLogging('module', stage='prod')

# using with credential and remote fluent host
log = MixedLogging(
    'module', stage='prod',
    fluent_host='ip or dns', fluent_port=24224,
    project='project-id'
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

# foward log to fluent and cloud logging
log.persist("user-info", {
    "user": "Mark",
    "age": 25
}, track=True)

```

## More

### Google Auth

Refer to `google.auth`:

1. If the environment variable ``GOOGLE_APPLICATION_CREDENTIALS`` is set to the path of a valid service account JSON private key file, then it is loaded and returned. The project ID returned is the project ID defined in the service account file if available (some older files do not contain project ID information).
2. If the `Google Cloud SDK`_ is installed and has application default credentials set they are loaded and returned.

    To enable application default credentials with the Cloud SDK run: `gcloud auth application-default login`
    
    If the Cloud SDK has an active project, the project ID is returned. The active project can be set using: `gcloud config set project`

3. If the application is running in the `App Engine standard environment` then the credentials and project ID from the `App Identity Service` are used.
4. If the application is running in `Compute Engine` or the `App Engine flexible environment` then the credentials and project ID are obtained from the `Metadata Service`.
5. If no credentials are found,
    :class:`~google.auth.exceptions.DefaultCredentialsError` will be raised.

