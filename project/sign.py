from elliptic import Elliptic, Point, Galua
import json
from interface import login_or_register
from project.interface import show_info
from sign_center import SignCenter

from hash import hash_file
from interface import get_d, get_elliptic, get_filepath, get_keys_filepath, get_or_create_keys, get_password, get_point, get_q, get_r, get_username, show_verificate_results



class DigitalSignature:
    
    def __init__(self) -> None:
        self.elliptic = None
        self.public_key = None
        self.secret_key = None
        self.sign_center = SignCenter()
        self.username = None
        self.password = None

    def generate_keys(self):
        # генерация ключей в эллептических кривых
        a, b, p = get_elliptic()
        self.elliptic = Elliptic(a, b, p)

        u, v = get_point(self.elliptic._generate_points())
        e1 = Point(u, v)

        self.secret_key = get_d()
        e2 = self.elliptic.a_multiplication(e1, self.secret_key)
        self.public_key = self.elliptic.a, self.elliptic.b, self.elliptic.p, get_q(), e1, e2

        self.save_keys()

        return self.public_key

    def login(self, username, password):
        # авторизация в центре доверия
        self.sign_center.register(username, password)
        self.username = username
        self.password = password


    def register(self, username, password):
        # регистрация в центре доверия
        self.sign_center.register(username, password)
        self.username = username
        self.password = password

    def sign_file(self):
        # подпись файла
        get_or_create_keys(self)
        login_or_register(self)
        self.sign_center.set_pulic_key(self.username, self.password, self.public_key)
        _, _, _, q, e1, _ = self.public_key
        point = None
        while not Point:
            show_info('При умножении r * e1 получена нулевая точка. Введите другое r')
            r = get_r(q)
            point = self.elliptic.a_multiplication(e1, r)
        s1 = point.x % q
        filepath = get_filepath()
        hash = hash_file(filepath)
        s2 = ((hash + self.secret_key * s1) * Galua(q).mult_inv(r)) % q
        self.save_file_signature(filepath, s1, s2)


    def verificate_file(self):
        username = get_username()
        a, b, p, q, e1, e2 = self.sign_center.get_public_key(username)
        elliptic = Elliptic(a, b, p)
        filepath = get_filepath()
        s1, s2 = self.get_file_signature(filepath)
        inv_s2 = Galua(q).mult_inv(s2)
        a = hash_file(filepath) * inv_s2 % q
        b = inv_s2 * s1 % q
        t = elliptic.addition(elliptic.a_multiplication(e1, a), elliptic.a_multiplication(e2, b))
        show_verificate_results(username, t.x == (s1 % q))

    
    def save_keys(self):
        public = get_keys_filepath()
        private = public + '_private'
        a, b, p, q, e1, e2 = self.public_key
        data = {
            'a': a,
            'b': b,
            'p': p,
            'q': q,
            'e1': {
                'x': e1.x,
                'y': e1.y,
            },
            'e2': {
                'x': e2.x,
                'y': e2.y,
            },
        }
        with open(public, 'w') as file:
            json.dump(data, file)

        with open(private, 'w') as file:
            file.write(str(self.secret_key))


    def get_keys(self):
        public = get_keys_filepath()
        private = public + '_private'
        with open(public) as file:
            data = json.load(file)
            e1 = Point(data['e1']['x'], data['e1']['y'])
            e2 = Point(data['e2']['x'], data['e2']['y'])
            self.public_key = data['a'], data['b'], data['p'], data['q'], e1, e2
            self.elliptic = Elliptic(data['a'], data['b'], data['p'])

        with open(private) as file:
            self.secret_key = int(file.read())

    def save_file_signature(self, filepath, s1, s2):
        data = {
            's1': s1,
            's2': s2,
        }
        file_signature_path = filepath + '.sg'
        with open(file_signature_path, 'w') as file:
            json.dump(data, file)

    
    def get_file_signature(self, filepath):
        file_signature_path = filepath + '.sg'
        with open(file_signature_path, 'w') as file:
            data = json.load(file)
            return data['s1'], data['s2']

