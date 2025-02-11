# Flash Card Speech Recognition App

This is a Python-based flash card application that uses speech recognition to assess answers. The app displays a question from a JSON file, listens to the user's spoken response, and determines if the answer is correct or incorrect.

## Features
- Displays questions from a JSON file.
- Uses speech recognition to capture and evaluate user responses.
- Marks answers as correct or incorrect based on speech input.
- Tracks correct and incorrect answers.
- Saves results to text files and an Excel file.
- Provides a graphical user interface (GUI) using Tkinter.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flashcard-speech-app.git
   cd flashcard-speech-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Prepare your questions in a JSON file, formatted like this:
   ```json
   [
       {"question": "What is the capital of France?", "answer": "Paris"},
       {"question": "What is 2 + 2?", "answer": "4"}
   ]
   ```
2. Run the application:
   ```bash
   python flashcard_app.py
   ```
3. Speak your answer when prompted.
4. The app will indicate whether your response is correct or incorrect.
5. Results are saved in `correct_answers.txt`, `incorrect_answers.txt`, and `quiz_results.xlsx`.

## Dependencies

The following Python libraries are required:
- `speechrecognition`
- `pyaudio`
- `pyttsx3`
- `tkinter`
- `pandas`
- `openpyxl`


See `requirements.txt` for installation details.

## The purpose

I created this app for a psychology course, however, the questions would not cycle fast enough for me to use it for my purposes. I needed to get through 32 questions in 1 min. I spent a couple hours to get it this far so I decided to move on to something else. This was good enough.


## Contributing
Feel free to submit issues or pull requests to improve this project!

## License
This project is licensed under the GNU General public License.

