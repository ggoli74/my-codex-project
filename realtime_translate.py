#!/usr/bin/env python3
"""Continuously capture microphone audio, transcribe speech, and print English translations."""

from __future__ import annotations

import argparse
import queue
import tempfile
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf
import whisper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Listen to microphone audio in chunks and print English translations "
            "using OpenAI Whisper."
        )
    )
    parser.add_argument(
        "--model",
        default="small",
        help="Whisper model to use (tiny, base, small, medium, large). Default: small",
    )
    parser.add_argument(
        "--chunk-seconds",
        type=float,
        default=5.0,
        help="Length of each recorded audio chunk in seconds. Default: 5",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="Input sample rate used for recording. Default: 16000",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="Optional microphone device name or index. Default: system default input",
    )
    return parser.parse_args()


def record_chunk(sample_rate: int, chunk_seconds: float, device: str | int | None) -> np.ndarray:
    frames = int(sample_rate * chunk_seconds)
    audio_q: queue.Queue[np.ndarray] = queue.Queue()

    def callback(indata: np.ndarray, _frames: int, _time: object, status: sd.CallbackFlags) -> None:
        if status:
            print(f"[audio warning] {status}")
        audio_q.put(indata.copy())

    chunks: list[np.ndarray] = []
    deadline = time.time() + chunk_seconds
    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        callback=callback,
        blocksize=1024,
        device=device,
    ):
        received = 0
        while received < frames:
            timeout = max(0.1, deadline - time.time())
            try:
                block = audio_q.get(timeout=timeout)
            except queue.Empty:
                continue
            chunks.append(block)
            received += len(block)

    return np.concatenate(chunks, axis=0)[:frames].reshape(-1)


def transcribe_and_translate(model: whisper.Whisper, audio: np.ndarray, sample_rate: int) -> tuple[str, str]:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        wav_path = Path(temp_wav.name)

    try:
        sf.write(str(wav_path), audio, sample_rate)
        detected = model.transcribe(str(wav_path), task="transcribe", fp16=False)
        translated = model.transcribe(str(wav_path), task="translate", fp16=False)
    finally:
        wav_path.unlink(missing_ok=True)

    language = detected.get("language", "unknown")
    english = translated.get("text", "").strip()
    return language, english


def main() -> None:
    args = parse_args()
    model = whisper.load_model(args.model)

    print("\nListening continuously. Press Ctrl+C to stop.")
    print(
        f"Model={args.model}, chunk_seconds={args.chunk_seconds}, "
        f"sample_rate={args.sample_rate}, device={args.device or 'default'}"
    )

    try:
        while True:
            audio = record_chunk(args.sample_rate, args.chunk_seconds, args.device)
            if not np.any(np.abs(audio) > 1e-3):
                continue

            language, english = transcribe_and_translate(model, audio, args.sample_rate)
            if english:
                print(f"[{language}] {english}")
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
