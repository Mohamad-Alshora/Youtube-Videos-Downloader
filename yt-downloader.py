import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import yt_dlp
import imageio_ffmpeg

def get_ffmpeg_path():
    return imageio_ffmpeg.get_ffmpeg_exe()


def choose_path():
    folder = filedialog.askdirectory()
    if folder:
        path_label.config(text=folder)


def download_video():
    url = url_entry.get()
    save_path = path_label["text"]
    is_audio = audio_var.get()

    if not url.strip():
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    if save_path == "No save location selected":
        messagebox.showerror("Error", "Please choose a save location.")
        return

    def run_download():
        try:
            status_label.config(text="⏳ Downloading...")

            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'ffmpeg_location': get_ffmpeg_path(),
            }

            if is_audio:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'bestvideo*+bestaudio[acodec^=mp4a]/best',
                    'merge_output_format': 'mp4',
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_label.config(text="✅ Download completed!")
            messagebox.showinfo("Success", "Download successful!")

        except Exception as e:
            status_label.config(text="❌ Error during download")
            messagebox.showerror("Error", str(e))

    threading.Thread(target=run_download).start()


# GUI setup
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x300")
root.resizable(False, False)

tk.Label(root, text="YouTube URL:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(root, width=60)
url_entry.pack()

tk.Button(root, text="Choose save location", command=choose_path).pack(pady=10)
path_label = tk.Label(root, text="No save location selected", fg="gray")
path_label.pack()

audio_var = tk.BooleanVar()
tk.Checkbutton(root, text="Audio only (MP3)", variable=audio_var).pack(pady=5)

tk.Button(
    root,
    text="Start Download",
    command=download_video,
    bg="#1DB954",
    fg="white",
    font=("Arial", 12)
).pack(pady=10)

status_label = tk.Label(root, text="", fg="green")
status_label.pack()

root.mainloop()
