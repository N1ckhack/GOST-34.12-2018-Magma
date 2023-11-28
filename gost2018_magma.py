import binascii
alphabet = '0123456789abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'

transformation_table = [
    [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2],
    [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
    [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
    [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
    [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
    [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
    [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
    [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1]
]

# TODO! функция перестановки (G)
#   принимает два блока (половины) числа numLeft и numRight, а также ключ key
def transformation(numLeft, numRight, key):
    numLeftOut = numRight #меняем местами две половины ключа
    numRightOut = xor(numRight, key, 2) #XORим правую часть с ключом
    numRightOut = overwriteMode(numRightOut)
    numRightOut = xor(numRightOut, numLeft, 2) #XORим левую и правую части
    return numLeftOut, numRightOut

# TODO! Генерация раундовых подключей
def cutKey(key):
    key = convertBase(key, 2, 16) #перевод ключа в двоичную форму
    keys = []
    for i in range(3): #Два вложенных цикла используются для добавления первых
                    # 24 (3 * 8) подключей. Каждое подключение представляет собой
                    # последовательность из 32 бит, взятую из исходного ключа.
        for j in range(8):
            keys.append(key[j * 32 : j * 32 + 32])
    for i in range(7, -1, -1): #добавляются 8 подключей в обратном порядке
        keys.append(key[i * 32 : i * 32 + 32])
    return keys

#TODO! Функция, выполняющая 32 раунда шифрования (опционально дешифрования, если сменим flag на reverse)
def TransformChain(numLeft, numRight, key, flag = 'straight'):
    if flag == 'reverse':
        start = 31
        stop = 0
        step = -1
        last = 0
    else:
        start = 0
        stop = 31
        step = 1
        last = 31
    for i in range(start, stop, step):
        numLeft, numRight = transformation(numLeft, numRight, key[i]) #На каждой итерации цикла вызывается функция
                                                                    # transformation для выполнения преобразования с
                                                                    # использованием соответствующего ключа key[i]
    numRightLast = numRight #Фиксируется последнее состояние правого блока
    numLeft, numRight = transformation(numLeft, numRight, key[last]) # В финальный раунд передаются две части блока
                                                            # и шифруются/дешифруются при помощи ключа и G-функции
    return numRight + numRightLast # две части входного блока склеиваются

# TODO! Преобразуем входной текст в UTF-8 из HEX
def hexToUtf8(text):
    text = binascii.unhexlify(text).decode('utf8')
    return text

#TODO! Обратная функция: преобразует UTF-8 в HEX
def utf8ToHex(text):
    text = binascii.hexlify(text.encode('utf8')).decode('utf8')
    return text

# TODO! Реализация XOR
def xor(num1, num2, in_code = 2): #Здесь in_code = 2 указывает на СС, в котороый мы складываем
    len1 = len(str(num1)) #Определяем длинну
    num1 = int(num1, in_code)
    num2 = int(num2, in_code)

    num = str(bin(num1 ^ num2)[2:]) #Здесь [2:] указывает на то, что мы отбросим на выходе типовой блок 0b
                                    #для двоичной системы
    num = zeros_before_number(num, len1)

    return num

#TODO! добавляет нули в начало числа num1, чтобы длина числа стала равной указанной длине length
def zeros_before_number(num1, length) -> str:
    num1 = str(num1)
    if len(str(num1)) != length: #проверяет, нужно ли добавлять нули.
        for i in range(length - len(str(num1))):
            num1 = '0' + num1
    return num1

# TODO! добавляет нули в конец числа num1, чтобы длина числа стала равной указанной длине length
def zeros_after_number(num1, length) -> str:
    num1 = str(num1)
    if len(str(num1)) != length:
        for i in range(length - len(str(num1))):
            num1 = num1 + '0'
    return num1

# TODO! Функция преобразования входных бит
def overwriteMode(bitNumberIn):
    bitNumberInOut = '' #пустая строка bitNumberInOut, которая будет
                        #использоваться для хранения результатов операций.
    for i in range(8): #Выбирается последовательность из 4 бит из входного числа bitNumberIn
        num1 = bitNumberIn[i * 4: i * 4 + 4]
        num2 = bin(transformation_table[i][int(bitNumberIn[i * 4: i * 4 + 4], 2)])[2:]
        #Выполняется доступ к перестановочной таблице
        #transformation_table, и возвращается результат в бинарной форме.
        #Этот результат представляет собой переставленные 4 бита из входного числа
        num2 = zeros_before_number(num2, 4)

        bitNumberInOut += xor(num1, num2, 2)
        # Выполняется операция XOR над num1 и num2, и результат добавляется к строке bitNumberInOut.
    return bitNumberInOut


# TODO! преобразует число из одной системы счисления в другую, возвращая его представление
#   в виде строки в новой системе счисления
def convertBase(num, toBase = 10, fromBase = 10) -> str | int:
    # конвертация в десятичное число входной строки
    if isinstance(num, str):
        n = int(num, fromBase) # проверяем
    else:
        n = int(num)

    # преобразование десятичного числа в требуемую систему счисления
    if n < toBase:
        return alphabet[n]
    else:
        return convertBase(n // toBase, toBase) + alphabet[n % toBase]
    # к результату добавляется цифра, соответствующая остатку от деления на toBase. Рекурсивный вызов продолжается до
    # тех пор, пока n не станет меньше toBase, и цифры начнут добавляться в обратном порядке.
    # Результат возвращается как строка

# TODO! Расширение ключа
def transformKey(key) -> str:
    key = binascii.hexlify(key.encode('utf8')).decode('utf8')
    count = 64 - len(key) % 64 #проверка кратности 64
    while len(key) < 64:
        key += key
    return key[:64]


# TODO! Функция ШИФРОВАНИЯ
def encrypt(text, key):
    key = transformKey(key)
    key = cutKey(key)
    text = convertBase(utf8ToHex(text), toBase = 2, fromBase = 16)
    if len(text) % 8 != 0: # проверяется длина входного текста, если не кратна 8, то дополняется пустыми символами
        text = zeros_before_number(text, (len(text) // 8)  * 8 + 8)
    textArray = [] #список который будет использоваться для хранения блоков текста, предназначенных для шифрования.
    textEncrypt = ''
    for i in range(len(text) // 64 + 1): #Цикл разбивает входной текст на блоки по 64 бита (8 байт)
        textForAppend = text[i * 64 : i * 64 + 64]
        textForAppend = zeros_after_number(textForAppend, 64)
        textArray.append(textForAppend)
    for i in range(len(textArray)):
        textEncrypt += TransformChain(textArray[i][:32], textArray[i][32:], key)
    textEncrypt = convertBase(textEncrypt, toBase = 16, fromBase = 2)
    return textEncrypt

# TODO! Функция ДЕШИФРОВАНИЯ
def decrypt(text, key):
    key = transformKey(key)
    key = cutKey(key)
    text = convertBase(text, toBase = 2, fromBase = 16)
    if len(text) % 8 != 0:
        text = zeros_before_number(text, (len(text) // 8)  * 8 + 8)
    textArray = []
    textDecrypt = ''
    if (len(text) // 64 * 64) != len(text):
        count = len(text) // 64 + 1
    else:
        count = len(text) // 64
    for i in range(count):
        textForAppend = text[i * 64 : i * 64 + 64]
        textForAppend = zeros_after_number(textForAppend, 64)
        textArray.append(textForAppend)
    for i in range(len(textArray)):
        textDecrypt += TransformChain(textArray[i][:32], textArray[i][32:], key, flag = 'reverse')
    textDecrypt = convertBase(textDecrypt, toBase = 16, fromBase = 2)
    return textDecrypt

