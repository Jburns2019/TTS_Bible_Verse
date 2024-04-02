import pyttsx3

test_text = """
For ye were once darkness, but are now light in the Lord: walk as children of light
(for the fruit of the light is in all goodness and righteousness and truth),
proving what is well-pleasing unto the Lord;
and have no fellowship with the unfruitful works of darkness, but rather even reprove them;
for the things which are done by them in secret it is a shame even to speak of.
But all things when they are reproved are made manifest by the light: for everything that is made manifest is light.
Wherefore [he] saith, Awake, thou that sleepest, and arise from the dead, and Christ shall shine upon thee.
Look therefore carefully how ye walk, not as unwise, but as wise;
redeeming the time, because the days are evil.
Wherefore be ye not foolish, but understand what the will of the Lord is.
And be not drunken with wine, wherein is riot, but be filled with the Spirit;
speaking one to another in psalms and hymns and spiritual songs, singing and making melody with your heart to the Lord;
giving thanks always for all things in the name of our Lord Jesus Christ to God, even the Father;
subjecting yourselves one to another in the fear of Christ.
"""

def say_text(text: str):
    engine = pyttsx3.init()

    print(engine.getProperty('rate'))   #printing current voice rate
    engine.setProperty('rate', 150)     # setting up new voice rate

    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

    engine.save_to_file(text, 'recording.mp3')
    engine.runAndWait()

say_text(test_text)