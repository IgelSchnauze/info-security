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
    k = int(k)
    n = len(alph)
    cipher_text = []

    for letter in text.lower():
        new_letter = alph[(alph.index(letter) + (k % n)) % n] if letter not in spec_sym else letter
        cipher_text.append(new_letter)

    return ''.join(cipher_text)


def deciphering(text, k, alph):
    k = int(k)
    n = len(alph)
    decipher_text = []

    for letter in text:
        new_letter = alph[(alph.index(letter) - (k % n)) % n] if letter not in spec_sym else letter
        decipher_text.append(new_letter)

    return ''.join(decipher_text)


if __name__ == '__main__':
    sg.theme('DarkBrown')
    # заполнение разметки окна - лист из листов
    layout = [
        [sg.Text('Input Text on language:'),
         sg.Radio('русский', "Lang"), sg.Radio('english', "Lang", default=True, key='-Eng-')],
        [sg.Multiline(size=(70, 3), background_color='lightgray', text_color='SteelBlue4', key='-IText-')],
        [sg.Text('Key'), sg.InputText(size=(20, 2), key='-Key-'), sg.Button('Ciphering')],
        [sg.Text('Cipher Text')],
        [sg.Multiline(size=(70, 3), background_color='lightgray', text_color='SteelBlue4', key='-CText-')],
        [sg.Button('Deciphering')],
        [sg.Text('Decipher Text'), sg.Text()],
        [sg.Text(size=(63, 3), background_color='lightgray', text_color='SteelBlue4', key='-DText-')],
    ]
    window = sg.Window('Caesar Cipher from KVA', layout)

    while True:
        event, values = window.read()
        # print(values)
        if event in (None, 'Exit'):
            break

        key_value = values['-Key-'].replace(' ', '')

        if event == 'Ciphering':
            window['-Key-'].update(key_value)

            if values['-IText-'] == '' or key_value == '':
                sg.PopupOK('Please, write input text and key for ciphering')
                continue
            if (values['-Eng-'] and
                not all([(sym in eng_alph) or (sym in spec_sym) for sym in values['-IText-'].lower()]) ) \
                or (not values['-Eng-'] and
                not all([(sym in rus_alph) or (sym in spec_sym) for sym in values['-IText-'].lower()]) ):
                sg.PopupOK('Please, choose right language and write text on this language only')
                continue
            if not all([num in numbers for num in key_value]):
                if key_value[0] == '-' and all([num in numbers for num in key_value[1:]]): # negative it's ok
                    pass
                else:
                    sg.PopupOK('Key can be only integer, no punctuation and letters')
                    continue

            cipher_text = ciphering(
                values['-IText-'], key_value, eng_alph if values['-Eng-'] else rus_alph
            )
            # set in element with key 'CTEXT' new value
            window['-CText-'].update(cipher_text)
            _cipher_text = cipher_text


        if event == 'Deciphering':
            window['-Key-'].update(key_value)

            if values['-CText-'] == '' or key_value == '':
                sg.PopupOK('Please, write key and cipher some text')
                continue
            if (values['-Eng-'] and
                not all([(sym in eng_alph) or (sym in spec_sym) for sym in values['-CText-'].lower()]) ) \
                    or (not values['-Eng-'] and
                        not all([(sym in rus_alph) or (sym in spec_sym) for sym in values['-CText-'].lower()]) ):
                sg.PopupOK('Please, choose right language and write text on this language only')
                continue
            if not all([num in numbers for num in key_value]):
                if key_value[0] == '-' and all([num in numbers for num in key_value[1:]]): # negative it's ok
                    pass
                else:
                    sg.PopupOK('Key can be only integer, no punctuation and letters')
                    continue

            decipher_text = deciphering(
                values['-CText-'], key_value, eng_alph if values['-Eng-'] else rus_alph
            )
            window['-DText-'].update(decipher_text)
