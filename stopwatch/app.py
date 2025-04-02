import tkinter as tk
from tkinter import ttk
import time

class StopwatchApp:
    def __init__(self, root):
        # Initialize variables
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.lap_times = []

        # GUI setup
        root.title("Stopwatch")
        root.geometry("400x550")
        root.resizable(False, False)

        # Modern dark theme colors
        self.bg_color = "#1e1e2e"  # Dark background
        self.fg_color = "#ffffff"  # White text
        self.accent_color = "#ff6f61"  # Vibrant coral accent
        self.button_color = "#2e2e3e"  # Darker button background
        self.highlight_color = "#ff9e80"  # Lighter coral for highlights
        self.hover_color = "#ff8566"  # Hover effect color

        root.configure(bg=self.bg_color)

        # Modern fonts
        self.time_font = ("Consolas", 36, "bold")
        self.button_font = ("Verdana", 12, "bold")
        self.lap_font = ("Courier New", 12)

        # Elapsed time display
        self.time_label = tk.Label(root, text="00:00:00.00", font=self.time_font, fg=self.accent_color, bg=self.bg_color)
        self.time_label.pack(pady=20)

        # Circular buttons
        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.pack(pady=20)

        self.start_button = self.create_circular_button(self.button_frame, "Start", self.start_stop, 100, 100)
        self.lap_button = self.create_circular_button(self.button_frame, "Lap", self.record_lap, 100, 100)
        self.reset_button = self.create_circular_button(self.button_frame, "Reset", self.reset, 100, 100)

        # Rounded list box with scrollbar
        self.lap_frame = tk.Frame(root, bg=self.bg_color)
        self.lap_frame.pack(pady=20)

        self.lap_listbox = tk.Listbox(self.lap_frame, font=self.lap_font, height=10, width=40, bg=self.button_color, fg=self.fg_color, highlightbackground=self.accent_color, highlightthickness=1, selectbackground=self.highlight_color, relief="flat")
        self.lap_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(self.lap_frame, orient=tk.VERTICAL, command=self.lap_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lap_listbox.config(yscrollcommand=self.scrollbar.set)

        # Keyboard shortcuts
        root.bind("<space>", lambda event: self.start_stop())
        root.bind("<Return>", lambda event: self.record_lap())
        root.bind("<BackSpace>", lambda event: self.reset())

        # Update the timer display
        self.update_timer()

    def create_circular_button(self, parent, text, command, width, height):
        """Create a circular button with hover effects."""
        canvas = tk.Canvas(parent, width=width, height=height, bg=self.bg_color, highlightthickness=0)
        canvas.pack(side=tk.LEFT, padx=10)

        # Draw a circle
        circle = canvas.create_oval(5, 5, width - 5, height - 5, fill=self.accent_color, outline="")
        canvas.tag_bind(circle, "<Button-1>", lambda event: command())
        canvas.tag_bind(circle, "<Enter>", lambda event: canvas.itemconfig(circle, fill=self.hover_color))
        canvas.tag_bind(circle, "<Leave>", lambda event: canvas.itemconfig(circle, fill=self.accent_color))

        # Add text to the circle
        label = canvas.create_text(width // 2, height // 2, text=text, font=self.button_font, fill=self.fg_color)
        canvas.tag_bind(label, "<Button-1>", lambda event: command())
        canvas.tag_bind(label, "<Enter>", lambda event: canvas.itemconfig(circle, fill=self.hover_color))
        canvas.tag_bind(label, "<Leave>", lambda event: canvas.itemconfig(circle, fill=self.accent_color))

        # Store references for dynamic updates
        canvas.circle = circle
        canvas.label = label
        canvas.text = text
        return canvas

    def update_button_text(self, button, text):
        """Update the text of a circular button."""
        button.itemconfig(button.label, text=text)

    def start_stop(self):
        if not self.running:
            # Start the stopwatch
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.update_button_text(self.start_button, "Stop")
        else:
            # Stop the stopwatch
            self.running = False
            self.elapsed_time = time.time() - self.start_time
            self.update_button_text(self.start_button, "Start")

    def record_lap(self):
        if self.running:
            # Record the current cumulative lap time
            current_time = time.time() - self.start_time
            self.lap_times.append(current_time)
            formatted_lap_time = self.format_time(current_time)
            self.lap_listbox.insert(tk.END, f"Lap {len(self.lap_times)}: {formatted_lap_time}")

    def reset(self):
        # Reset the stopwatch
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.lap_times = []
        self.time_label.config(text="00:00:00.00")
        self.lap_listbox.delete(0, tk.END)
        self.update_button_text(self.start_button, "Start")  # Reset button text to "Start"

    def update_timer(self):
        if self.running:
            # Update the elapsed time display
            current_time = time.time() - self.start_time
            self.time_label.config(text=self.format_time(current_time))
        else:
            # Display the last recorded elapsed time
            self.time_label.config(text=self.format_time(self.elapsed_time))
        # Schedule the next update
        self.time_label.after(50, self.update_timer)

    @staticmethod
    def format_time(seconds):
        # Format time as HH:MM:SS.ss
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02}:{int(minutes):02}:{seconds:05.2f}"

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()