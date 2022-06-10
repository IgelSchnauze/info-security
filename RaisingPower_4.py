import PySimpleGUI as sg

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def raising(binary_x, a, n):
    r = 1
    for x_i in binary_x:
        if int(x_i) == 1:
            r = (a * r * r) % n  # a*r^2 mod n
        else:
            r = (r * r) % n  # r^2 mod n
    return r


if __name__ == '__main__':
    sg.theme('DarkBrown')
    font_window = ('Arial 12 bold')
    font_input = ('Arial 12')
    # заполнение разметки окна - лист из листов
    layout = [
        [sg.Text('z = (a^x) mod n', font=font_window)],
        [sg.Text('a: ', font=font_window),
         sg.InputText(size=(20, 2), font=font_input, key='-a-'),
         sg.Text('x: ', font=font_window),
         sg.InputText(size=(20, 2), font=font_input, key='-x-'),
         sg.Text('n: ', font=font_window),
         sg.InputText(size=(20, 2), font=font_input, key='-n-')],
        [sg.Button('Find "z"', font=font_window)],
        [sg.Text('z: ', font=font_window),
         sg.Text(size=(22, 1), background_color='darkgray', font=font_input, text_color='SteelBlue4', key='-z-')],
    ]
    window = sg.Window('Fast raising to power from KVA', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        if event == 'Find "z"':
            a = values['-a-'].replace(' ', '')
            x = values['-x-'].replace(' ', '')
            n = values['-n-'].replace(' ', '')
            window['-a-'].update(a)
            window['-x-'].update(x)
            window['-n-'].update(n)

            if not all(sym in numbers for sym in a) \
                    or not all(sym in numbers for sym in x) \
                    or not all(sym in numbers for sym in n):
                sg.PopupOK('Oh, input data need be only numbers, no punctuation or letters')
                window['-z-'].update('')
                continue

            if n == '0':
                sg.PopupOK('Oh, mod can not be zero')
                window['-z-'].update('')
                continue

            z = raising(f'{int(x):b}', int(a), int(n))
            window['-z-'].update(z)
