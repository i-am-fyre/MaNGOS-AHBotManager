# Web App for Managing the MaNGOS Auction House Bot

A simple web app to display items that are included/excluded in the Auction House bot for MaNGOS servers.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine. Tested on Ubuntu 20.04 WSL.

### Prerequisites

Run the following:
- `sudo apt-get install libmariadb-dev python3-dev`
- `sudo git clone https://github.com/i-am-fyre/MaNGOS-AHBotManager`
- `cd MaNGOS-AHBotManager`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

### Configuration

You can set your database information in `config.ini`.

If you have an existing ahbot.conf, you can place it into the root directory. If you don't, no worries! Saving your configuration within the app will create one for you!

### Starting Up

Once the pre-requisites above have been installed and configurations are set, do the following:
- `export FLASK_APP=main.py`
- `flask run`
Your local server should then be running at http://localhost:5000

If you want to see raw data for all quests, go to: http://localhost:5000/all
