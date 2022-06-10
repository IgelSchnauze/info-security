import PySimpleGUI as sg
import time

from PrimeNumber_5 import nod, raising
from Euclid_4 import ee_algorithm

rus_alph = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й',
            'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
            'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я',
            'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й',
            'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']  # 16-79
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def method_pollard(n):
    p, q = 1, 1
    x_i = 2
    y_i = 1

    i = 1
    start = time.time()
    while True:
        _nod = nod(abs(x_i-y_i), n)
        if _nod > 1 and _nod != n:
            p, q = _nod, n//_nod
            break
        y_i = x_i if (i & (i-1) == 0) else y_i
        x_i = (x_i*x_i - 1) % n
        if i%10000000 == 0:
            print(f'{i}:  x = {x_i}, y = {y_i}, nod={_nod}')
        i += 1
        # if i > 200000:
        #     break

    end = time.time()
    return p, q, end-start, i


def hacking_rsa(cipher_text, n, e):
    p, q, time, iter_num = method_pollard(n)

    phi_n = (p-1) * (q-1)
    _, d, _ = ee_algorithm(phi_n, e)
    orig_text_code = str(raising(d, cipher_text, n))

    orig_text = ""
    for i in range(0, len(orig_text_code)-1, 2):
        sym_code = int(orig_text_code[i] + orig_text_code[i+1])
        if (sym_code >= 16) and (sym_code <= 79):
            orig_text += rus_alph[sym_code - 16]
        else:
            orig_text += "<error>"

    return orig_text, p, q, time, iter_num


if __name__ == '__main__':
    sg.theme('DarkBrown')
    font_window = ('Arial 12 bold')
    font_input = ('Arial 12')
    # заполнение разметки окна - лист из листов
    layout = [
        [sg.Text('Input ciphertext, N, e:', font=font_window)],
        [sg.Multiline(size=(50, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4',
                      key='-Text-')],
        [sg.Multiline(size=(50, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4',
                      key='-n-')],
        [sg.Multiline(size=(50, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4',
                      key='-e-')],
        [sg.Button('Hacking', font=font_window)],
        [sg.Text('Message text:', font=font_window)],
        [sg.Text(size=(50, 3), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-HText-')],
        [sg.Text('\n')],
        [sg.Text('p - ', font=font_window), sg.Text(font=font_input, key='-p-')],
        [sg.Text('q - ', font=font_window), sg.Text(font=font_input, key='-q-')],
        [sg.Text('time of hack: ', font=font_window), sg.Text(font=font_input, key='-time-')],
        [sg.Text('num of iterations: ', font=font_window), sg.Text(font=font_input, key='-iter-')],
    ]
    window = sg.Window('Hacking from KVA', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        if event == 'Hacking':
            cipher_text = values['-Text-'].replace(' ', '')
            n = values['-n-'].replace(' ', '')
            e = values['-e-'].replace(' ', '')

            if cipher_text == '' or n == '' or e == '':
                sg.PopupOK('Please, write input text and number or bits')
                continue
            if not all([num in numbers for num in cipher_text]):
                sg.PopupOK('Ciphertext is only nUmBEr!')
                continue
            if not all([num in numbers for num in n]):
                sg.PopupOK('N is only nUmBEr!')
                continue
            if not all([num in numbers for num in e]):
                sg.PopupOK('e is only nUmBEr!')
                continue

            message_text, p, q, time, iter_num = hacking_rsa(int(cipher_text), int(n), int(e))
            # print(f'{int(time//60)} min {time%60:.3f} sec')

            window['-HText-'].update(message_text)
            window['-p-'].update(p)
            window['-q-'].update(q)
            # window['-time-'].update(f'{time:.3f} sec')
            window['-time-'].update(f'{int(time//60)} min {time%60:.3f} sec')
            window['-iter-'].update(iter_num)
