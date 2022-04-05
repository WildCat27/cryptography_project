import argparse
from interface import sign_or_verificate
from sign import DigitalSignature


# parser = argparse.ArgumentParser()
# parser.add_argument('--path', type=str)
# args = parser.parse_args()


if __name__ == '__main__':
    sign_or_verificate(DigitalSignature())

