import os
from os import path
import importlib.metadata
from typing import BinaryIO, Union

import numpy as np
import ffmpeg
from fastapi import FastAPI, File, UploadFile, Query, applications
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from whisper import tokenizer

from typing import Union
from io import BytesIO

ASR_ENGINE = os.getenv("ASR_ENGINE", "openai_whisper")
if ASR_ENGINE == "faster_whisper":
    from .faster_whisper.core import transcribe, language_detection
else:
    from .openai_whisper.core import transcribe, language_detection

SAMPLE_RATE=16000
LANGUAGE_CODES=sorted(list(tokenizer.LANGUAGES.keys()))

projectMetadata = importlib.metadata.metadata('whisper-asr-webservice')
app = FastAPI(
    title=projectMetadata['Name'].title().replace('-', ' '),
    description=projectMetadata['Summary'],
    version=projectMetadata['Version'],
    contact={
        "url": projectMetadata['Home-page']
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    license_info={
        "name": "MIT License",
        "url": projectMetadata['License']
    }
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173"  # Add other allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allowed HTTP headers
)

@app.post("/asr", tags=["Endpoints"])
def asr(
    task : Union[str, None] = Query(default="transcribe", enum=["transcribe", "translate"]),
    language: Union[str, None] = Query(default=None, enum=LANGUAGE_CODES),
    initial_prompt: Union[str, None] = Query(default=None),
    audio_file: UploadFile = File(...),
    encode : bool = Query(default=True, description="Encode audio first through ffmpeg"),
    output : Union[str, None] = Query(default="txt", enum=["txt", "vtt", "srt", "tsv", "json"]),
    word_timestamps : bool = Query(
        default=False, 
        description="World level timestamps", 
        include_in_schema=(True if ASR_ENGINE == "faster_whisper" else False)
    )
):
    # Process the audio file and obtain the result
    result = transcribe(load_audio(audio_file.file, encode), task, language, initial_prompt, word_timestamps, output)
    
    data = result.getvalue()

    # Create a JSON response with both the filename and result data
    response_data = {
        'filename':  f'{audio_file.filename}.{output}',
        'result': data
    }

    # Close the StringIO object
    result.close()

    return JSONResponse(content=response_data)

@app.post("/detect-language", tags=["Endpoints"])
def detect_language(
    audio_file: UploadFile = File(...),
    encode : bool = Query(default=True, description="Encode audio first through ffmpeg")
):
    detected_lang_code = language_detection(load_audio(audio_file.file, encode))
    return { "detected_language": tokenizer.LANGUAGES[detected_lang_code], "language_code" : detected_lang_code }

def load_audio(file: BinaryIO, encode=True, sr: int = SAMPLE_RATE):
    """
    Open an audio file object and read as mono waveform, resampling as necessary.
    Modified from https://github.com/openai/whisper/blob/main/whisper/audio.py to accept a file object
    Parameters
    ----------
    file: BinaryIO
        The audio file like object
    encode: Boolean
        If true, encode audio stream to WAV before sending to whisper
    sr: int
        The sample rate to resample the audio if necessary
    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    if encode:
        try:
            # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
            # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
            out, _ = (
                ffmpeg.input("pipe:", threads=0)
                .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
                .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=file.read())
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e
    else:
        out = file.read()

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
