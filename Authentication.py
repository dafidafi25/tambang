from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad,unpad
from hashlib import md5






def encrypt(plain_text, key1,key2="TuhasAkhirISTTS@2022"):
    # generate a random salt
    salt = bytearray(key2.encode())
    

    # use the Scrypt KDF to get a private key from the key1
    private_key = hashlib.scrypt(
        key1.encode(), salt=salt, n=2, r=8, p=1, dklen=32)

    # create cipher configte
    cipher_config = AES.new(private_key, AES.MODE_GCM)


    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))

    chiper = b64encode(cipher_text).decode('utf-8') + "<=N=>" + b64encode(cipher_config.nonce).decode('utf-8') + "<=T=>" + b64encode(tag).decode('utf-8')



    return chiper

def decrypt(chiper, key1,key2 = "TuhasAkhirISTTS@2022"):

    salt = bytearray(key2.encode())
    cipher_text = b64decode(chiper[0:chiper.index("<=N=>")])
    nonce = b64decode(chiper[chiper.index("<=N=>")+5: chiper.index("<=T=>")])
    tag =b64decode( chiper[chiper.index("<=T=>")+5:len(chiper)])

    # generate the private key from the key1 and salt
    private_key = hashlib.scrypt(
        key1.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted


class AESCipher:
    def __init__(self, key):
        self.key = md5(key.encode('utf8')).digest()

    def encrypt(self, data):
        iv = bytes.fromhex("00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15")
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data.encode('utf-8'), 
            AES.block_size)))

    def decrypt(self, data):
        raw = b64decode(data)
        self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)


if __name__ == "__main__":
    # password = key1
    # # First let us encrypt secret message
    # encrypted = encrypt(plain_text="FF FF D6 B5 52 08 04 00 62 63 FF FF FF FF FF FF",key1= password,key2="60000")
    # print(encrypted)

    # # Let us decrypt using our original password
    # # decrypted = decrypt(encrypted, password,key2="60000")
    # # print(bytes.decode(decrypted))
    key1 = "MayoraInvesta@2022"
    key2 = "TuhasAkhirISTTS@2022"

    cipher_text = AESCipher(key1).encrypt("FF FF D6 B5 52 08 04 00 62 63 FF FF FF FF FF FF")
    print(cipher_text)
    # print('TESTING ENCRYPTION')
    # msg = input('Message...: ')
    # pwd = input('Password..: ')
    # print('Ciphertext:', AESCipher(pwd).encrypt(msg).decode('utf-8'))


    # print('\nTESTING DECRYPTION')
    # cte = input('Ciphertext: ')
    # pwd = input('Password..: ')
    # print('Message...:', AESCipher(pwd).decrypt(cte).decode('utf-8'))

