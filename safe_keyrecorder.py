"""
Safe Keyboard Event Recorder (educational / UI testing)

- Records keys only while this app's window is focused AND recording is active.
- Visible GUI with Start / Stop / Save / Clear buttons.
- Saves a timestamped log to a plain text file.
- No background/global keylogging; does NOT capture keystrokes outside the app window.

Usage:
    python safe_keyrecorder.py
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os

DEFAULT_LOGFILE = "key_events_log.txt"

class SafeKeyRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Safe Key Recorder")
        self.root.geometry("700x420")
        self.recording = False
        self.events = []  # list of (timestamp, keysym, char)

        # Top controls
        control_frame = tk.Frame(root)
        control_frame.pack(fill="x", padx=8, pady=6)

        self.start_btn = tk.Button(control_frame, text="Start Recording", command=self.start_recording)
        self.start_btn.pack(side="left", padx=4)

        self.stop_btn = tk.Button(control_frame, text="Stop Recording", command=self.stop_recording, state="disabled")
        self.stop_btn.pack(side="left", padx=4)

        self.save_btn = tk.Button(control_frame, text="Save Log", command=self.save_log)
        self.save_btn.pack(side="left", padx=4)

        self.clear_btn = tk.Button(control_frame, text="Clear", command=self.clear_events)
        self.clear_btn.pack(side="left", padx=4)

        self.open_btn = tk.Button(control_frame, text="Open Log File", command=self.open_log_file)
        self.open_btn.pack(side="left", padx=4)

        # Recording indicator
        self.status_label = tk.Label(control_frame, text="Recording: No", fg="red")
        self.status_label.pack(side="right", padx=6)

        # Info / instructions
        info = tk.Label(root, text="Instructions: Click 'Start Recording', then click inside the input area below and type.\n"
                                   "Only keys typed while this window and input box are focused will be recorded.",
                        justify="left")
        info.pack(fill="x", padx=8)

        # Input area where keys will be recorded
        self.text_frame = tk.Frame(root, bd=2, relief="sunken")
        self.text_frame.pack(fill="both", expand=True, padx=8, pady=6)

        self.text_widget = tk.Text(self.text_frame, wrap="word", height=12)
        self.text_widget.pack(fill="both", expand=True)
        # Ensure text widget can receive focus
        self.text_widget.focus_set()

        # Bottom pane to show recorded events (readonly)
        bottom_label = tk.Label(root, text="Recorded events (most recent at bottom):")
        bottom_label.pack(anchor="w", padx=8)

        self.log_display = tk.Text(root, height=8, state="disabled", bg="#f9f9f9")
        self.log_display.pack(fill="both", expand=False, padx=8, pady=(0,8))

        # Bind key events to text_widget (only when it has focus)
        self.text_widget.bind("<KeyPress>", self.on_key_press)

        # Ensure we ask user before closing if unsaved events exist
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_label.config(text="Recording: Yes", fg="green")
        self._append_message("Recording started. Click inside input area and type...")

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="Recording: No", fg="red")
        self._append_message("Recording stopped.")

    def on_key_press(self, event):
        """
        This handler runs only when the text_widget has focus (so keys
        typed elsewhere are NOT captured). We record the event only if
        recording is active.
        """
        if not self.recording:
            return  # ignore key events when not recording

        # Gather safe, human-readable info
        timestamp = datetime.utcnow().isoformat() + "Z"  # UTC timestamp
        keysym = event.keysym  # e.g., 'a', 'Return', 'BackSpace', 'Shift_L'
        char = event.char  # actual character if printable, else empty string

        # Normalize char for control keys
        if char == "":
            char_repr = "<non-printable>"
        else:
            # replace newline with explicit label for readability
            char_repr = char.replace("\n", "\\n")

        self.events.append((timestamp, keysym, char_repr))
        self._append_to_display(f"{timestamp} | {keysym} | {char_repr}")

    def _append_to_display(self, text):
        self.log_display.config(state="normal")
        self.log_display.insert("end", text + "\n")
        self.log_display.see("end")
        self.log_display.config(state="disabled")

    def _append_message(self, msg):
        # messages go to display (not saved as keystrokes)
        self._append_to_display(f"[INFO] {datetime.utcnow().isoformat()}Z | {msg}")

    def save_log(self):
        if not self.events:
            messagebox.showinfo("Save Log", "No recorded events to save.")
            return

        # Ask the user where to save
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=DEFAULT_LOGFILE,
            title="Save key event log as..."
        )
        if not path:
            return  # user cancelled

        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"# Key event log saved: {datetime.utcnow().isoformat()}Z\n")
                for ts, keysym, ch in self.events:
                    f.write(f"{ts}\t{keysym}\t{ch}\n")
                f.write("\n")
            messagebox.showinfo("Save Log", f"Saved {len(self.events)} events to:\n{path}")
            self._append_message(f"Saved {len(self.events)} events to {os.path.basename(path)}")
            # Optionally clear recorded events after saving
            # self.events.clear()
        except Exception as e:
            messagebox.showerror("Save Log", f"Failed to save file:\n{e}")

    def open_log_file(self):
        # Let user pick an existing log to open for reading (no editing)
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Open log file..."
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Show content in a temporary read-only dialog
            top = tk.Toplevel(self.root)
            top.title(f"Viewing: {os.path.basename(path)}")
            txt = tk.Text(top, wrap="word")
            txt.insert("1.0", content)
            txt.config(state="disabled")
            txt.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Open Log", f"Failed to open file:\n{e}")

    def clear_events(self):
        if not self.events and self.log_display.compare("end-1c", "==", "1.0"):
            return
        if messagebox.askyesno("Clear", "Clear recorded events and display?"):
            self.events.clear()
            self.log_display.config(state="normal")
            self.log_display.delete("1.0", "end")
            self.log_display.config(state="disabled")
            self._append_message("Cleared recorded events.")

    def on_close(self):
        if self.events:
            if not messagebox.askyesno("Exit", "There are unsaved recorded events. Exit without saving?"):
                return
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SafeKeyRecorder(root)
    root.mainloop()
