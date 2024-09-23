import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from easygui import buttonbox
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string
from googletrans import Translator,LANGUAGES
# Constants
ISL_GIF = [
    'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
    'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
    'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
    'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
    'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing', 
    'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
    'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
    'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
    'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
    'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
    'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
    'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
    'where is the bathroom', 'where is the police station', 'you are wrong','address','agra','ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
    'bihar','bihar','bridge','cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile','dasara',
    'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
    'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
    'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
    'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
    'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
    'voice', 'wednesday', 'weight','please wait for sometime','what is your mobile number','what are you doing','are you busy'
]

ALPHABETS = list(string.ascii_lowercase)

class ImageLabel(tk.Label):
    """A label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

def display_gif(phrase):
    root = tk.Tk()
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(f'ISL_Gifs/{phrase}.gif')
    root.mainloop()

def display_alphabet_images(text):
    for char in text:
        if char in ALPHABETS:
            image_address = f'letters/{char}.jpg'
            image_itself = Image.open(image_address)
            image_numpy_format = np.asarray(image_itself)
            plt.imshow(image_numpy_format)
            plt.draw()
            plt.pause(0.8)
    plt.close()

# Initialize the translator
translator = Translator()
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print(f"Speak Something.")
            audio = recognizer.listen(source)
            try:
                true_text = recognizer.recognize_google(audio)
                detected = translator.detect(true_text)
                text = translator.translate(text=true_text, dest='en').text
                text=text.lower()
                print(f'You Said: {true_text}')
                detected_lang_name = LANGUAGES.get(detected.lang, 'Unknown Language')
                print(f"You Spoke in: {detected_lang_name}")
                print(f'Translated Text: {text}')
                for c in string.punctuation:
                    text = text.replace(c, "")
                if text in ["goodbye", "good bye", "bye"]:
                    print("Oops! Time to say goodbye")
                    break
                elif text in ISL_GIF:
                    display_gif(text)
                else:
                    display_alphabet_images(text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

def main():
    while True:
        image = "signlang.png"
        msg = "HEARING IMPAIRMENT ASSISTANT"
        choices = ["Live Voice", "All Done!"]
        reply = buttonbox(msg, image=image, choices=choices)
        if reply == choices[0]:
            recognize_speech()
        elif reply == choices[1]:
            break

if __name__ == "__main__":
    main()