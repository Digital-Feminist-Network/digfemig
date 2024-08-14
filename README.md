# digfemig

A Python utility to collect up to the top 100 media for a given Instagram hashtag. This utility came out of a research need for the [Digital Feminist Network](https://digfemnet.org/).

## Requirements

* [instagrapi](https://github.com/subzeroid/instagrapi)
* [tomli](https://pypi.org/project/tomli/)

## Usage

```
digfemig example.toml
```

Where you configure a `config.toml` file with your requirements.

How to create a session file:

```python
from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)
cl.dump_settings("session.json")
```

## License

The Unlicense
