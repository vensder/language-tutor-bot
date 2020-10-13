# Telegram English Tutor Bot

This is a simple English Tutor Bot which can help you to enrich your vocabulary and can help to learn phrases and pronunciation.

It is pretty easy to use it: just send the word or sentence to the Telegram channel, where is your bot added. And bot will translate it and will add the audio file to the telegram channel.

The audio file has the structure:

`<the phrase in studying language>, 
<the phrase in your native language>, 
<the slow phrase in studying language>`

## Run The Bot

To run the bot just rename `example.config.py` file to `config.py` and replace the fake Telegram Bot API token with the real one. 

How to create the bot and how to obtain the token, check out here: https://core.telegram.org/bots/api

Also put the language codes into the config, corresponding to your native language and learning language. You can check them out here: https://cloud.google.com/translate/docs/languages

The benefit of having the audio files in the telegram group is that you can listen to all audio on your mobile device even if you are walking. The telegram media player will play all of them in the group.

Later you can delete all of them and add the new ones.
