# Whisper FastAPI Microservice

Этот микросервис реализован с использованием FastAPI и OpenAI Whisper для автоматической транскрипции аудиофайлов. Микросервис принимает аудиофайл через HTTP POST-запрос, выполняет его транскрипцию и возвращает результат в формате JSON.

## Оглавление

- [Требования](#требования)
- [Установка и запуск локально](#установка-и-запуск-локально)
- [Запуск с помощью Docker](#запуск-с-помощью-docker)
- [Использование](#использование)
- [Пример запроса](#пример-запроса)
- [Поддерживаемые форматы аудио](#поддерживаемые-форматы-аудио)
- [Информация о моделях Whisper](#информация-о-моделях-whisper)

## Требования

Для запуска микросервиса требуются:

- Python 3.9+
- Установленный [FFmpeg](https://ffmpeg.org/download.html) для декодирования аудио
- Установленный [Docker](https://docs.docker.com/get-docker/) (для запуска в контейнере)

## Установка и запуск локально

### 1. Клонирование репозитория

```bash
git clone <repository_url>
cd Whisper_Fastapi_Service
```

### 2. Создание и активация виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # для Linux/MacOS
# или
venv\Scripts\activate  # для Windows
```

### 3. Установка зависимостей

```bash
pip install -r app/requirements.txt
```

### 4. Запуск приложения

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Убедитесь, что сервис доступен по адресу

```bash
    http://127.0.0.1:8000
```

## Запуск с помощью Docker

### 1. Построение Docker-образа

```bash
docker build -t my_microservice .
```

### 2. Запуск Docker-контейнера

```bash
docker run -d -p 80:80 my_microservice
```

### 3. Доступ к сервису

После запуска микросервис будет доступен по адресу:

```bash
http://localhost:80
```

## Использование

### Эндпоинт для загрузки аудио и выбора модели Whisper

#### `POST /transcribe/`

Этот эндпоинт принимает аудиофайл и название модели Whisper для транскрипции.

- **URL**: `/transcribe/`
- **Метод**: `POST`
- **Формат данных**: `multipart/form-data`
- **Параметры**:
  - `file`: аудиофайл (обязательный)
  - `whisper_model`: название модели Whisper для использования (обязательный). Доступные модели: `tiny`, `base`, `small`, `medium`, `large`, `turbo`.

#### Пример запроса

```bash
curl -X POST "http://127.0.0.1:8000/transcribe/" \
    -F "file=@/path/to/audiofile.ogg" \
    -F "whisper_model=base"
```

#### Пример ответа

```json
{
  "transcription": "This is the transcribed text from the audio file."
}
```

## 📝 API documentation

- SWAGGER-UI - `/docs/`
- REDOC - `/redoc/`

## Поддерживаемые форматы аудио

Микросервис поддерживает следующие форматы аудиофайлов:

- `audio/mpeg` (MP3)
- `audio/wav` (WAV)
- `audio/x-wav` (WAV)
- `audio/flac` (FLAC)
- `audio/ogg` (OGG)

Убедитесь, что файл имеет один из поддерживаемых форматов перед отправкой запроса.

## Информация о моделях Whisper

Модели Whisper различаются по размеру, количеству параметров, поддерживаемым языкам, требуемой видеопамяти (VRAM) и скорости обработки. Выберите модель в зависимости от ваших требований к точности и времени обработки:

| Model   | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|---------|------------|--------------------|--------------------|---------------|----------------|
| tiny    | 39 M       | `tiny.en`          | `tiny`             | ~1 GB         | ~10x           |
| base    | 74 M       | `base.en`          | `base`             | ~1 GB         | ~7x            |
| small   | 244 M      | `small.en`         | `small`            | ~2 GB         | ~4x            |
| medium  | 769 M      | `medium.en`        | `medium`           | ~5 GB         | ~2x            |
| large   | 1550 M     | N/A                | `large`            | ~10 GB        | 1x             |
| turbo   | 809 M      | N/A                | `turbo`            | ~6 GB         | ~8x            |

- **Relative speed**: Относительная скорость обработки модели. Модели с большей относительной скоростью (`10x`, `7x`) обрабатывают аудио быстрее, чем более точные модели, такие как `large` (`1x`).
- **Required VRAM**: Требуемый объём видеопамяти для использования модели. Большие модели, такие как `large`, требуют до 10 ГБ видеопамяти.

## [Планы развития микросервиса](https://github.com/NewalexOA/Whisper_Fastapi_Service/blob/main/Docs/Fufture_updates.md)
