import os
import uuid

from fastapi import APIRouter, UploadFile, File

from app.services.stt import speech_to_text

router = APIRouter()

UPLOAD_DIR = "temp_audio"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)

@router.post("/voice")

async def voice_upload(
    audio: UploadFile = File(...)
):

    filename = (
        str(uuid.uuid4())
        + ".webm"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    with open(
        filepath,
        "wb",
    ) as f:

        f.write(
            await audio.read()
        )

    text = speech_to_text(
        filepath
    )

    os.remove(
        filepath
    )

    return {
        "text": text
    }