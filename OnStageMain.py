import tkinter as tk
from tkinter import filedialog
from pychordpro import chordpro
import pychordpro

class PrompterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Panel")
        
        self.secondary = tk.Toplevel(root)
        self.secondary.title("Stage Display")
        
        # Fullscreen the secondary display
        self.secondary.attributes('-fullscreen', True)
        self.secondary.configure(bg='black')
        
        self.current_lyrics = tk.StringVar()
        self.current_chords = tk.StringVar()
        self.current_tempo = tk.IntVar(value=120)
        
        # Control panel UI
        tk.Label(root, text="Enter Lyrics:").pack()
        self.lyrics_entry = tk.Entry(root, textvariable=self.current_lyrics)
        self.lyrics_entry.pack()
        tk.Label(root, text="Enter Chords:").pack()
        self.chords_entry = tk.Entry(root, textvariable=self.current_chords)
        self.chords_entry.pack()
        tk.Label(root, text="Enter Tempo (BPM):").pack()
        self.tempo_entry = tk.Entry(root, textvariable=self.current_tempo)
        self.tempo_entry.pack()
        tk.Button(root, text="Display", command=self.display_content).pack()
        tk.Button(root, text="Load ChordPro File", command=self.load_chordpro).pack()
        
        # Secondary display UI
        self.canvas = tk.Canvas(self.secondary, highlightthickness=0, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.lyrics_label = tk.Label(self.secondary, text="", font=("Helvetica", 32), fg="white", bg="black")
        self.chords_label = tk.Label(self.secondary, text="", font=("Helvetica", 24), fg="yellow", bg="black")
        
        self.lyrics_window = self.canvas.create_window(0, 0, window=self.lyrics_label, anchor='center')
        self.chords_window = self.canvas.create_window(0, 0, window=self.chords_label, anchor='center')

        self.canvas.bind('<Configure>', self.resize_labels)
        
        self.update_tempo()
        
    def resize_labels(self, event):
        width = event.width
        height = event.height
        
        self.canvas.coords(self.lyrics_window, width / 2, height / 2 - 40)
        self.canvas.coords(self.chords_window, width / 2, height / 2 + 40)
    
    def display_content(self):
        lyrics = self.current_lyrics.get()
        chords = self.current_chords.get()
        self.lyrics_label.config(text=lyrics)
        self.chords_label.config(text=chords)
    
    def update_tempo(self):
        bpm = self.current_tempo.get()
        self.root.after(60000 // bpm, self.blink_tempo)
        
    def blink_tempo(self):
        self.canvas.delete("border")
        width = self.secondary.winfo_width()
        height = self.secondary.winfo_height()
        border_thickness = 20
        
        current_color = self.canvas.cget("highlightbackground")
        next_color = "red" if current_color == "black" else "black"
        
        # Top border
        self.canvas.create_rectangle(0, 0, width, border_thickness, fill=next_color, outline="", tag="border")
        # Bottom border
        self.canvas.create_rectangle(0, height - border_thickness, width, height, fill=next_color, outline="", tag="border")
        # Left border
        self.canvas.create_rectangle(0, 0, border_thickness, height, fill=next_color, outline="", tag="border")
        # Right border
        self.canvas.create_rectangle(width - border_thickness, 0, width, height, fill=next_color, outline="", tag="border")
        
        self.canvas.config(highlightbackground=next_color)
        
        bpm = self.current_tempo.get()
        self.root.after(60000 // bpm, self.blink_tempo)

    def load_chordpro(self):
        file_path = filedialog.askopenfilename(filetypes=[("ChordPro files", "*.pro *.chopro")])
        if not file_path:
            return

        with open(file_path, 'r') as file:
            content = file.read()

        parsed_song = content

        lyrics = []
        chords = []
        for line in parsed_song:
            for element in line:
                if isinstance(element, pychordpro.Song.dump_chords):
                    chords.append(f"[{element.name}]")
                if isinstance(element, ):
                    lyrics.append(element.text)
        
        self.current_lyrics.set(' '.join(lyrics))
        self.current_chords.set(' '.join(chords))
        self.display_content()

if __name__ == "__main__":
    root = tk.Tk()
    app = PrompterApp(root)
    root.mainloop()
