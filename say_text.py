import pyttsx3
import js
import time

html_accessed = True
try:
    from pyscript import document
except:
    html_accessed = False

def say_text(text: str):
    engine = pyttsx3.init()

    engine.setProperty('rate', 200)     # setting up new voice rate

    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female

    engine.say(text)
    engine.runAndWait()

def parse_verse(line: str, want_text=True):
    chap_verse_start = len(line.split(':')[0].split(' ')) - 1

    line_composition = line.split(' ')
    book = ' '.join(line_composition[0:chap_verse_start])
    chap, verse = line_composition[chap_verse_start].split(':')

    text = ''
    if want_text:
        text = ' '.join(line_composition[chap_verse_start+1:])

    return (book, chap, verse, text)

def convert_to_dictionary():
    bible = open('asv.txt', 'r')
    bible_dictionary = {}
    for line in bible.readlines():
        line = line.replace('\n', '')

        if line.count(' ') > 2 and ':' in line:
            book, chap, verse, text = parse_verse(line, want_text=True)
            if not book in bible_dictionary:
                bible_dictionary[book] = {chap: {verse: text}}
            elif not chap in bible_dictionary[book]:
                bible_dictionary[book][chap] = {verse: text}
            else:
                bible_dictionary[book][chap][verse] = text
    
    bible.close()

    return bible_dictionary

def parse_prompt(prompt: str):
    split = prompt.split('-')

    results = []
    for verse_prompt in split:
        if ':' in verse_prompt and verse_prompt.count(' ') > 0:
            book, chap, verse, text = parse_verse(verse_prompt, want_text=False)
        elif ':' in verse_prompt:
            book = results[0][0]

            chap, verse = verse_prompt.split(':')
        elif len(results) > 0:
            book = results[0][0]
            chap = results[0][1]
            verse = verse_prompt

        results.append([book, chap, verse])
    
    return results

def valid_verse(bible: dict, verse_breakdown: list):
    book, chap, verse = verse_breakdown
    return book in bible and chap in bible[book] and verse in bible[book][chap]

def get_all_verses(bible: dict, elipse: list):
    verse_list = []

    if len(elipse) == 1 and valid_verse(bible, elipse[0]):
        book, chap, verse = elipse[0]
        verse_list.append(bible[book][chap][verse])
    if len(elipse) > 1 and valid_verse(bible, elipse[0]) and valid_verse(bible, elipse[1]):
        book_beg, chap_beg, verse_beg = elipse[0]
        book_end, chap_end, verse_end = elipse[1]

        books = list(bible.keys())
        book_beg_index = books.index(book_beg)
        book_end_index = books.index(book_end)
        verse_list = [bible[book_beg][chap_beg][verse_beg]]
        if book_beg == book_end and chap_beg == chap_end and int(verse_beg) >= int(verse_end):
            print(f'[Error]: Verse {verse_end} is the same or comes before verse {verse_beg} in the book of {book_beg} chapter {chap_beg}.')
            return verse_list
        elif book_beg == book_end and int(chap_beg) > int(chap_end):
            print(f'[Error]: The chapter of {chap_end} comes before chapter {chap_beg} in the book of {book_beg}.')
            return verse_list
        elif not book_end in books[book_beg_index:]:
            choices = ', '.join(books[book_beg_index:])
            print(f'[Error]: The book of {book_end} comes before the book of {book_beg}. Choose from {choices}.')
            return verse_list
        verse_list = []

        book_range = books[book_beg_index:book_end_index+1]
        for book in book_range:
            chap_beg_book, chap_end_book = (1, int(list(bible[book].keys())[-1]))
            if book == book_beg:
                chap_beg_book = int(chap_beg)
            if book == book_end:
                chap_end_book = int(chap_end)

            for chap in range(chap_beg_book, chap_end_book+1):
                verse_beg_book, verse_end_book = (1, int(list(bible[book][str(chap)].keys())[-1]))
                if chap == chap_beg_book:
                    verse_beg_book = int(verse_beg)
                if book == book_end and chap == int(chap_end):
                    verse_end_book = int(verse_end)

                for verse in range(verse_beg_book, verse_end_book+1):
                    if str(verse) in bible[book][str(chap)]:
                        verse_list.append(bible[book][str(chap)][str(verse)])

    return verse_list

def gen_output(event=None):
    if event == None or event != None and event.key == 'Enter':
        bible = convert_to_dictionary()

        prompt = 'Ephesians 5:8-21'
        if html_accessed:
            input_text = document.querySelector("#english")
            prompt = input_text.value
        
        try:
            elipse = parse_prompt(prompt)#'Genesis 1:1-Revelation 22:21')
            verse_list = get_all_verses(bible, elipse)
            text = '\n'.join(verse_list)
        except:
            text = '[Error]: Prompt was not accepted.'

        if html_accessed:
            output_div = document.querySelector("#output")
            output_div.innerText = text
        else:
            print(text)
        
        if event != None and len(text) < 350000:
            #https://github.com/kripken/speak.js/tree/master
            js.speak(text)
        elif event == None:
            sayable_outputs = []
            for character_index in range(0, len(text), 350000):
                max_val = min(character_index + 350000, len(text))
                
                sayable_outputs.append(text[character_index:max_val])

            for sayable_output in sayable_outputs:
                say_text(sayable_output)

if __name__ == '__main__' and not html_accessed:
    gen_output()