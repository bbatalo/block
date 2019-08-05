# Block


[![PyPI](https://img.shields.io/badge/pypi-0.0.3-blue.svg)](https://pypi.org/project/block-hosts/0.0.3/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Block is a simple Python-based command line utility for blocking access to web sites in order to stop you from procrastinating, because you can't do it by yourself. Relies on modifying the hosts file.

## Installing

It is possible to install Block using the Python package manager, pip:

```
$ pip install block-hosts
```

## Usage

The simplest and most common usage of Block is to block all sites in a curated list. To do this, run the following command in the console:

```
$ block-hosts block-all
```

and to unblock, run:

```
$ block-hosts unblock-all
```

To block a profile of web sites, such as "social" or "news", run:

```
$ block-hosts block-profile PROFILE_NAME
```

and to unblock, run:

```
$ block-hosts unblock-profile PROFILE_NAME
```

To block a single web site, run:

```
$ block-hosts WEBSITE_URL
```

where *website_url* refers to, you guessed it, the URL of the website you want to block. To reverse the action, run

```
$ block-hosts unblock WEBSITE_URL
```

Note: modifying the hosts file requires administrator privileges, so make sure that the terminal is in elevated mode.

Another note: you might need to restart the browser for changes to take effect.