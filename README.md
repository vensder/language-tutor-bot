# Telegram English Tutor Bot

This is a simple English Tutor Bot which can help you to enrich your vocabulary and can help to learn phrases and pronunciation.

It is pretty easy to use it: just send the word or sentence to the Telegram channel, where is your bot added. And bot will translate it and will add the audio file to the telegram channel.

The audio file has the structure:

`<the phrase in studying language>, 
<the phrase in your native language>, 
<the slow phrase in studying language>`

## Run The Bot

Clone the repo:

```sh
git clone https://github.com/vensder/telegram-english-tutor.git
```

Add the Python 3 virtual environment and install the modules:

```sh
cd telegram-english-tutor
virtualenv -p python3 env
source ./env/bin/activate
pip install -r requirements.txt
```

To run the bot just rename `example.config.py` file to `config.py` and replace the fake Telegram Bot API token with the real one. 

```sh
mv example.config.py config.py
./main.py
```

How to create the bot and how to obtain the token, check out here: https://core.telegram.org/bots/api

Also put the language codes into the config, corresponding to your native language and learning language. You can check them out here: https://cloud.google.com/translate/docs/languages

The benefit of having the audio files in the telegram group is that you can listen to all audio on your mobile device even if you are walking. The telegram media player will play all of them in the group.

Later you can delete all of them and add the new ones.

## Some screenshots

![Telegram bot 01](./img/mobile01.jpg?raw=true)

![Telegram bot 02](./img/mobile02.jpg?raw=true)

![Telegram bot 03](./img/desktop01.png?raw=true)
