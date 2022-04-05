import hmac
import hashlib
import base64


KEY_PATH = 'key'


def hash_file(filepath):
    with open(filepath, 'rb') as file:
        return int(hmac.new(b'', msg=file.read(), digestmod=hashlib.sha256).hexdigest(), 16)


def set_key(key):
    with open(KEY_PATH, 'w') as file:
        file.write(key)


def get_key():
    with open(KEY_PATH) as file:
        return file.read()


# dig = hmac.new(b'1234567890', msg=your_bytes_string, digestmod=hashlib.sha256).digest()
# base64.b64encode(dig).decode()      # py3k-mode
# 'Nace+U3Az4OhN7tISqgs1vdLBHBEijWcBeCqL5xN9xg='