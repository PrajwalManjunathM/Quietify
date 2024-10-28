import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QLabel, QListWidget, QListWidgetItem, QComboBox, QDialog,
    QProgressBar, QTextEdit
)
from PyQt5.QtGui import QIcon , QFont
from PyQt5.QtCore import Qt, QTimer , QSize
from pydub import AudioSegment
import noisereduce as nr
import numpy as np
from scipy.io import wavfile
import librosa
import soundfile as sf
from scipy.signal import butter, filtfilt
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget, QListWidgetItem, QComboBox, QDialog, QProgressBar
from PyQt5.QtGui import QIcon, QFont, QPalette, QLinearGradient, QColor, QBrush
from PyQt5.QtCore import Qt, QTimer, QSize
import librosa
import matplotlib.pyplot as plt
import soundfile as sf
import scipy.fftpack as fft
from scipy.signal import medfilt

# Image usage after exe conversion
# Get the path to the image
if hasattr(sys, '_MEIPASS'):
    # Running from the PyInstaller bundle
    base_path = sys._MEIPASS
else:
    # Running from source
    base_path = os.path.abspath(".")

# Now, you can access the image files
image1_path = os.path.join(base_path, "images", "C:\\Users\\A\\PycharmProjects\\Eveny_planner_GUI\\folder.png")
image2_path = os.path.join(base_path, "images", "C:\\Users\\A\\PycharmProjects\\Eveny_planner_GUI\\images-removebg-preview (1).png")


# Custom styles for the GUI
STYLE_SHEET = """
    QWidget {
        background-color: #66A5AD; 
        font-family: Arial;
        font-size: 14px;
    }

    QLabel {
        color:  #FFFFFF;
        font-size: 18px;
        font-weight: bold;
        qproperty-alignment: 'AlignCenter';
    }


    QListWidget {
        background-color: #F1F1F2;
        color: #000000;
        border: 2px solid #2c3e50;
        padding: 5px;
        font-size: 25px;
    }

    QPushButton {
        background-color: #1995AD;
        color: white;
        font-size: 18px;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #F1F1F2;
        font-size: 18px;
        color: #1995AD;
    }

    QComboBox {
        background-color: #1995AD;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
    }

    QComboBox:hover {
        background-color: #F1F1F2;
        color: #1995AD;
    }

    QComboBox QAbstractItemView {
        background-color: #1995AD;
        color: white;
        border-radius: 10px;
        padding: 5px;
    }
"""


# Utility functions
def audiosegment_to_numpy(audio_segment):
    """
    Convert AudioSegment to numpy array, handling stereo and mono.
    """
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1).astype(np.int16)
    return samples, audio_segment.frame_rate


def numpy_to_audiosegment(samples, frame_rate, channels=1, sample_width=2):
    """
    Convert numpy array back to AudioSegment.
    """
    audio_segment = AudioSegment(
        samples.tobytes(),
        frame_rate=frame_rate,
        sample_width=sample_width,
        channels=channels
    )
    return audio_segment


def process_in_chunks(audio_segment, chunk_size=30000):
    """
    Process audio in chunks to avoid memory overload.
    """
    audio_samples, sample_rate = audiosegment_to_numpy(audio_segment)
    processed_chunks = []
    for i in range(0, len(audio_samples), chunk_size):
        chunk = audio_samples[i:i + chunk_size]
        reduced_chunk = nr.reduce_noise(y=chunk, sr=sample_rate)
        processed_chunks.append(reduced_chunk)
    reduced_audio = np.concatenate(processed_chunks)
    return reduced_audio, sample_rate


def strip(path):
    """
    Check if the file is a .wav file.
    """
    return path.endswith('.wav')

def splt(path):
    s_path = path.split('/')
    l = len(s_path)
    s_path = s_path[l-1]
    s_path = s_path.split('.')
    s_path = s_path[0]
    return s_path

def splt_1(path):
    s_path = path.split('\\')
    l = len(s_path)
    s_path = s_path[l-1]
    s_path = s_path.split('.')
    s_path = s_path[0]
    return s_path


