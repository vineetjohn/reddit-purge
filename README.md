# Reddit Purge

Python script to overwrite and delete personal comments on reddit.com.

Written after the forced profile format change (December, 2017).

## Pre-requisites

* Python
* [uv](https://docs.astral.sh/uv/)

## Usage

* Create a reddit app ([Link](https://www.reddit.com/prefs/apps/))

* Clone this repository

```bash
git clone https://github.com/vineetjohn/reddit-purge && cd reddit-purge
```

* Install dependencies

```bash
uv sync
```

* Add reddit user and app credentials to the ```config/credentials.json``` file

* Run script using

```bash
uv run comments_purge --credential-file-path config/credentials.json
```

* Profit?
