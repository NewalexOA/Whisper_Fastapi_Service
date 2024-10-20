from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import whisper
import tempfile
import os
import logging

app = FastAPI()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Доступные модели Whisper
available_models = ["tiny", "base", "small", "medium", "large", "turbo"]

class TranscriptionResponse(BaseModel):
    transcription: str

@app.post("/transcribe/", response_model=TranscriptionResponse)
async def transcribe(
    file: UploadFile = File(...), 
    whisper_model: str = Form(...)  # Переименовали model_name в whisper_model
) -> TranscriptionResponse:
    # Проверка наличия аудиофайла
    if file.content_type not in ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/flac", "audio/mp3", "audio/ogg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file.")

    # Проверка названия модели
    if whisper_model not in available_models:
        raise HTTPException(status_code=400, detail=f"Invalid model name. Available models: {', '.join(available_models)}")

    try:
        # Загрузка выбранной модели
        logger.info(f"Loading Whisper model: {whisper_model}")
        model = whisper.load_model(whisper_model)

        # Сохранение загруженного аудиофайла во временный файл
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_filename = tmp.name

        logger.info(f"Processing file: {tmp_filename}")

        # Транскрипция аудиофайла с помощью Whisper
        result = model.transcribe(tmp_filename)
        transcription = result["text"]
        logger.info("Transcription successful")

    except Exception as e:
        logger.error(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    finally:
        # Удаление временного файла
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)
            logger.info(f"Temporary file {tmp_filename} removed")

    # Возвращаем транскрипцию в виде JSON
    return TranscriptionResponse(transcription=transcription)
