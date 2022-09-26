# Description

---
## Prerequisites
The Twitter blocked in some countries including Russia, so
because of this I created Twitter Screenshot TelegramBot

---
## Usage

You send twitter's post link, enter <b>twit depth</b> (how many twits in branch to include),
bot will parse twit and reply you with screenshots

---
### Docker

Everything is very simple! Just edit `.env` file with your environment variables
and run docker-compose with command:

``docker-compose up``

### Python

Create virtual environment: `python3 -m venv env`

Install requirements: `env/bin/python -m pip install -r requirements.txt`

export env variables with `export` command

Run bot: `env/bin/python -m src.cmd.main`

