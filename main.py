#!/usr/bin/env python3

import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from googletrans import Translator
from gtts import gTTS

# Configure logging
logging_level = os.getenv('LOGGING_LEVEL', 'INFO')
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.getLevelName(logging_level),
)
logger = logging.getLogger(__name__)

# Environment variables
telegram_token = os.getenv('TELEGRAM_TOKEN')
learning_lang = os.getenv('LEARNING_LANGUAGE', 'en')  # Default to English
native_lang = os.getenv('NATIVE_LANGUAGE', 'en')      # Default to English
audio_dir = "/tmp"

async def translate(text):
    """Translate text and extract transcription, definitions, and examples."""
    transcription = ""
    definitions = None
    examples = None
    try:
        async with Translator() as translator:
            tr = await translator.translate(text, dest=native_lang, src=learning_lang)
        if len(text.split()) == 1:
            if (
                hasattr(tr, "extra_data")
                and tr.extra_data
                and "translation" in tr.extra_data
                and isinstance(tr.extra_data["translation"], list)
                and len(tr.extra_data["translation"]) > 1
                and isinstance(tr.extra_data["translation"][1], list)
                and len(tr.extra_data["translation"][1]) > 3
            ):
                transcription = "[{}]".format(tr.extra_data["translation"][1][3])
            if (
                hasattr(tr, "extra_data")
                and tr.extra_data
                and "definitions" in tr.extra_data
                and tr.extra_data["definitions"]
            ):
                definitions = tr.extra_data["definitions"][0][1]
            if (
                hasattr(tr, "extra_data")
                and tr.extra_data
                and "examples" in tr.extra_data
                and tr.extra_data["examples"]
            ):
                examples = tr.extra_data["examples"][0]
        return tr.src, tr.dest, tr.text, transcription, definitions, examples
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise

class TutorMeIt:
    """Class to handle text, translation, and metadata."""
    def __init__(self, passed_text, translation_data):
        (
            source_lang,
            dest_lang,
            translation,
            transcription,
            definitions,
            examples,
        ) = translation_data
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

async def send_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages, generate audio, and send it back."""
    try:
        translation_data = await translate(update.message.text)
        repeat_it = TutorMeIt(update.message.text, translation_data)
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
                if repeat_it.definitions:
                    for definition in repeat_it.definitions:
                        tts_definition = gTTS(definition[0], lang=repeat_it.textLang)
                        tts_definition.write_to_fp(f)
                if repeat_it.examples:
                    tts_some_examples = gTTS("Some examples.", lang=learning_lang)
                    tts_some_examples.write_to_fp(f)
                    for example in repeat_it.examples:
                        tts_example = gTTS(
                            example[0].replace("<b>", "").replace("</b>", ""),
                            lang=repeat_it.textLang,
                        )
                        tts_example.write_to_fp(f)

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

        # Send audio to Telegram
        with open(audio_path, "rb") as audio:
            await context.bot.send_audio(
                chat_id=update.message.chat_id,
                audio=audio,
                caption=caption,
                title=repeat_it.text if len(repeat_it.text) < 18 else repeat_it.text[:18] + "…",
            )

        # Clean up audio file
        try:
            os.remove(audio_path)
        except Exception as e:
            logger.warning(f"Failed to delete audio file {audio_path}: {str(e)}")

    except Exception as e:
        logger.error(f"Error in send_audio: {str(e)}")
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Error processing your request: {str(e)}"
        )

if __name__ == '__main__':
    if not telegram_token:
        logger.error("TELEGRAM_TOKEN environment variable is not set")
        exit(1)

    # Create the Application instance
    application = Application.builder().token(telegram_token).build()

    # Add handler for text messages (ignores commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_audio))

    # Start polling
    logger.info("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
