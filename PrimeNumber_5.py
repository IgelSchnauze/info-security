import random

import PySimpleGUI as sg

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ACC = 1000


def nod(a, b):
    mod = a % b
    while mod != 0:
        a = b
        b = mod
        mod = a % b
    return b


def raising(x, a, n):
    binary_x = f'{int(x):b}'
    r = 1
    for x_i in binary_x:
        if int(x_i) == 1:
            r = (a * r * r) % n  # a*r^2 mod n
        else:
            r = (r * r) % n  # r^2 mod n
    return r


def Jacob(a, p):
    if a == 0 or nod(a, p) != 1:
        return 0
    a = a % p

    two_deg = 0
    while a % 2 == 0:
        a = a // 2
        two_deg += 1
    s = 1 if two_deg % 2 == 0 else pow(-1, (p % 8 == 3 or p % 8 == 5))

    if a == 1:
        return s

    s *= pow(-1, (a % 4 == 3 and p % 4 == 3))
    return int(s * Jacob(p, a))


def is_prime_test_F(num):
    if num % 2 == 0:
        return False
    power = num-1
    if num < ACC:
        for a in range(2, num - 1):  # all possible a
            if nod(a, num) != 1:
                continue
            if raising(power, a, num) != 1:
                return False
    else:
        for _ in range(ACC):  # with some accuracy
            a = random.randint(2, num - 1)
            if nod(a, num) != 1:
                continue
            if raising(power, a, num) != 1:
                return False
    return True


def is_prime_test_SSh(num):
    if num % 2 == 0:
        return False
    power = (num-1)//2

    for _ in range(ACC):
        a = random.randint(2, num - 1)
        j = int(Jacob(a, num))
        j = num + j if j < 0 else j
        if raising(power, a, num) != j:
            return False
    return True


def is_prime_test_MR(num):
    if num % 2 == 0:
        return False
    t = num - 1
    two_deg_s = 0
    while t % 2 == 0:
        t //= 2
        two_deg_s += 1

    for _ in range(ACC):
        a = random.randint(2, num - 2)
        a_deg_t = raising(t, a, num)
        if a_deg_t == 1 or a_deg_t == -1 or a_deg_t == num - 1:
            continue  # this a is witness, look next

        is_witness = False
        s = 0
        while s < two_deg_s and not is_witness:
            a_deg_t = (a_deg_t * a_deg_t) % num
            if a_deg_t == -1 or a_deg_t == num - 1:
                is_witness = True  # this a is witness, look next
            s += 1

        if is_witness:
            continue
        return False  # this a isn't witness

    return True  # all a were witness


def gener_prime_F(min_len):
    a = random.randint(pow(10, min_len - 1), pow(10, min_len) - 1)
    if a%2 == 0:  # if even
        a +=1
    while True:
        if is_prime_test_F(a):
            return a
        a += 2


def gener_prime_SSh(min_len):
    a = random.randint(pow(10, min_len - 1), pow(10, min_len) - 1)
    if a%2 == 0: # if even
        a +=1
    while True:
        if is_prime_test_SSh(a):
            return a
        a += 2


def gener_prime_MR(min_len):
    a = random.randint(pow(10, min_len - 1), pow(10, min_len) - 1)
    if a%2 == 0: # if even
        a +=1
    while True:
        if is_prime_test_MR(a):
            return a
        a += 2


if __name__ == '__main__':
    sg.theme('DarkBrown')
    font_window = ('Arial 12 bold')
    font_input = ('Arial 12')
    # заполнение разметки окна - лист из листов
    layout = [
        [sg.Text('Input some number:', font=font_window),
          sg.InputText(size=(45, 2), font=font_input, key='-input_num-'),
          sg.Button('It\'s prime?', font=font_window)],
        [sg.Text('Test F:', font=font_input, size=(15, 1)), sg.Text('Test S-Sh:', font=font_input, size=(15, 1)),
         sg.Text('Test M-R:', font=font_input, size=(15, 1))],
        [sg.Text(size=(15, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-TestF-'),
         sg.Text(size=(15, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-TestSSh-'),
         sg.Text(size=(15, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-TestMR-'),
         sg.Text('(probably prime/composite)', font=font_input)],
        [sg.Text('\n\n')],
        [sg.Text('Input some min number of bits:', font=font_window),
         sg.InputText(size=(7, 1), font=font_input, key='-bits_num-'),
         sg.Text(' , and choose method:', font=font_window)],

        [sg.Radio('Test Ferm', "Test", font=font_window, default=True, size=(11, 1), key='-test1-'),
         sg.Multiline(size=(55, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-primeF-')],
        [sg.Radio('Test S-Sh', "Test", font=font_window, size=(11, 1),  key='-test2-'),
         sg.Multiline(size=(55, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-primeSSh-')],
        [sg.Radio('Test M-R', "Test", font=font_window, size=(11, 1),  key='-test3-'),
         sg.Multiline(size=(55, 1), background_color='lightgray', font=font_input, text_color='SteelBlue4', key='-primeMR-')],

        [sg.Button('Generate prime', font=font_window)],
        [sg.Button('Clear all', font=font_input, button_color='gray23')]
    ]
    window = sg.Window('Test for prime from KVA', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        if event == 'It\'s prime?':
            num = values['-input_num-'].replace(' ', '')
            if not all(sym in numbers for sym in num) or num == '':
                sg.PopupOK('Write only number please, no punctuation or letters')
                continue

            window['-TestF-'].update(
                'pr. prime' if is_prime_test_F(int(num)) else 'composite'
            )
            window['-TestSSh-'].update(
                'pr. prime' if is_prime_test_SSh(int(num)) else 'composite'
            )
            window['-TestMR-'].update(
                'pr. prime' if is_prime_test_MR(int(num)) else 'composite'
            )

        if event == 'Generate prime':
            bits_num = values['-bits_num-'].replace(' ', '')
            if not all(sym in numbers for sym in bits_num) or bits_num == '':
                sg.PopupOK('Write only number please, no punctuation or letters')
                continue

            _ = f'{pow(10, int(bits_num))}'  # some binary this length
            num_min_len = len(f'{int(_, 2)}')  # length decimal

            if values['-test1-']:
                window['-primeF-'].update(gener_prime_F(num_min_len))

            if values['-test2-']:
                window['-primeSSh-'].update(gener_prime_SSh(num_min_len))

            if values['-test3-']:
                window['-primeMR-'].update(gener_prime_MR(num_min_len))

        if event == 'Clear all':
            window['-primeMR-'].update('')
            window['-primeSSh-'].update('')
            window['-primeF-'].update('')

            window['-TestMR-'].update('')
            window['-TestSSh-'].update('')
            window['-TestF-'].update('')
