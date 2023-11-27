import gost2018_magma as magma
from random import choice

text = input('Введите секретный текст: ')
key = ''.join(choice(magma.alphabet) for i in range(48)) #mypassw0rd
print('Ключ:', key)

# Шифрование
textEncrypt = magma.encrypt(text, key)
print('Зашифрованный текст: ', textEncrypt)

# Расшифровка
textDecrypt = magma.decrypt(textEncrypt, key)
print('Расшифрованный текст: ', magma.hexToUtf8(textDecrypt))