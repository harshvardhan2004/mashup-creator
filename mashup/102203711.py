#pip install --upgrade pytube moviepy pydub yt-dlp

# line no 72 ->put sender_email address
#         73 -> put sender_email password
#         102 -> put recipient_email address

import os
import yt_dlp
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def download_videos(query, num_videos):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{num_videos}:{query}", download=False)['entries']
        videos = []
        for entry in search_results:
            try:
                info = ydl.extract_info(entry['webpage_url'], download=True)
                filename = ydl.prepare_filename(info).replace('.webm', '.mp3')
                videos.append(filename)
                print(f"Successfully downloaded: {filename}")
            except Exception as e:
                print(f"Error downloading video: {entry.get('title', 'Unknown title')}")
                print(f"Error details: {str(e)}")
    return videos


def cut_audio(audio_files):
    processed_files = []
    for audio in audio_files:
        try:
            sound = AudioSegment.from_mp3(audio)
            cut_sound = sound[30000:]  # Cut first 30 seconds (30000 milliseconds)
            output_file = f"cut_{audio}"
            cut_sound.export(output_file, format="mp3")
            processed_files.append(output_file)
            os.remove(audio)  # Remove the original file
        except Exception as e:
            print(f"Error processing audio for: {audio}")
            print(f"Error details: {str(e)}")
    return processed_files

def merge_audio(audio_files):
    combined = AudioSegment.empty()
    for audio in audio_files:
        sound = AudioSegment.from_mp3(audio)
        combined += sound
        os.remove(audio)  # Remove individual audio files after merging
    output_file = "merged_sharry_mann.mp3"
    combined.export(output_file, format="mp3")
    return output_file


def zip_file(file_to_zip):
    zip_filename = "sharry_mann_audio.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(file_to_zip, arcname=os.path.basename(file_to_zip))
    os.remove(file_to_zip)  # Remove the unzipped merged file
    return zip_filename

def send_email(zip_file, recipient_email):
    sender_email = "sender@gmail.com"  # Replace with your email
    password = "pwd"  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Sharry Mann Audio Compilation"

    with open(zip_file, "rb") as file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(file.read())
    
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {zip_file}")
    msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)


if __name__ == "__main__":
    query = "Sharry Mann"
    num_videos = 20
    recipient_email = "recipient@gmail.com"  # Replace with the recipient's email

    video_files = download_videos(query, num_videos)
    cut_audio_files = cut_audio(video_files)
    merged_file = merge_audio(cut_audio_files)
    zip_file = zip_file(merged_file)
    send_email(zip_file, recipient_email)
    os.remove(zip_file)  # Clean up the zip file after sending

    print("Process completed successfully!")