# Reddit Purge

Python script to overwrite and delete personal comments on reddit.com.

Written after the forced profile format change (December, 2017).

## Pre-requisites

* Python
* [Poetry](https://python-poetry.org/docs/#installation)

## Usage

* Create a reddit app ([Link](https://www.reddit.com/prefs/apps/))

* Clone this repository

```bash
git clone https://github.com/vineetjohn/reddit-purge && cd reddit-purge
```

* Install dependencies

```bash
poetry install
```

* Add reddit user and app credentials to the ```config/credentials.json``` file

* Run script using

```bash
poetry run comments_purge --credential-file-path config/credentials.json
```

* Profit?
