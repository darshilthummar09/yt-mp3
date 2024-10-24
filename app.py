from fastapi import FastAPI, HTTPException, BackgroundTasks
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
import time
app = FastAPI()

def download_and_convert(url: str, output_path: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}.%(ext)s',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    # Convert to MP3 using pydub
    audio = AudioSegment.from_file(filename)
    mp3_filename = output_path + ".mp3"
    audio.export(mp3_filename, format="mp3")

    # Clean up temporary file
    os.remove(filename)

    return mp3_filename

@app.get("/youtube-to-mp3/")
async def youtube_to_mp3(url: str, background_tasks: BackgroundTasks):
    output_path = f"downloads/{url.split('=')[-1]}"
    s_time=time.time()
    try:
        # Run the download and conversion in the background
        background_tasks.add_task(download_and_convert, url, output_path)
        return {"message": "Your download will start soon."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    e_time=time.time()
    print(e_time-s_time)

# To run the server:
# uvicorn main:app --host 0.0.0.0 --port 8000
