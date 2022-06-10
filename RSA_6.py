import random

import PySimpleGUI as sg

from string import punctuation
from PrimeNumber_5 import gener_prime_MR, nod, raising
from Euclid_4 import ee_algorithm

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
spec_sym = punctuation + ' ' + '\n'


def key_generation(min_len):
    p = gener_prime_MR(min_len)
    q = gener_prime_MR(min_len)
    n = p * q
    a_n = (p-1) * (q-1)

    len_bin_e = len(f'{n:b}') // 3
    min_dec_e = int(f'{pow(10, len_bin_e-1)}', 2)
    max_dec_e = int(''.join(['1' for i in range(len_bin_e)]), 2)

    # len_e = len(str(n)) // 3
    # e = random.randint(pow(10, len_e-1), pow(10, len_e))  # take just decimal len n
    while True:
        e = random.randint(min_dec_e, max_dec_e)
        if nod(a_n, e) == 1:
            break

    _, d, _ = ee_algorithm(a_n, e)
    if d < 0:
        d = d + a_n  # %

    return p, q, n, a_n, e, d


def rsa_ciphering(text, e, n):
    ciphercode = []
    for sym in text:
        sym_code = ord(sym)
        code_cipher = raising(e, sym_code, n)
        ciphercode.append(str(code_cipher))
    return '\n'.join(ciphercode)


def rsa_deciphering(ciphercode, d, n):
    text = []
    for h in ciphercode:
        sym_code = raising(d, h, n)
        text.append(chr(int(sym_code % 55295)))
        # if sym_code > 55295:
        #     text.append(chr(int(sym_code % 55295)))
        #     # text.append('<error>')
        # else:
        #     text.append(chr(int(sym_code)))
    return ''.join(text)


param_n = None
param_d = None
if __name__ == '__main__':
    sg.theme('DarkBrown')
    font_window = ('Arial 12 bold')
    font_input = ('Arial 12')
    # заполнение разметки окна - лист из листов
    layout = [
        [sg.Text('Input Text (any language with number and punctuation):', font=font_window)],
        [sg.Multiline(size=(70, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4',
                      key='-IText-')],
        [sg.Text('Some min number of bits for p,q:', font=font_window),
         sg.InputText(size=(10, 2), key='-Nbit-', font=font_input),
         sg.Button('Ciphering', font=font_window)],
        [sg.Text('Cipher Text:', font=font_window)],
        [sg.Multiline(size=(120, 7), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-CText-')],
        [sg.Button('Deciphering', font=font_window)],
        [sg.Text('Decipher Text:', font=font_window)],
        [sg.Text(size=(70, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-DText-')],
        [sg.Text('\n')],
        [sg.Text('p - ', font=font_window), sg.Text(font=font_input, key='-p-')],
        [sg.Text('q - ', font=font_window), sg.Text(font=font_input, key='-q-')],
        [sg.Text('n - ', font=font_window), sg.Text(font=font_input, key='-n-')],
        [sg.Text('a - ', font=font_window), sg.Text(font=font_input, key='-an-')],
        [sg.Text('e - ', font=font_window), sg.Text(font=font_input, key='-e-')],
        [sg.Text('d - ', font=font_window), sg.Text(font=font_input, key='-d-')]
    ]
    window = sg.Window('RSA from KVA', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        num_bits = values['-Nbit-'].replace(' ', '').lower()

        if event == 'Ciphering':
            window['-DText-'].update('')
            window['-Nbit-'].update(num_bits)

            if values['-IText-'] == '' or num_bits == '':
                sg.PopupOK('Please, write input text and number or bits')
                continue
            if not all([num in numbers for num in num_bits]):
                sg.PopupOK('Number of bits is only nUmBEr!')
                continue

            _ = f'{pow(10, int(num_bits))}'  # some binary this length
            num_min_len = len(f'{int(_, 2)}')  # length decimal

            p, q, n, a_n, e, d = key_generation(num_min_len)
            window['-p-'].update(p)
            window['-q-'].update(q)
            window['-n-'].update(n)
            window['-an-'].update(a_n)
            window['-e-'].update(e)
            window['-d-'].update(d)
            param_n = n
            param_d = d

            cipher_text = rsa_ciphering(values['-IText-'], e, n)
            window['-CText-'].update(cipher_text)

        if event == 'Deciphering':
            if values['-CText-'] == '':
                sg.PopupOK('Please, write cipher text')
                continue

            ciphercode = [int(code) for code in values['-CText-'].split('\n')]
            decipher_text = rsa_deciphering(ciphercode, param_d, param_n)
            window['-DText-'].update(decipher_text)
