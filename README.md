🖥️ Safe Keyboard Event Recorder

A safe, transparent, and ethical keyboard event recorder built using Python and Tkinter.
This tool records keystrokes only inside its own visible window and only when the user explicitly clicks Start Recording.
It does NOT run in the background, does NOT capture system-wide keys, and is intended purely for educational and UI testing purposes.

🚀 Features

✔️ Records key presses only when the app window is focused

✔️ Start / Stop / Save / Clear controls

✔️ Visible real-time log display

✔️ Saves logs to a text file

✔️ 100% ethical & legal (no hidden/global keylogging)

✔️ Uses only built-in Python libraries (no external dependencies)

📂 Project Structure
safe_keyrecorder.py
README.md
key_events_log.txt (generated after saving)

🛠️ Requirements

Python 3.7+

Tkinter (bundled with Python)

No installation of external packages needed.

▶️ How to Run

Make sure Python is installed

Save the script as:

safe_keyrecorder.py


Run it:

python safe_keyrecorder.py

🎮 How to Use

Open the program

Click Start Recording

Click inside the large text box and start typing

View your captured keystrokes in the log pane below

Click Save Log to save them to a .txt file

Click Stop Recording anytime

Use Clear to reset the log display

📝 Log Format

Each recorded entry contains:

timestamp | keysym | character


Example:

2025-11-17T12:45:30.321Z | a | a
2025-11-17T12:45:31.002Z | BackSpace | <non-printable>
2025-11-17T12:45:32.110Z | space |  

🔒 Ethical & Safety Notes

This program:

❗does NOT capture keys outside the app

❗does NOT run in background

❗does NOT hide itself

✔️ is safe for demos, research, and learning

This is not a keylogger.
It is a keyboard event recorder confined to its own window, designed for safe usage.

📜 License

This project is free to use for educational purposes.

💡 Want More Features?

I can add:

CSV export

Typing speed (WPM) statistics

Visual charts

Auto-save feature

Light/Dark themes

Just tell me what you want!