# Dialog classes
class LoadingDialog(QDialog):
    """
    Dialog to show progress during processing.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processing...")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(400, 100)
        layout = QVBoxLayout()
        self.label = QLabel("Processing, please wait...", self)
        layout.addWidget(self.label)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_message(self, message):
        self.label.setText(message)


class UploadOnlyWAV(QDialog):
    """
    Dialog to warn about non-WAV file selection.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERROR - WARNING")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(400, 100)
        layout = QVBoxLayout()
        self.label = QLabel("Upload only WAV file/files", self)
        layout.addWidget(self.label)
        self.setLayout(layout)

class FileEmpty(QDialog):
    """
    Dialog to warn about non-WAV file selection.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERROR - WARNING")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(400, 100)
        layout = QVBoxLayout()
        self.label = QLabel("Folder Empty", self)
        layout.addWidget(self.label)
        self.setLayout(layout)

class InputEmpty(QDialog):
    """
    Dialog to warn about empty input file selection.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERROR - WARNING")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(400, 100)
        layout = QVBoxLayout()
        self.label = QLabel("Please select input file", self)
        layout.addWidget(self.label)
        self.setLayout(layout)


class OutputEmpty(QDialog):
    """
    Dialog to warn about empty output directory selection.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERROR - WARNING")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.resize(400, 100)
        layout = QVBoxLayout()
        self.label = QLabel("Please select output directory", self)
        layout.addWidget(self.label)
        self.setLayout(layout)


# Main GUI Class
class AudioProcessorGUI(QWidget):
    file_path = None
    folder_path = None
    directory = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Apply custom style sheet
        self.setWindowTitle("Quietify")
        self.setStyleSheet(STYLE_SHEET)

        # Layouts
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # Left Section: File/Directory Selection
        self.left_label = QLabel("Select File/Directory:")
        self.left_list = QListWidget()

        # Increase the size of icons and font in the left list
        self.left_list.setIconSize(QSize(64, 64))
        font = QFont()
        font.setPointSize(16)
        self.left_list.setFont(font)

        # Create a dropdown (QComboBox) for file/folder selection
        self.left_dropdown = QComboBox()
        self.left_dropdown.addItem("Select Input type")
        self.left_dropdown.addItem("Select File")
        self.left_dropdown.addItem("Select Folder")
        self.left_dropdown.currentIndexChanged.connect(self.handle_left_selection)

        # Right Section: Output Directory Selection
        self.right_label = QLabel("Select Output Directory:")
        self.right_list = QListWidget()

        # Increase the size of icons and font in the right list
        self.right_list.setIconSize(QSize(64, 64))
        self.right_list.setFont(font)

        self.right_select_button = QPushButton("Select Output Directory")
        self.right_select_button.clicked.connect(self.select_output_directory)

        # Process Audio Button
        self.process_button = QPushButton("Process Audio")
        self.process_button.clicked.connect(self.process_audio)

        # Adding to layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.left_label)
        left_layout.addWidget(self.left_list)
        left_layout.addWidget(self.left_dropdown, alignment=Qt.AlignCenter)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.right_label)
        right_layout.addWidget(self.right_list)
        right_layout.addWidget(self.right_select_button, alignment=Qt.AlignCenter)

        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)

        bottom_layout.addWidget(self.process_button)

        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def handle_left_selection(self):
        selected_option = self.left_dropdown.currentText()
        if selected_option == "Select File":
            self.select_file()
        elif selected_option == "Select Folder":
            self.select_folder()
        elif selected_option == "Select Input type":
            self.left_list.clear()

    def select_file(self):
        self.folder_path = None
        self.left_list.clear()
        # Open a file selection dialog
        selected_file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if selected_file_path:
            self.file_path = selected_file_path
            # Add selected file path to the list
            music_icon = QIcon(image2_path)  # Replace with the path to your music icon
            file_name = self.file_path.split('/')[-1]

            # Create a QListWidgetItem and apply the icon
            item = QListWidgetItem(music_icon, file_name)
            self.left_list.addItem(item)
        else:
            self.file_path = None

    def select_folder(self):
        self.file_path = None
        self.left_list.clear()
        # Open a folder selection dialog
        selected_folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if selected_folder_path:
            self.folder_path = selected_folder_path
            # List files in the selected folder
            self.list_files_in_folder(self.folder_path)
        else:
            self.folder_path = None

    def list_files_in_folder(self, folder_path):
        # Create an icon for the folder
        folder_icon = QIcon(image1_path)  # Replace with the path to your folder icon
        folder_name = folder_path.split('/')[-1]

        # Add folder to the list
        item = QListWidgetItem(folder_icon, folder_name)
        self.left_list.addItem(item)

        # List all files in the folder
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                music_icon = QIcon(image2_path)  # Replace with your music icon path
                item = QListWidgetItem(music_icon, file)
                self.left_list.addItem(item)

    def select_output_directory(self):
        self.directory = None
        self.right_list.clear()
        # Open a directory selection dialog
        selcted_directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if selcted_directory:
            self.directory = selcted_directory
            folder_icon = QIcon(image1_path)
            folder_name = self.directory.split('/')[-1]
            item = QListWidgetItem(folder_icon, folder_name)
            self.right_list.addItem(item)
        else:
            self.directory = None
            print('bfhilwkesdewased')

    def list_files_in_directory(self, directory):
        """
        List files recursively in the directory.
        """
        path = Path(directory)
        return [str(file) for file in path.rglob('*') if file.is_file()]

    def process_audio(self):
        """
        Process selected audio files.
        """
        # Show loading dialog
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.show()
        print(self.file_path)
        print(self.folder_path)
        print(self.directory)

        if self.file_path == None and self.folder_path == None:
            self.error_dialog = InputEmpty()
            self.error_dialog.show()
            self.loading_dialog.close()

        if self.directory == None:
            self.error_dialog = OutputEmpty()
            self.error_dialog.show()
            self.loading_dialog.close()

        if self.file_path != None and self.directory != None:
            if strip(self.file_path) == True:
                # Load the audio file
                y, sr = librosa.load(path=self.file_path, sr=None)

                S_full, phase = librosa.magphase(librosa.stft(y))

                noise_power = np.mean(S_full[:, :int(sr * 0.1)], axis=1)

                mask = S_full > noise_power[:, None]

                mask = mask.astype(float)

                mask = medfilt(mask, kernel_size=(1, 5))

                S_clean = S_full * mask

                y_clean = librosa.istft(S_clean * phase)

                # Save the cleaned audio file
                x = splt(self.file_path)
                output_audio_file_path = self.directory + '\\' + x +'.wav'

                # Save the enhanced and smoothed audio
                sf.write(output_audio_file_path, y_clean, sr)

                # Simulate a time-consuming task with a timer
                QTimer.singleShot(3000, self.finishProcessing)  # Simulates a 3-second process
            else:
                self.error_dialog = UploadOnlyWAV()
                self.error_dialog.show()
                self.loading_dialog.close()

        if self.folder_path != None and self.directory != None:
            all_files = self.list_files_in_directory(self.folder_path)

            if len(all_files) == 0:
                self.error_dialog = FileEmpty()
                self.error_dialog.show()
                self.loading_dialog.close()

            else:
                for file in all_files:
                    if strip(file) == True:
                        audio_file_path = file

                        # Load the audio file
                        y, sr = librosa.load(path=audio_file_path, sr=None)

                        S_full, phase = librosa.magphase(librosa.stft(y))

                        noise_power = np.mean(S_full[:, :int(sr * 0.1)], axis=1)

                        mask = S_full > noise_power[:, None]

                        mask = mask.astype(float)

                        mask = medfilt(mask, kernel_size=(1, 5))

                        S_clean = S_full * mask

                        y_clean = librosa.istft(S_clean * phase)

                        # Save the cleaned audio file
                        x = splt_1(file)
                        output_audio_file_path = self.directory + '\\' + x +'.wav'

                        # Save the enhanced and smoothed audio
                        sf.write(output_audio_file_path, y_clean, sr)

                        # Simulate a time-consuming task with a timer
                        QTimer.singleShot(3000, self.finishProcessing)  # Simulates a 3-second process
                    else:
                        self.error_dialog = UploadOnlyWAV()
                        self.error_dialog.show()
                        self.loading_dialog.close()

    def finishProcessing(self):
        """
        Finish processing and close the loading dialog.
        """
        self.loading_dialog.update_message("Processing finished.")
        QTimer.singleShot(1000, self.loading_dialog.close)


# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioProcessorGUI()
    ex.showMaximized()
    sys.exit(app.exec_())
