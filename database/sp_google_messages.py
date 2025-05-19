import logging
import time
import os
import pickle
from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPIError, InvalidArgument


class MessageConfig:
    def __init__(self, idiom="ENG", api_key=None, cache_duration=3600, cache_file="translation_cache.pkl",
                 environment="development"):
        self.idiom = idiom
        self.api_key = api_key
        self.cache_duration = cache_duration  # Duration in seconds for cache expiration
        self.cache_file = cache_file  # File to persist the cache
        self.translate_client = translate.Client() if api_key else None
        self.messages = {
            "ENG": {
                "ERR-001": "ERR-001: Access information provided is incorrect.",
                "ERR-002": "ERR-002: User information provided is incorrect.",
                "SUC-001": "SUC-001: Operation completed successfully.",
                "WARN-001": "WARN-001: This is a warning message.",
                "INFO-001": "INFO-001: This is an informational message."
            }
        }
        self.translation_cache = self.load_cache()
        self.setup_logging(environment)

    def setup_logging(self, environment):
        if environment == "development":
            logging_level = logging.DEBUG
        elif environment == "production":
            logging_level = logging.ERROR
        else:
            logging_level = logging.INFO

        logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler("message_config.log"),
                                logging.StreamHandler()
                            ])

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                try:
                    return pickle.load(f)
                except (pickle.UnpicklingError, EOFError):
                    logging.warning("Failed to load cache file. Starting with an empty cache.")
                    return {}
        return {}

    def save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.translation_cache, f)
        logging.info("Cache saved to disk.")

    def translate_message(self, message, target_language):
        if not self.translate_client:
            logging.error("Translation client is not initialized. Please provide a valid API key.")
            return message  # Fallback to the original message

        # Check if translation is already cached and still valid
        cache_key = (message, target_language)
        current_time = time.time()
        if cache_key in self.translation_cache:
            cached_translation, timestamp = self.translation_cache[cache_key]
            if current_time - timestamp < self.cache_duration:
                logging.info(f"Using cached translation for message '{message}' in language '{target_language}'")
                return cached_translation
            else:
                logging.info(f"Cache expired for message '{message}' in language '{target_language}'")
                del self.translation_cache[cache_key]  # Remove expired cache

        try:
            result = self.translate_client.translate(message, target_language=target_language)
            translated_text = result['translatedText']

            # Cache the translation with the current timestamp
            self.translation_cache[cache_key] = (translated_text, current_time)
            logging.info(f"Translated and cached message '{message}' in language '{target_language}'")
            self.save_cache()  # Save cache to disk after each new translation

            return translated_text
        except GoogleAPIError as e:
            logging.error(f"Google API error: {e.message}")
            return message  # Fallback to the original message
        except InvalidArgument as e:
            logging.error(f"Invalid argument error: {e.message}")
            return message  # Fallback to the original message
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return message  # Fallback to the original message

    def get_message(self, code):
        if self.idiom == "ENG":
            return self.messages["ENG"].get(code, f"Message code {code} not found.")

        message_in_english = self.messages["ENG"].get(code, f"Message code {code} not found.")
        translated_message = self.translate_message(message_in_english, target_language=self.idiom)
        return translated_message


# Usage example:
# Replace 'your-api-key' with your actual Google Cloud API key
config = MessageConfig(idiom="lt", api_key='your-api-key', cache_duration=7200, environment="production")
msg_err_01 = config.get_message("ERR-001")
msg_suc_01 = config.get_message("SUC-001")
msg_warn_01 = config.get_message("WARN-001")
msg_info_01 = config.get_message("INFO-001")

print(msg_err_01)
print(msg_suc_01)
print(msg_warn_01)
print(msg_info_01)
