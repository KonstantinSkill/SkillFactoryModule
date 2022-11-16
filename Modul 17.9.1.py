print(f'Здравствуйте. Данная программа:\n'
      f'    1. Принимает последовательность чисел \n'
      f'    2. Преобразует последовательность в список \n'
      f'    3. Выстраивает числа в списке по порядку \n'
      f'А также находит индексы ближайших чисел в списке для введенного Вами числа.')
sequence = input(f'\nВведите целые числа через пробел:\t')
number = int(input(f'\nВведите любое целое число:\t'))
error = 'f\nПожалуйста, перезапустите программу'

# Определяем цифры в строке

def is_int(str):
    str = str.replace(' ', '')
    try:
        int(str)
        return True
    except ValueError:
        return False

# Проверка соответствия условию и преобразование строки в список

if " " not in sequence:
    print(f'\nВ последовательности отсутствуют пробелы')
    raise ValueError (error)
if not is_int(sequence):
    print(f'\nВ последовательности присутствуют недопустимые значения)\n')
    raise ValueError(error)
else:
     sequence = sequence.split()

# Формирование списка чисел

list_sequence = [int(item) for item in sequence]

# Функция сортировки по возрастанию с помощью встроенной функции - sorted ()

def sort (lst):
    return sorted (lst)

# Функция двоичного поиска элемента в списке

def binary_search(array, element, left, right):
    try:
        if left > right:
            return False
        middle = (right + left) // 2
        if array[middle] == element:
            return middle
        elif element < array[middle]:
            return binary_search(array, element, left, middle - 1)
        else:
            return binary_search(array, element, middle + 1, right)
    except IndexError:
        return f'\nВаше число вне диапазона последовательности.'

# Сортируем список и выводим последовательность

list_sequence = sort (list_sequence)
print (f'\nПоследовательность введеных Вами чисел в порядке возрастания:\n \t', list_sequence)

# Установление возможной позиции нового числа
# Определения большего и меньшего числа и их индексы

if not binary_search(list_sequence, number, 0, len(list_sequence)):
    rI = min(list_sequence, key=lambda x: (abs(x - number), x))
    ind = list_sequence.index(rI)
    max_ind = ind + 1
    min_ind = ind - 1
    if rI < number:
        print(f'В списке нет введенного элемента \n'
              f'Ближайший меньший элемент:\t {rI}\t, его индекс:\t {ind}\n'
              f'Ближайший больший элемент:\t {list_sequence[max_ind]}\t, его индекс:\t {max_ind}')
    elif min_ind < 0:
        print(f'В списке нет введенного элемента\n'
              f'Ближайший больший элемент:\t {rI},\t его индекс:\t {list_sequence.index(rI)}\n'
              f'В списке нет меньшего элемента')
    elif rI > number:
        print(f'В списке нет введенного элемента\n'
              f'Ближайший больший элемент:\t {rI},\t его индекс:\t {list_sequence.index(rI)}\n'
              f'Ближайший меньший элемент:\t {list_sequence[min_ind]},\t его индекс:\t {min_ind}')
    elif list_sequence.index(rI) == 0:
        print(f'Индекс введенного элемента:\t {list_sequence.index(rI)}')
else:
    print(f'Индекс введенного элемента:\t {binary_search(list_sequence, number, 0, len(list_sequence))}')