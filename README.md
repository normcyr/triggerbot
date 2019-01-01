# Reddit Trigger Bot

Bot that will reply a canned answer upon being triggered by a keyword.

## Requirements

- praw
- PyYAML

Details are found in `requirements.txt`.


## To install

1. Clone the repository

```bash
git clone git@github.com:normcyr/triggerbot.git
```

2. Create and activage a Python 3 virtual environment

```bash
cd triggerbot
virtualenv -p python3 venv
source venv/bin/activate
```

3. Install the triggerbot module

The requirements are included in the `setup.py` file.

```bash
pip install -e .
```

4. Start the script

```bash
triggerbot
```

You may include `LOGGING=DEBUG` before the `triggerbot` command to enable debugging.

```bash
LOGGING=DEBUG triggerbot
```
