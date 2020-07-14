try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os.path

BASE_PATH = os.path.dirname(__file__)

with open(os.path.join(BASE_PATH, "README.md")) as readme:
    long_description = readme.read()


setup(
    name="gcp-mixed-logging",
    version="0.0.6",
    description="write log to cloud logging or fluentd, for app in gcp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="wb",
    author_email="wbin.chn@gmail.com",
    maintainer="wbchn",
    maintainer_email="wbin.chn@gmail.com",
    url="https://github.com/wbchn/gcp-mixed-logging",
    download_url='http://pypi.python.org/pypi/gcp-mixed-logging/',
    package_dir={'gcp_mixed_logging': 'gcp_mixed_logging'},
    packages=["gcp_mixed_logging"],
    python_requires=">=3.5.3",
    install_requires=["google-cloud-logging>=1.15.0", "fluent-logger>=0.9.6"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "coverage", "pytest-cov"],
    test_suite='tests',
)
