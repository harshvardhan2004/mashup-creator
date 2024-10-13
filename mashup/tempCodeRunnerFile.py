
if __name__ == "__main__":
    query = "Sharry Mann"
    num_videos = 20
    recipient_email = "harshvardhn06@gmail.com"  # Replace with the recipient's email

    video_files = download_videos(query, num_videos)
    cut_audio_files = cut_audio(video_files)
    merged_file = merge_audio(cut_audio_files)
    zip_file = zip_file(merged_file)
    send_email(zip_file, recipient_email)
    os.remove(zip_file)  # Clean up the zip file after sending

    print("Process completed successfully!")