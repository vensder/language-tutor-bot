# Telegram Language Tutor Bot

This is a simple Language Tutor Bot which can help you to enrich your vocabulary and can help to learn phrases and pronunciation.

Actually you can learn any language and can have any native language - the bot is multilingual.

It is pretty easy to use it: just send the word or sentence to the Telegram channel, where is your bot added. And bot will translate it and will add the audio file to the telegram channel.

The audio file has the structure:

`<the phrase in studying language>, 
<the phrase in your native language>, 
<the slow phrase in studying language>`

If you send one word only and if the translation module returns the definitions and/or examples of the word, this text will be added to the audio file as well.

## Run The Bot

Clone the repo:

```sh
git clone https://github.com/vensder/language-tutor-bot.git
```

Add the Python 3 virtual environment and install the modules:

```sh
cd language-tutor-bot
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

Once you remember them, you can delete them and add new ones.
