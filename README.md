# Installation

## Gitlab CE

To start local gitlab instance run following commands:
```
cd gitlab-ce
docker-compose up
```

Start Docker environment:
```
docker-compose up -d
```
Login to container:
```
docker-compose exec app sh
```
Download requirements:
```
/app # virtualenv venv
/app # . venv/bin/activate
(venv) /app # pip install --upgrade requests
```
# NPM example

Copy `config.py.example` to `config.py`

Create directory for npm tests (NOT INSIDE OF CURRENT POC DIRECTORY):
```
(venv) /app # mkdir /npm-example
```
Create a private token on your Gitlab instance with api scope https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token

Copy private token to `config.py`

Start script and follow the instructions:
```
(venv) /app # python3 create.py
```
Publish test NPM package:
```
(venv) /app # npm publish
```
Switch to `/npm-example` directory and install test package:
```
(venv) /npm-example # npm install @root/test
```

# COMPOSER example

Create directory for composer tests (NOT INSIDE OF CURRENT DIRECTORY):
```
(venv) /app # mkdir /composer-example
(venv) /app # cd /composer-example
```
Run command and follow instruction:
```
(venv) /composer-example # composer init
```
Run Git commands to tag the changes and push them to composer project repository:
```
(venv) /composer-example # git init
(venv) /composer-example # git add composer.json
(venv) /composer-example # git commit -m 'Composer package test'
(venv) /composer-example # git tag v1.0.0
(venv) /composer-example # git remote add origin http://host.docker.internal/poc/testcomposer.git
(venv) /composer-example # git push --set-upstream origin master
(venv) /composer-example # git push origin v1.0.0
```
Start script for upload composer package:
```
(venv) /app # python3 composer-publish.py
```
In order to download composer package create another one directory(NOT INSIDE OF CURRENT DIRECTORY):
```
(venv) /app # mkdir /testcomposer
(venv) /app # cd /testcomposer
```
Create `/testcomposer/composer.json` with data:
```
{}
```
Run:
```
(venv) /testcomposer # composer config repositories.host.docker.internal/<group_id> '{"type": "composer", "url": "http://host.docker.internal/api/v4/group/<group_id>/-/packages/composer/packages.json"}'

(venv) /testcomposer # composer config gitlab-domains host.docker.internal

(venv) /testcomposer # composer config gitlab-token.host.docker.internal <private_token>

(venv) /testcomposer # composer config secure-http false

(venv) /testcomposer # composer req poc/testcomposer:v1.0.0
```

# Delete all tokens

Run:
```
(venv) /app # python3 tokens-delete.py
```
