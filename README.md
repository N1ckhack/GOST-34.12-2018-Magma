> **Created by N1ck, 2023**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) [![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/n1ck_dv)
# ГОСТ 34.12-2018 — _МАГМА_
#### _ГОСТ 34.12 - это стандарт криптографической защиты информации. В России и некоторых других странах СНГ это общепринятый стандарт, устанавливающий требования к методам и алгоритмам шифрования информации._



##### *Полезные ссылки:*
1. [Шифруем по-русски, или отечественные криптоалгоритмы](https://habr.com/ru/articles/530816/ "Habr")
2. [Лекция Шакурского М. В. по криптографическому стандарту МАГМА](https://disk.yandex.ru/i/O2_2oAbzo3ohEA "Яндекс.Диск")
3. [Русская Магма](https://spy-soft.net/magma-encryption/ "xаker.ru")

ГОСТ 34.12 представляет собой набор алгоритмов блочного шифрования, используемых для защиты информации, включая шифрование данных и создание цифровой подписи.

![alt-текст](https://habrastorage.org/r/w1560/getpro/habr/upload_files/728/134/d27/728134d27b9f8c7d6d8c52e8329532f1.png "Общая структура работы алгоритма Магма:")

### Пояснения к работе G-функции (функция `transformation`)
1. `numLeftOut = numRight`: Первый половинный блок numLeft остается без изменений и просто копируется в `numLeftOut`.
2. `numRightOut = xor(numRight, key, 2)`: Выполняется операция XOR между numRight и ключом key в двоичной системе счисления.
3. `numRightOut = overwriteMode(numRightOut)`: Применяется функция overwriteMode, это включает в себя операции XOR с использованием трансформационной таблицы.
4. `numRightOut = xor(numRightOut, numLeft, 2)`: Еще одна операция XOR, но на этот раз между `numRightOut` (результат предыдущего XOR) и `numLeft`.
5. Функция возвращает модифицированные значения `numLeftOut` и `numRightOut`

## Troubleshooting
В ранних версиях **PyCharm** возможны ошибки с конструкцией вида: `transformKey(key) -> str`.
Если у вас возникла такая ошибка, просто удалите ожидаемый результат, убрав `-> str`.
## License

MIT

**Free Software, GLHF!**
