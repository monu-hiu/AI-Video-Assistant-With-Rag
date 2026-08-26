import yt_dlp
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import os
import re

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def extract_video_id(url: str) -> str:
    """Pull the YouTube video ID out of any common URL format."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from URL: {url}")


def get_transcript_text(url: str) -> str | None:
    """
    Try to fetch an existing YouTube transcript (free, no download needed).
    Returns the joined transcript text, or None if unavailable.
    """
    try:
        video_id = extract_video_id(url)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join(segment["text"] for segment in transcript_list)
        return text
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print(f"Transcript fetch failed, will fall back to audio download: {e}")
        return None


def download_youtube_audio(url: str) -> str:
    """Fallback: download audio via yt-dlp when no transcript is available."""
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["ios", "android", "web"],
                "jsi": ["nodejs"]
            }
        },
        "retries": 3,
        "sleep_interval_requests": 2,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    filename = os.path.splitext(filename)[0] + ".wav"

    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Expected output file not found after download: {filename}"
        )

    return filename


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # 16kHz
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str):
    """
    For YouTube URLs: try transcript first (free, fast, no bot-detection risk).
    If no transcript exists, fall back to downloading + chunking audio for Whisper.
    Returns either a transcript string OR a list of audio chunk paths —
    check the type in your calling code, or adapt this to always return
    a consistent shape depending on your RAG pipeline's needs.
    """
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Trying transcript API first...")
        transcript = get_transcript_text(source)

        if transcript:
            print("Transcript found — skipping audio download entirely.")
            return {"type": "transcript", "text": transcript}

        print("No transcript available. Falling back to audio download...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return {"type": "audio_chunks", "chunks": chunks}
