def get_elliptic():
    print('Введите данные эллептической кривой (a, b, p)')
    print('>>', end=' ')
    a, b, p = (int(s) for s in input().split(' '))
    return a, b, p


def get_q():
    print('Введите простое q')
    print('>>', end=' ')
    return int(input())


def get_d():
    print('Введите сектретный ключ d')
    print('>>', end=' ')
    return int(input())


def get_point(points):
    print('Выберите точку прямой')
    print(points)
    print('Введите координаты точки')
    print('>>', end=' ')
    u, v = (int(s) for s in input().split(' '))
    return u, v


def get_r(q):
    print('Введите r от 1 до {}'.format(q - 1))
    print('>>', end=' ')
    return int(input())


def get_filepath():
    print('Введите путь до подписываемого файла')
    print('>>', end=' ')
    return input()


# def enter():
#     answer = None
#     while answer is None:
#         print('Сгенировать новый ключ? [Y/n]')
#         answer_str = input()

#         if answer_str in ['Y', 'y']:
#             answer = True

#         if answer_str in ['N', 'n']:
#             answer = False

#     return answer


def get_keys_filepath():
    print('Введите путь до публичного ключа')
    print('>>', end=' ')
    return input()


def get_username():
    print('Введите имя пользователя')
    print('>>', end=' ')
    return input()


def get_password():
    print('Введите пароль')
    print('>>', end=' ')
    return input()


def show_verificate_results(username, result):
    if result:
        print(f'Файл подписан пользователем {username}')

    else:
        print(f'Файл не был подписан пользователем {username}')


def login_or_register(ds):
    print('1 - Войти\n2 - Зарегистрироваться')
    print('>>', end=' ')
    command = input()
    if command == '1':
        ds.login(get_username(), get_password())

    if command == '2':
        ds.register(get_username(), get_password())


def get_or_create_keys(ds):
    print('1 - Сгенирировать новый ключ\n2 - Загрузить ключ')
    print('>>', end=' ')
    command = input()
    if command == '1':
        ds.generate_keys()

    if command == '2':
        ds.get_keys()

def sign_or_verificate(ds):
    print('1 - Подписать файл\n2 - Проверить файл')
    print('>>', end=' ')
    command = input()
    if command == '1':
        ds.sign_file()

    if command == '2':
        ds.verificate_file()

def show_info(message):
    print(message)

def get_hash_password():
    print('Введите')