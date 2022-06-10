import random

from string import punctuation
import PySimpleGUI as sg
import numpy as np

rus_alph = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й',
            'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
spec_sym = punctuation + ' ' + '\n'
code_size = 5

_generated_key = None


def key_generating(text_len):
    key_len = text_len * code_size
    key = [i % 2 for i in range(key_len)]  # same count 0 and 1
    random.shuffle(key)

    key = np.reshape(key, (text_len, code_size))
    # key = [key[i*code_size:(i+1)*code_size] for i in range(text_len)]
    return key


def key_converting(key_str, text_len):
    key_binary_list = []
    key_index = 0
    for _ in range(text_len):
        letter_code = rus_alph.index(key_str[key_index])
        letter_binary_list = [int(x) for x in f'{letter_code:05b}']  # from decimal to binary
        key_binary_list.append(letter_binary_list)

        key_index += 1
        if key_index == len(key_str):
            key_index = 0

    return key_binary_list


def ciphering(text, key_list):
    cipher_text = []
    text_binary_list = []

    i = 0
    for letter in text.lower():
        if letter == ' ':
            cipher_text.append(' ')
            continue
        letter_code = rus_alph.index(letter)
        letter_binary_list = [int(x) for x in f'{letter_code:05b}']  # from decimal to binary
        text_binary_list.append(letter_binary_list)

        cipher_binary_list = [str(int(letter_binary_list[k] != key_list[i][k])) for k in range(code_size)]  # xor
        cipher_binary_str = ''.join(cipher_binary_list)
        cipher_text.append(rus_alph[int(cipher_binary_str, 2)])  # from binary to decimal, get symbol
        i += 1

    return ''.join(cipher_text), text_binary_list


def array_print(arr_arr):
    arr_str = [str(np.array(arr)) for arr in arr_arr]
    # arr_str = [str(arr) for arr in arr_arr]
    return ' - '. join(arr_str)


if __name__ == '__main__':
    sg.theme('DarkBrown')
    font_window = ('Arial 12 bold')
    font_input = ('Arial 12')
    # заполнение разметки окна - лист из листов
    layout = [
        [sg.Text('Input Text on russian language:', font=font_window)],
        [sg.Multiline(size=(70, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4',
                      key='-IText-')],
        [sg.Text('Key', font=font_window), sg.InputText(size=(20, 2), key='-Key-', font=font_input),
         sg.Checkbox('Use generated Key', font=font_window, key='-GKey-'),
         sg.Button('Ciphering', font=font_window)],
        [sg.Text('Binary input Text:', font=font_window)],
        [sg.Text(size=(72, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-BIText-')],
        [sg.Text('Binary Key:', font=font_window)],
        [sg.Text(size=(72, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-BKey-')],
        [sg.Text('Cipher Text:', font=font_window)],
        [sg.Multiline(size=(70, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4',
                      key='-CText-')],
        [sg.Button('Deciphering', font=font_window)],
        [sg.Text('Decipher Text:', font=font_window)],
        [sg.Text(size=(70, 2), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-DText-')],
    ]
    window = sg.Window('XOR Cipher from KVA', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        key_value = values['-Key-'].replace(' ', '').lower()

        if event == 'Ciphering':
            window['-DText-'].update('')
            if values['-GKey-']:
                key_value = ''
            window['-Key-'].update(key_value)

            if values['-IText-'] == '' or (not values['-GKey-'] and key_value == ''):
                sg.PopupOK('Please, write input text and key for ciphering')
                continue
            if not all([(sym in rus_alph) or (sym == ' ') for sym in values['-IText-'].lower()]):
                sg.PopupOK('Please, write input text on russian only, no punctuation and numbers')
                continue
            if not values['-GKey-'] and not all([sym in rus_alph for sym in key_value]):
                sg.PopupOK('Please, write key on russian only, no punctuation and numbers')
                continue

            # get right binary key (gamma) for ciphering
            text_len = len(values['-IText-'].replace(' ', ''))
            if values['-GKey-']:
                key_binary_list = key_generating(text_len)
                _generated_key = key_binary_list
            else:
                key_binary_list = key_converting(key_value, text_len)

            cipher_text, binary_input_text = ciphering(
                values['-IText-'], key_binary_list
            )
            window['-BIText-'].update(array_print(binary_input_text))
            window['-BKey-'].update(array_print(key_binary_list))
            window['-CText-'].update(cipher_text)

        if event == 'Deciphering':
            if values['-GKey-']:
                key_value = ''
            window['-Key-'].update(key_value)

            if values['-CText-'] == '' or (not values['-GKey-'] and key_value == ''):
                sg.PopupOK('Please, write cipher text and key for deciphering')
                continue
            if not all([(sym in rus_alph) or (sym == ' ') for sym in values['-CText-'].lower()]):
                sg.PopupOK('Please, write cipher text on russian only, no punctuation and numbers')
                continue
            if not values['-GKey-'] and not all([sym in rus_alph for sym in key_value]):
                sg.PopupOK('Please, write key on russian only, no punctuation and numbers')
                continue

            # get right binary key (gamma) for ciphering
            text_len = len(values['-CText-'].replace(' ', ''))
            if values['-GKey-']:
                key_binary_list = _generated_key  # take key, generated for ciphering
            else:
                key_binary_list = key_converting(key_value, text_len)

            decipher_text, binary_cipher_text = ciphering(
                values['-CText-'], key_binary_list
            )
            window['-DText-'].update(decipher_text)
