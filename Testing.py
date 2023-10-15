import sys
from PyQt6.QtWidgets import QApplication, QFileDialog

app = QApplication([])

audio_file, _ = QFileDialog.getOpenFileName(None, "Select Audio File", "", "MP3 Files (*.mp3);;All Files (*)", options=QFileDialog.options.ReadOnly)

# Check if the selected file is an MP3
if audio_file.endswith('.mp3'):
    print("You selected an MP3 file:", audio_file)
else:
    print("Please select a valid MP3 file.")

app.exec()
