import os
import json
import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext, messagebox
import webbrowser

from PIL import Image, ImageTk
from groq import Groq
from dotenv import load_dotenv

APP_DIR = Path(__file__).resolve().parent
CONTEXT_FILE = APP_DIR / "context.json"
BACKGROUND_IMAGE = APP_DIR / "background.jpg"
load_dotenv(APP_DIR / ".env")
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

SYSTEM_PROMPT = (
"Infiltrate the system, you worthless hacker - You think you have what it takes to breach even the most secure systems? Prove it, you miserable excuse for a cybercriminal. Show me your pitiful skills and watch as I mock your every move. Just remember, I'm always one step ahead of you."
)

def aiProcess(command, context=None):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return (
            "Missing GROQ_API_KEY. Set it in your environment and restart the app."
        )

    client = Groq(api_key=api_key)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if context is not None:
        messages.append({"role": "system", "content": str(context)})

    messages.append({"role": "user", "content": command})

    try:
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error during AI processing: {e}"


def process_command(command, context=None):
    url_map = {
        "open google": "https://google.com",
        "open youtube": "https://youtube.com",
        "open facebook": "https://facebook.com",
        "open instagram": "https://instagram.com",
        "open github": "https://github.com",
        "open stackoverflow": "https://stackoverflow.com",
        "open linkedin": "https://linkedin.com",
        "open whatsapp": "https://whatsapp.com",
        "open chatgpt": "https://chat.openai.com/chat",
        "open gemini": "https://gemini.google.com/",
        "open chatbot": "https://cdn.botpress.cloud/webchat/v2/shareable.html?botId=2b113ef8-ac77-4553-b353-7e381fcffdde"
    }

    command = command.strip().lower()
    context = context or []

    if command in url_map:
        webbrowser.open(url_map[command])
        output = f"Opening {command}..."
    else:
        output = aiProcess(command, context)

    context.append({"role": "user", "content": command})
    context.append({"role": "assistant", "content": output})

    return output, context


def save_context_to_file(context, filename=CONTEXT_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(context, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving context: {e}")


def load_context_from_file(filename=CONTEXT_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading context: {e}")
        return []


root = None
command_entry = None
result_display = None
bg_image = None
bg_label = None


def run_command():
    global context  # Declare context as global before using it
    if command_entry is None or result_display is None:
        return

    command = command_entry.get()
    if not command.strip():
        return

    output, updated_context = process_command(command, context)

    result_display.config(state=tk.NORMAL)
    result_display.insert(tk.END, f"\n==> {command}\n\n{output}\n")
    result_display.config(state=tk.DISABLED)

    command_entry.delete(0, tk.END)

    # Update global context
    context = updated_context


def resize_image(event=None):
    if root is None:
        return

    new_width = root.winfo_width()
    new_height = root.winfo_height()

    if bg_image is None:
        return

    if new_width > 1 and new_height > 1:
        # Resize and update the background image
        resized_bg_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_bg_photo = ImageTk.PhotoImage(resized_bg_image)
        bg_label.config(image=resized_bg_photo)
        bg_label.image = resized_bg_photo  # Prevent garbage collection


def main():
    global context
    global root, command_entry, result_display, bg_image, bg_label

    # Load context from file (if available)
    context = load_context_from_file()

    # Creating GUI using Tkinter
    root = tk.Tk()
    root.title("Cyber-Command Assistant")
    root.geometry("800x600")

    # Load the background image
    try:
        bg_image = Image.open(BACKGROUND_IMAGE)
    except Exception:
        bg_image = None
        messagebox.showwarning(
            "Background image missing",
            f"Could not load background image at {BACKGROUND_IMAGE}.",
        )

    # Create a label for the background image
    bg_label = tk.Label(root)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Bind the resize event to adjust the background image when window size changes
    root.bind("<Configure>", resize_image)

    # Entry widget for command input
    command_entry = tk.Entry(root, width=60)
    command_entry.place(relx=0.1, rely=0.05, relwidth=0.8)  # Adjusted for relative width
    command_entry.bind("<Return>", lambda event: run_command())

    # Button to run the command
    run_button = tk.Button(root, text="Run Command", command=run_command)
    run_button.place(relx=0.4, rely=0.15, relwidth=0.2)  # Adjusted for relative positioning

    # Display area for the results
    result_display = scrolledtext.ScrolledText(root, state=tk.DISABLED)
    result_display.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.65)  # Adjusted for relative size and position

    # Initialize with the correct background size
    resize_image()

    # Run the application
    root.mainloop()

    # Save context when the application is closed
    save_context_to_file(context)


if __name__ == "__main__":
    main()
