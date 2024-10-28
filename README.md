# **Quietify - Audio Noise Reduction GUI**

Quietify is a PyQt5-based desktop application for reducing noise in audio files. It supports both individual audio files and batch processing of folders. The tool leverages **Librosa**, **PyDub**, and **NoiseReduce** to enhance the audio quality by minimizing background noise.

---

## **Features**
- Process individual `.wav` files or entire folders.
- Batch noise reduction to prevent memory overload.
- User-friendly GUI built with PyQt5.
- Customized styling for an intuitive user experience.
- Displays alerts for non-WAV files, empty selections, or missing inputs.
- Progress dialog to track audio processing in real-time.

---

## **Installation**

To run the application, ensure that the following dependencies are installed.  
This app works best on **Python 3.8+**. Install libraries through `apt` or `pip` if needed:

```bash
# Install required dependencies
sudo apt-get install python3-pyqt5 python3-scipy
pip3 install librosa pydub noisereduce soundfile matplotlib numpy
```

---

## **How to Run**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Ensure all dependencies are installed (as mentioned above).

3. Launch the application:
   ```bash
   python3 main.py
   ```

---

## **Usage Guide**

1. **Select Input File/Folder**:
   - Use the dropdown to choose between file or folder selection.
   - Select a `.wav` file or a folder containing audio files.

2. **Select Output Directory**:
   - Choose the destination directory for the processed files.

3. **Process Audio**:
   - Click the **Process Audio** button to start the noise reduction process.

4. **View Progress**:
   - A loading dialog will appear during processing.
   - Once finished, the cleaned audio files will be saved in the selected output directory.

---

## **Directory Structure**

```
📦Your_Project
 ┣ 📂images
 ┃ ┣ 📄folder.png
 ┃ ┗ 📄music-icon.png
 ┣ 📄main.py
 ┣ 📄README.md
```

---

## **Known Issues and Limitations**
- Only `.wav` files are supported.
- Large audio files may take longer to process.
- Ensure the output directory is not empty; otherwise, the process will stop.

---

## **Contributing**

Feel free to submit pull requests for new features or bug fixes. Fork the repository, make changes, and submit a pull request.

---

## **License**

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**
- [Librosa](https://librosa.org) for audio manipulation.
- [PyDub](https://github.com/jiaaro/pydub) for audio processing.
- [NoiseReduce](https://github.com/timsainb/noisereduce) for noise reduction.
- Icons from [Flaticon](https://www.flaticon.com/).

---

## **Contact**
For any questions or support, please reach out through the Issues tab.

---

This README provides all essential information for users and contributors to understand and run your application. You can customize it further by adding screenshots, a demo video, or detailed error troubleshooting steps.
