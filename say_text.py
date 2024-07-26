import js
import random

html_accessed = True
try:
    from pyscript import document
    from pyscript import window
except:
    import multiprocessing
    html_accessed = False

def say_text(text: str):
    import pyttsx3
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
    bible = open('World_English_Version.txt', encoding='utf8')

    bible_dictionary = {}
    for line in bible.readlines():
        line = line.replace('\n', '').replace('\t', ' ')

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
    named_list = []

    if len(elipse) == 1 and valid_verse(bible, elipse[0]):
        book, chap, verse = elipse[0]
        verse_list.append(bible[book][chap][verse])
        named_list = [f'{book} {chap}:{verse}: ']
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
        named_list = []

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
                        named_list.append(f'{book} {chap}:{verse}: ')

    return (verse_list, named_list)

def get_text(bible, prompt: str):
    elipse = parse_prompt(prompt)#'Genesis 1:1-Revelation 22:21')
    verse_list, named_list = get_all_verses(bible, elipse)

    text = ''
    speach_text = ''
    for i in range(len(verse_list)):
        text += named_list[i] + verse_list[i]
        speach_text += verse_list[i]
        
        if i < len(verse_list) - 1:
            text += '\n'
            speach_text += '\n'

    return (text, speach_text)

def output_text(text: str, speach_text: str, output_location: str, event):
    want_tts = False
    if html_accessed:
        dropdown = document.querySelector('#' + output_location + '-audio')

        output_div = document.querySelector('#' + output_location + '-output')
        output_div.innerText = dropdown


        selected_option = dropdown.options[dropdown.selectedIndex]
        want_tts = selected_option.value == 'yes'

        output_div = document.querySelector('#' + output_location + '-output')
        output_div.innerText = selected_option.value#text
    else:
        print(text)
    
    if want_tts and event != None and len(text) < 350000:
        #https://github.com/kripken/speak.js/tree/master
        js.speak(speach_text)
    elif event == None and want_tts:
        sayable_outputs = []
        for character_index in range(0, len(speach_text), 350000):
            max_val = min(character_index + 350000, len(speach_text))
            
            sayable_outputs.append(speach_text[character_index:max_val])

        for sayable_output in sayable_outputs:
            say_text(sayable_output)

def start_output(function, event):
    if not html_accessed:
        global processes
        if not 'processes' in globals():
            processes = []
        
        while len(processes) > 0:
            process = processes.pop()
            process.terminate()
        
        process = multiprocessing.Process(target=function, args=(event,))
        process.start()
        processes.append(process)
    else:
        function(event) 

def start_generating_output(event=None):
    start_output(gen_output, event)

def gen_output(event):
    if event == None or event != None and (not hasattr(event, 'key') or event.key == 'Enter' ):
        try:
            bible = convert_to_dictionary()
            
            prompt = 'Genesis 1:1'#'Ephesians 5:8-21'
            if html_accessed:
                input_text = document.querySelector("#english")
                prompt = input_text.value

            text, speach_text = get_text(bible, prompt)
            text = prompt + '\n' + text
            speach_text = prompt.replace(':', ' ').replace('-', ' to ') + '\n' + speach_text
        except:
            text = '[Error]: Prompt was not accepted.'
            speach_text = ''

        output_text(text, speach_text, 'find-verse', event)

def get_next_chapter(bible, books: list, random_book_start: str, random_chapter_start: str):
    book_end = random_book_start
    chapter_end = str(int(random_chapter_start) + 1)
    if not chapter_end in bible[random_book_start]:
        if not random_book_start == 'Revelation':
            book_end = books[books.index(random_book_start)+1]
            chapter_end = "1"
        else:
            chapter_end = random_chapter_start

    return (book_end, chapter_end)

def start_generating_random_reading(event=None):
    start_output(gen_random_reading, event)

def gen_random_reading(event):
    try:
        bible = convert_to_dictionary()
        books = list(bible.keys())

        random_book_start = random.choice(books)
        random_chapter_start = random.choice(list(bible[random_book_start].keys()))
        
        book_end, chapter_end = (random_book_start, random_chapter_start)
        verse_end = list(bible[book_end][chapter_end].keys())[-1]
        verse_text = f'{random_book_start} {random_chapter_start}:1-{book_end} {chapter_end}:{verse_end}'

        prev_length = 0
        length = len(get_text(bible, verse_text)[0])
        while len(get_text(bible, verse_text)[0]) < 5000 and length > prev_length:
            book_end, chapter_end = get_next_chapter(bible, books, book_end, chapter_end)
            verse_end = list(bible[book_end][chapter_end].keys())[-1]
            verse_text = f'{random_book_start} {random_chapter_start}:1-{book_end} {chapter_end}:{verse_end}'

            prev_length = length
            length = len(get_text(bible, verse_text)[0])

        text, speach_text = get_text(bible, verse_text)
        text, speach_text = get_text(bible, verse_text)
        text = verse_text + '\n' + text
        speach_text = verse_text.replace(':', ' ').replace('-', ' to ') + '\n' + speach_text
    except:
        text = '[Error]: Prompt was not accepted.'
        speach_text = ''
    
    output_text(text, speach_text, 'devotion', event)

if __name__ == '__main__' and not html_accessed:
    start_generating_random_reading()
    print('I launched a thread.')
    start_generating_random_reading()
    start_generating_output()