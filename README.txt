# TODO! Пояснение к функции перестановки (описание G-функции)

numLeftOut = numRight: Первый половинный блок numLeft остается без изменений и просто копируется в numLeftOut.

numRightOut = xor(numRight, key, 2): Выполняется операция XOR между numRight и ключом key в двоичной системе счисления.

numRightOut = overwriteMode(numRightOut): Применяется функция overwriteMode, это включает в себя операции XOR с использованием трансформационной таблицы.

numRightOut = xor(numRightOut, numLeft, 2): Еще одна операция XOR, но на этот раз между numRightOut (результат предыдущего XOR) и numLeft.

Функция возвращает модифицированные значения numLeftOut и numRightOut