import PySimpleGUI as sg

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def ee_algorithm(a, b):
    mod, div_arr, x_arr, y_arr = a % b, [], [], []
    div_arr.append(a // b)

    while len(div_arr) == 0 or mod != 0:
        a = b
        b = mod
        mod = a % b
        div_arr.append(a // b)

    x_arr.append(0)
    y_arr.append(1)
    for i in range(len(div_arr) - 2, -1, -1):
        x_arr.append(y_arr[-1])
        y_arr.append(x_arr[-2] - (div_arr[i] * x_arr[-1]))

    return x_arr[-1], y_arr[-1], b


if __name__ == '__main__':
    sg.theme('DarkBrown')
    font_window = ('Arial 12 bold')
    font_input = ('Arial 12')
    # заполнение разметки окна - лист из листов
    layout = [
        [sg.Text('Ax + By = НОД(A, B)', font=font_window)],
        [sg.Text('A: ', font=font_window),
         sg.InputText(size=(20, 2), font=font_input, key='-a-'),
         sg.Text('B: ', font=font_window),
         sg.InputText(size=(20, 2), font=font_input, key='-b-')],
        [sg.Button('Find x, y and НОД', font=font_window)],
        [sg.Text('x: ', font=font_window),
         sg.Text(size=(20, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-x-'),
         sg.Text('y: ', font=font_window),
         sg.Text(size=(20, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-y-'),
         sg.Text('НОД: ', font=font_window),
         sg.Text(size=(15, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-nod-')],
    ]
    window = sg.Window('Extended Euclid algorithm from KVA', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        if event == 'Find x, y and НОД':
            a = values['-a-'].replace(' ', '')
            b = values['-b-'].replace(' ', '')
            window['-a-'].update(a)
            window['-b-'].update(b)

            if not all(sym in numbers for sym in a) \
                    or not all(sym in numbers for sym in b):
                sg.PopupOK('Oh, input data need be only numbers, no punctuation or letters')
                window['-x-'].update('')
                window['-y-'].update('')
                window['-nod-'].update('')
                continue

            if b == '0':
                sg.PopupOK('Please, do not use zero values in B')
                window['-x-'].update('')
                window['-y-'].update('')
                window['-nod-'].update('')
                continue

            x, y, nod = ee_algorithm(int(a), int(b))
            window['-x-'].update(x)
            window['-y-'].update(y)
            window['-nod-'].update(nod)
