IEEE-TEC-Bot
==================
![Some informative photo goes here](photo.png)![photo](photo.png)   
| Release        | Master           | Develop  |
| ------------- |-------------| -----|
|[![Github All Releases](https://img.shields.io/github/release/TEComputerIEEE/IEEE-TEC-Bot.svg)](https://github.com/TEComputerIEEE/IEEE-TEC-Bot)     | [![Travis Build Status](https://travis-ci.org/TEComputerIEEE/IEEE-TEC-Bot.svg?branch=master)](https://github.com/TEComputerIEEE/IEEE-TEC-Bot)  | [![Travis Build Status](https://travis-ci.org/TEComputerIEEE/IEEE-TEC-Bot.svg?branch=develop)](https://github.com/TEComputerIEEE/IEEE-TEC-Bot) |    
Telegram Bot for the TEC's Branch of the IEEE. With this bot you can......**Features go here**.......

## Getting Started

The last stable version of the bot is up and running, you can search it on Telegram's search bar under the name **the final bot name goes here**. This repo can be clone to get the latest source code version of the app with the command:
```
git clone https://github.com/TEComputerIEEE/IEEE-TEC-Bot.git
```

### Prerequisites
If you wish to develop or test your own version of the bot, you'll have to install the following prerequisites. **Pd: installation notes are for debian based systems with apt installed, but you can use your own package manager**.     
#### Python 3 and Pip
If you don't have python installed you can install it by typing into a terminal:
```
sudo apt get install python3 python3-pip
pip3 install --upgrade pip setuptools
```
#### Pip Quick Install
Since we have a [requirements.txt](requirements.txt) file with the requirements, you can simply install all with:
```
pip install -r requirements.txt --user
```
You can also install them in a [virtual enviroment](https://virtualenv.pypa.io/en/stable/userguide/#usage).
Other way is install each of them manually:
##### Python-telegram-bot wrapper
This bot is based on [python-telegram-bot wrapper](https://github.com/python-telegram-bot/python-telegram-bot), you can install it with:
```
pip3 install python-telegram-bot --upgrade --user
```
##### Request-Cache
To improve response time, the request responses are [cached](https://github.com/reclosedev/requests-cache/blob/master/docs/user_guide.rst):
```
pip3 install requests-cache --upgrade --user
```
##### Schedule
To do task periodically this bot uses [schedule](https://github.com/dbader/schedule):
```
pip3 install schedule --upgrade --user
```

Also as we're using our own API, you'll have to make a API. See [IEEE-TEC-WebAPI](https://github.com/TEComputerIEEE/IEEE-TEC-WebAPI) if you need a example.

## Running the tests
**Unit test howto**

## Deployment
To deploy your own version of the bot. You need to follow the telegram bot creation [steps](https://core.telegram.org/bots#3-how-do-i-create-a-bot). And create a config.py file with your private info, as this one:

```
#API KEYs
TELAPIKEY = ""
WEBAPIKEY = ""
#Config parameters
Logging = True
cacheTime = 1 #In hours
clearCacheTime = "23:00" # the time when the clear cache function will be called
webApiAddr = "http://httpbin.org"
#Default Messages
startReply = "Bienvenido al Bot de IEEE Computer Society TEC"
unrecognizedReply = "Comando invalido, por favor utilice el teclado especial."
```

This is not the [best way](https://medium.freecodecamp.org/how-to-securely-store-api-keys-4ff3ea19ebda) to handle your key, but for now it will do.

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning
Given a version number MAJOR.MINOR.PATCH, increment the:

* MAJOR version when you make incompatible API changes,
* MINOR version when you add functionality in a backwards-compatible manner, and
* PATCH version when you make backwards-compatible bug fixes.

For the versions available, see the [tags on this repository](https://github.com/TEComputerIEEE/IEEE-TEC-Bot/tags). 

## Authors
The leading developers involved in this project can be found in this list. For further details, you can go to the [contributors graph](https://github.com/TEComputerIEEE/IEEE-TEC-Bot/graphs/contributors).
* [**Full Name**](Github Profile Link) - *Role* - [IEEE-TEC-Bot](https://github.com/TEComputerIEEE/IEEE-TEC-Bot)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
**Here some Acknowledgements**
