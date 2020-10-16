#!/usr/bin/env python

from telegram.ext import Updater, MessageHandler
from googletrans import Translator
from gtts import gTTS
import config
import os

token = config.token
learning_lang = config.learning_language
native_lang = config.native_language

audio_dir = "audio"

translator = Translator()


def translate(text):
    transcription = None
    definitions = None
    examples = None
    detected_lang = translator.detect(text).lang
    if detected_lang == learning_lang:
        tr = translator.translate(text, dest=native_lang, src=learning_lang)
        if len(text.split()) == 1:
            if (
                "translation" in tr.extra_data
                and len(tr.extra_data["translation"][1]) > 3
            ):
                transcription = "[{}]".format(tr.extra_data["translation"][1][3])
            if "definitions" in tr.extra_data and tr.extra_data["definitions"]:
                definitions = tr.extra_data["definitions"][0][1]
            if "examples" in tr.extra_data and tr.extra_data["examples"]:
                examples = tr.extra_data["examples"][0]
    else:
        tr = translator.translate(text, dest=learning_lang, src=detected_lang)
    return tr.src, tr.dest, tr.text, transcription, definitions, examples


class TutorMeIt:
    def __init__(self, passed_text):
        (
            source_lang,
            dest_lang,
            translation,
            transcription,
            definitions,
            examples,
        ) = translate(passed_text)
        if source_lang == learning_lang:
            self.text = passed_text
            self.textLang = source_lang
            self.otherText = translation
            self.otherTextLang = dest_lang
        else:
            self.text = translation
            self.textLang = dest_lang
            self.otherText = passed_text
            self.otherTextLang = source_lang
        self.transcription = transcription
        self.definitions = definitions
        self.examples = examples


def send_audio(update, context):
    repeat_it = TutorMeIt(update.message.text)
    audio_path = f"{audio_dir}/{repeat_it.text}_{repeat_it.otherTextLang}.mp3"
    if not os.path.isfile(audio_path):
        tts_learning_lang = gTTS(repeat_it.text, lang=repeat_it.textLang)
        tts_other_lang = gTTS(repeat_it.otherText, lang=repeat_it.otherTextLang)
        tts_learning_lang_slow = gTTS(
            repeat_it.text, lang=repeat_it.textLang, slow=True
        )
        with open(audio_path, "wb") as f:
            tts_learning_lang.write_to_fp(f)
            tts_other_lang.write_to_fp(f)
            tts_learning_lang_slow.write_to_fp(f)

    caption = f"{repeat_it.text} {repeat_it.transcription}\n[{repeat_it.otherTextLang}]: {repeat_it.otherText}"
    if repeat_it.definitions:
        for definition in repeat_it.definitions:
            if len(caption + f"\n\n* {definition[0]}") <= 1024:
                caption += f"\n\n* {definition[0]}"
    if repeat_it.examples:
        if (
            len(
                caption
                + "\n\nExamples:"
                + f"\n\n* {repeat_it.examples[0][0]}".replace("<b>", "").replace(
                    "</b>", ""
                )
            )
            <= 1024
        ):
            caption += "\n\nExamples:"
            for example in repeat_it.examples:
                if (
                    len(
                        caption
                        + f"\n\n* {example[0]}".replace("<b>", "").replace("</b>", "")
                    )
                    <= 1024
                ):
                    caption += f"\n\n* {example[0]}".replace("<b>", "").replace(
                        "</b>", ""
                    )

    update.message.reply_audio(
        audio=open(audio_path, "rb"),
        quote=False,
        caption=caption,
    )

    del repeat_it


updater = Updater(token, use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(None, send_audio))

updater.start_polling()
updater.idle()
