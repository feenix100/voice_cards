import json
import random
import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pandas as pd
import os
from datetime import datetime

# Load Flashcards
with open("flashcards.json", "r") as f:
    flashcards = json.load(f)

# Initialize Speech Recognition and Text-to-Speech
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Global variables
current_index = 0
correct_count = 0
incorrect_count = 0
quiz_running = False  # Tracks if quiz has started
countdown_time = 1  # Listening delay (1 sec)

correct_entries = []
incorrect_entries = []

# File paths
correct_file = "correct_answers.txt"
incorrect_file = "incorrect_answers.txt"
excel_file = "quiz_results.xlsx"

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def normalize_text(text):
    """Normalize text for better matching (lowercase, strip spaces)."""
    return text.strip().lower()

def start_quiz():
    """Start the quiz and begin listening for answers."""
    global quiz_running, current_index, correct_entries, incorrect_entries
    quiz_running = True
    current_index = 0
    correct_entries = []
    incorrect_entries = []
    show_question()
    root.after(1000, check_answer)  # Start listening after 1 sec

def show_question():
    """Display the next question."""
    if current_index < len(flashcards):
        question_label.config(text=flashcards[current_index]["question"])
        answer_label.config(text="")  # Hide answer initially
        status_label.config(text="")  # Clear previous status
        speech_output_label.config(text="🗣 Your Answer: ")
        listening_label.config(text="🎤 Listening in 1 second...")
    else:
        question_label.config(text="All done!")
        answer_label.config(text="")
        status_label.config(text="Game over! Click Restart or Exit.")
        speech_output_label.config(text="")
        listening_label.config(text="")

        # Save results to files
        save_results()

def check_answer():
    """Use speech recognition to check user's spoken answer against the correct answer."""
    global current_index, correct_count, incorrect_count

    if current_index >= len(flashcards) or not quiz_running:
        return

    try:
        with sr.Microphone() as source:
            listening_label.config(text="🎤 Listening now...")
            root.update_idletasks()

            recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Quick noise adjustment
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)  # Fast response time

            # Convert speech to text
            spoken_text = recognizer.recognize_google(audio)
            user_answer = normalize_text(spoken_text)
            correct_answer = normalize_text(flashcards[current_index]["answer"])

            # Display recognized speech in separate label
            speech_output_label.config(text=f"🗣 Your Answer: {spoken_text}")

            # Capture current question and answer
            question_text = flashcards[current_index]["question"]
            correct_answer_text = flashcards[current_index]["answer"]

            # Check answer strictly
            if user_answer == correct_answer:
                correct_count += 1
                correct_label.config(text=f"✅ Correct: {correct_count}")
                status_label.config(text="✅ Correct!")
                correct_entries.append(f"Q: {question_text}\nA: {correct_answer_text}\n")
            else:
                incorrect_count += 1
                incorrect_label.config(text=f"❌ Incorrect: {incorrect_count}")
                status_label.config(text=f"❌ Incorrect! Correct: {correct_answer_text}")
                incorrect_entries.append(f"Q: {question_text}\nA: {correct_answer_text}\n")

    except sr.UnknownValueError:
        # If speech is not recognized, mark as incorrect
        question_text = flashcards[current_index]["question"]
        correct_answer_text = flashcards[current_index]["answer"]

        incorrect_count += 1
        incorrect_label.config(text=f"❌ Incorrect: {incorrect_count}")
        status_label.config(text="⚠️ Speech not recognized. Marked as incorrect.")
        speech_output_label.config(text="⚠️ Couldn't recognize speech.")
        incorrect_entries.append(f"Q: {question_text}\nA: {correct_answer_text}\n")

    except sr.RequestError:
        status_label.config(text="⚠️ Speech Recognition service unavailable.")
    except Exception as e:
        status_label.config(text=f"⚠️ Error: {str(e)}")

    # Move to next question automatically
    current_index += 1
    root.after(1000, show_question)  # Show next question after 1 second
    root.after(1100, check_answer)  # Start listening after 1 sec

def save_results():
    """Save correct and incorrect questions with answers to text files and log results in Excel."""
    date_today = datetime.today().strftime("%Y-%m-%d %H:%M")  # Format: YYYY-MM-DD HH:MM

    # Save correct answers to file
    with open(correct_file, "a") as f:
        f.write(f"\nDate: {date_today}\n")
        for entry in correct_entries:
            f.write(f"{entry}\n")

    # Save incorrect answers to file
    with open(incorrect_file, "a") as f:
        f.write(f"\nDate: {date_today}\n")
        for entry in incorrect_entries:
            f.write(f"{entry}\n")

    # Save results to Excel
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
    else:
        df = pd.DataFrame(columns=["Date", "Incorrect Count", "Correct Count"])

    new_entry = pd.DataFrame([[date_today, incorrect_count, correct_count]], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)

    # Save back to Excel
    df.to_excel(excel_file, index=False)

def shuffle_flashcards():
    """Restart game by reshuffling flashcards and resetting progress."""
    global flashcards, current_index, correct_count, incorrect_count, quiz_running
    random.shuffle(flashcards)
    current_index = 0
    correct_count = 0
    incorrect_count = 0
    quiz_running = False  # Reset game state
    correct_label.config(text="✅ Correct: 0")
    incorrect_label.config(text="❌ Incorrect: 0")
    question_label.config(text="Press 'Start Quiz' to begin")
    status_label.config(text="Game Restarted!")
    speech_output_label.config(text="🗣 Your Answer: ")
    listening_label.config(text="")

def exit_app():
    """Exit the application."""
    root.quit()

# GUI Setup
root = tk.Tk()
root.title("Flashcard App with Voice Recognition")
root.geometry("800x600")  # Set bigger window size

question_label = tk.Label(root, text="Press 'Start Quiz' to begin", font=("Arial", 20), pady=20, wraplength=700)
question_label.pack()

answer_label = tk.Label(root, text="", font=("Arial", 20), fg="blue")
answer_label.pack()

speech_output_label = tk.Label(root, text="🗣 Your Answer: ", font=("Arial", 16), fg="black")
speech_output_label.pack(pady=10)

listening_label = tk.Label(root, text="🎤 Listening in...", font=("Arial", 16), fg="blue")
listening_label.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

start_button = tk.Button(btn_frame, text="Start Quiz", command=start_quiz, fg="blue", font=("Arial", 14), width=15)
start_button.grid(row=0, column=0, padx=10)

restart_button = tk.Button(btn_frame, text="Restart", command=shuffle_flashcards, fg="red", font=("Arial", 14), width=15)
restart_button.grid(row=0, column=1, padx=10)

exit_button = tk.Button(root, text="Exit", command=exit_app, fg="black", font=("Arial", 14), width=15)
exit_button.pack(pady=10)

# Score Labels
correct_label = tk.Label(root, text="✅ Correct: 0", font=("Arial", 16), fg="green")
correct_label.pack()

incorrect_label = tk.Label(root, text="❌ Incorrect: 0", font=("Arial", 16), fg="red")
incorrect_label.pack()

status_label = tk.Label(root, text="", font=("Arial", 16), pady=10)
status_label.pack()

# Start the game
shuffle_flashcards()

# Run the app
root.mainloop()
