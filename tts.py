# Imports
import pyttsx3
from time import time, sleep
import unicodedata

# Retrieves wpm speed
rate = int(input('WPM : '))
while not(0 < rate <= 50):
    rate = int(input('Please enter a speed between 0 and 50 WPM : '))

# Reads the text of the user in the text.txt file
with open('text.txt', 'r') as f:
    string = f.read()

def preprocess(string, punctuation):
    """Transform the raw txt into a list of word for TTS

    Parameters
    ----------
    string : str
        Raw text file
    punctuation : dict
        Dictionnary with the punctation to pronounce

    Returns
    -------
    list
        List of preprocessed words
    """
    string = string.replace('\n', ' ') # Delete all \n (skip line)

    for key, value in punctuation.items():
        string = string.replace(key, value) # Replace punctuation
    
    string = unicodedata.normalize('NFD', string)\
           .encode('ascii', 'ignore')\
           .decode("utf-8") # Normalize special characters 

    string = string.split(' ') # Split the string into a list

    txt = []
    for word in string:
        if word not in [' ', '']:
            txt.append(word) # Avoid having spaces or blank
    
    return txt

def need(word, rate, len_word=5):
    """Computes the time needed to write word

    Parameters
    ----------
    word : str
        The word
    rate : int
        Word per minute
    len_word : int, optional
        Usually, a word is defined as 5 characters
    
    Returns
    -------
    float
        Time needed (s)
    """
    pause = len(word)/len_word*60/rate
    return pause

# French common punctuation
punctuation = {
    ',' : ' virgule ',
    '?' : " point d'interrogation ",
    '!' : " point d'exclamation ",
    ':' : ' deux points ',
    '.' : ' point ',
    '...' : ' trois petits points ',
    '=' : ' egal '
}

# Reverse punctuation
reverse = {value[1:-1]: key for key, value in punctuation.items()}

# Preprocess the txt file and init TTS
txt = preprocess(string, punctuation)
engine = pyttsx3.init()

# Track wpm speed
length = 0
start = time()
sleep(need(txt[0], rate)) # Avoid division by 0 the first loop

# Loop through each word
for word in txt:
    if sum([word == value[1:-1] for value in punctuation.values()]): # If word is a punctuation
        length += 1
        print(reverse[word])

        # TTS
        engine.say(word)
        engine.runAndWait()
    else: # If it is a word
        length += len(word)
        wpm = (length/5)/((time()-start)/60)
        print(word)
        
        # Compute the needed time and save when TTS started
        pause = need(word, rate)
        t = time()

        # TTS
        engine.say(word)
        engine.runAndWait()

        # Pause
        sleep(max(0, t+pause-time()))

print(f'{(length/5)/((time()-start)/60)}wpm') # Print wpm speed