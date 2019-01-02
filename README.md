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

4. Prepare the configuration files and log files

Create new log files:

```bash
mkdir -p triggerbot/log
touch triggerbot/log/info.log
touch triggerbot/log/errors.log
```

Create the configuration files from the example files:

```bash
mv triggerbot/config/config.yml.example triggerbot/config/config.yml
mv triggerbot/config/logging.yml.example triggerbot/config/logging.yml
```

Then edit both files to suit your needs using your favorite editor (*eg* `nano`):

```bash
nano triggerbot/config/config.yml
```

```bash
nano triggerbot/config/logging.yml
```

5. Start the script

```bash
triggerbot
```

You may include `LOGGING=DEBUG` before the `triggerbot` command to enable debugging.

```bash
LOGGING=DEBUG triggerbot
```
