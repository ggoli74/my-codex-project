# Real-time Speech Translation to English (Whisper)

This project provides a Python script that continuously listens to your microphone, detects the spoken language automatically, transcribes it, and prints the English translation to the console.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## Run (single command)

```bash
python realtime_translate.py
```

### Optional flags

- `--model small` (default: `small`)
- `--chunk-seconds 5`
- `--sample-rate 16000`
- `--device <name_or_index>`

Example:

```bash
python realtime_translate.py --model base --chunk-seconds 4
```

## Notes

- Whisper auto-detects language from each chunk.
- Translation output is always English (`task="translate"`).
- For best recognition, use a decent microphone and minimal background noise.
