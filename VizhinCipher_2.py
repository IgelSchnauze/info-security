import PySimpleGUI as sg
from string import punctuation

rus_alph = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
            'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
eng_alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
            'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
spec_sym = punctuation + ' ' + '\n'


def ciphering(text, k, alph):
    n = len(alph)
    cipher_text = []

    key_index = 0
    for letter in text.lower():
        new_letter = alph[(alph.index(letter) + alph.index(k[key_index])) % n] if letter != ' ' else letter
        cipher_text.append(new_letter)

        if letter != ' ':
            key_index +=1
        if key_index == len(k):
            key_index = 0

    return ''.join(cipher_text)


def deciphering(text, k, alph):
    text = text.lower()
    n = len(alph)
    decipher_text = []

    key_index = 0
    for letter in text.lower():
        new_letter = alph[(alph.index(letter) - alph.index(k[key_index])) % n] if letter != ' ' else letter
        decipher_text.append(new_letter)

        if letter != ' ':
            key_index +=1
        if key_index == len(k):
            key_index = 0

    return ''.join(decipher_text)


if __name__ == '__main__':
    sg.theme('DarkBrown')
    font_window = ('Arial 12 bold')
    font_input = ('Arial 12')
    # заполнение разметки окна - лист из листов
    layout = [
        [sg.Text('Input Text on language:', font=font_window),
         sg.Radio('русский', "Lang", font=font_window),
         sg.Radio('english', "Lang", default=True, key='-Eng-', font=font_window)],
        [sg.Multiline(size=(70, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-IText-')],
        [sg.Text('Key', font=font_window), sg.InputText(size=(20, 2), key='-Key-', font=font_input),
         sg.Button('Ciphering', font=font_window)],
        [sg.Text('Cipher Text', font=font_window)],
        [sg.Multiline(size=(70, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-CText-')],
        [sg.Button('Deciphering', font=font_window)],
        [sg.Text('Decipher Text', font=font_window)],
        [sg.Text(size=(63, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-DText-')],
    ]
    window = sg.Window('Vizhin Cipher from KVA', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        key_value = values['-Key-'].replace(' ', '').lower()

        if event == 'Ciphering':
            window['-Key-'].update(key_value)

            if values['-IText-'] == '' or key_value == '':
                sg.PopupOK('Please, write input text and key for ciphering')
                continue
            if (values['-Eng-'] and
                not all([(sym in eng_alph) or (sym == ' ') for sym in values['-IText-'].lower()])) \
                    or (not values['-Eng-'] and
                        not all([(sym in rus_alph) or (sym == ' ') for sym in values['-IText-'].lower()])):
                sg.PopupOK('Please, choose right language and write input text on this language only, no punctuation')
                continue
            if (values['-Eng-'] and not all([sym in eng_alph for sym in key_value])) \
                    or (not values['-Eng-'] and not all([sym in rus_alph for sym in key_value])):
                sg.PopupOK('Please, choose right language and write key on this language only, no punctuation')
                continue

            cipher_text = ciphering(
                values['-IText-'], key_value, eng_alph if values['-Eng-'] else rus_alph
            )
            window['-CText-'].update(cipher_text)
            _cipher_text = cipher_text

        if event == 'Deciphering':
            window['-Key-'].update(key_value)

            if values['-CText-'] == '' or key_value == '':
                sg.PopupOK('Please, write input text and key for ciphering')
                continue
            if (values['-Eng-'] and
                not all([(sym in eng_alph) or (sym == ' ') for sym in values['-CText-'].lower()])) \
                    or (not values['-Eng-'] and
                        not all([(sym in rus_alph) or (sym == ' ') for sym in values['-CText-'].lower()])):
                sg.PopupOK('Please, choose right language and write input text on this language only, no punctuation')
                continue
            if (values['-Eng-'] and not all([sym in eng_alph for sym in key_value])) \
                    or (not values['-Eng-'] and not all([sym in rus_alph for sym in key_value])):
                sg.PopupOK('Please, choose right language and write key on this language only, no punctuation')
                continue

            decipher_text = deciphering(
                values['-CText-'], key_value, eng_alph if values['-Eng-'] else rus_alph
            )
            window['-DText-'].update(decipher_text)
