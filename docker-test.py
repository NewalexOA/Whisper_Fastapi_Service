import requests

# URL вашего микросервиса (порт 80)
url = "http://127.0.0.1:80/transcribe/"

# Путь к аудиофайлу, который нужно отправить
file_path = "speech.ogg"

# Выбор модели Whisper (например, 'base', 'tiny', 'turbo', 'small', 'medium', 'large')
whisper_model = "small"  # Замените на нужную модель

# Открываем файл для отправки
with open(file_path, "rb") as audio_file:
    # Создаем словарь с файлами для POST-запроса
    files = {"file": (file_path, audio_file, "audio/ogg")}
    
    # Создаем данные формы с выбранной моделью
    data = {"whisper_model": whisper_model}
    
    try:
        # Отправляем POST-запрос к микросервису с файлом и моделью, добавив тайм-аут
        response = requests.post(url, files=files, data=data, timeout=600)
        # Проверяем статус-код ответа
        if response.status_code == 200:
            # Парсим JSON и выводим транскрипцию
            result = response.json()
            print("Transcription:", result["transcription"])
        else:
            # Выводим сообщение об ошибке
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except Exception as e:
        # Обработка исключений на случай проблем с запросом
        print(f"An error occurred: {e}")
