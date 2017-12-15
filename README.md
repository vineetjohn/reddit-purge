# Reddit Purge

Python script to overwrite and delete personal comments on Reddit.com
Written after of the forced profile format change (December, 2017)

## Pre-requisites

* Python
* Pip

## Usage

* Create a reddit app ([Link](https://www.reddit.com/prefs/apps/))

* Clone this repository

```bash
clone https://github.com/v1n337/reddit-purge.git
cd reddit-purge
```

* Install dependencies

```bash
pip install -r requirements.txt
```

* Add reddit user and app credentials to the ```config/credentials.json``` file

* Run script using

```bash
python comments_purge.py --credential-file-path config/credentials.json
```
