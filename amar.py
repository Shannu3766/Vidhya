from deep_translator import GoogleTranslator

# Define the word and target language
word = "hello"  # Spanish word for "Hello"
target_language = "ta"  # Translate to English

# Translate using Google Translator
translation = GoogleTranslator(source='auto', target=target_language).translate(word)

# Print the original word and the translated word
print(f"Original word: {word}")
print(f"Translated word: {translation.encode('utf-8')}")
