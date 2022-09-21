import secrets
from smartcard.util import BinStringToHexList

def hex_random_value(length:int):
    random_hex_list = (secrets.token_hex(length).upper())
    t = iter(random_hex_list)
    # print(random_hex_list)
    random_hex_list = ' '.join(a+b for a,b in zip(t, t))
    return list(bytes.fromhex(random_hex_list))

if __name__=="__main__":
    print(hex_random_value(6))
    print(hex_random_value(6))