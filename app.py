import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def fetch_video_info(url):
    """Fetch video information and available formats."""
    try:
        print(f"Fetching video info for URL: {url}")  # Debugging print
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        print(f"Video info fetched: {info}")  # Debugging print
        return info
    except yt_dlp.utils.DownloadError as e:
        messagebox.showerror("Error", f"Failed to fetch video info: {e}")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return None

def fetch_and_display_formats():
    """Fetch available formats and display them in the dropdown."""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    info = fetch_video_info(url)
    if not info:
        print("No video info returned.")  # Debugging print
        return

    # Populate the quality dropdown
    formats = info.get('formats', [])
    print("Raw formats:", formats)  # Debugging print
    if not formats:
        print("No formats found.")  # Debugging print
        messagebox.showerror("Error", "No formats found for this video.")
        return

    # Include all formats for testing
    quality_options = [
        f"{fmt.get('format_note', 'Unknown')} | {fmt['ext']} | {fmt['format_id']}"
        for fmt in formats
    ]
    if not quality_options:
        print("No video formats available.")  # Debugging print
        messagebox.showerror("Error", "No video formats available.")
        return

    # Populate the dropdown menu
    quality_var.set("")
    quality_menu['menu'].delete(0, 'end')
    for option in quality_options:
        quality_menu['menu'].add_command(label=option, command=tk._setit(quality_var, option))
    print("Formats successfully fetched and displayed.")  # Debugging print

def download_video():
    """Download the selected video quality and merge it with audio."""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    selected_quality = quality_var.get()
    if not selected_quality:
        messagebox.showerror("Error", "Please select a quality.")
        return

    # Extract format ID from the selected quality
    format_id = selected_quality.split(" | ")[-1]

    # Ask the user for the save location
    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showinfo("Cancelled", "Download cancelled.")
        return

    try:
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': f"{format_id}+bestaudio",  # Download selected video format + best audio
            'merge_output_format': 'mp4',  # Ensure the output is in MP4 format
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Video downloaded successfully with audio!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def download_audio():
    """Download audio-only."""
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    # Ask the user for the save location
    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showinfo("Cancelled", "Download cancelled.")
        return

    try:
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'format': 'bestaudio',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Audio downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_ui():
    """Create the main UI."""
    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("600x500")

    # Add UI elements
    tk.Label(root, text="Enter YouTube URL:").pack(pady=10)
    global url_entry
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    tk.Button(root, text="Fetch Formats", command=fetch_and_display_formats).pack(pady=10)

    tk.Label(root, text="Select Quality:").pack(pady=10)
    global quality_var, quality_menu
    quality_var = tk.StringVar(root)
    quality_menu = tk.OptionMenu(root, quality_var, "")
    quality_menu.pack(pady=5)

    tk.Button(root, text="Download Video", command=download_video).pack(pady=10)
    tk.Button(root, text="Download Audio Only", command=download_audio).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_ui()