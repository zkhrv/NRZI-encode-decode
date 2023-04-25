import matplotlib.pyplot as plt # импортируем модуль для построения графиков
import matplotlib.ticker as ticker # импортиурем модуль для настройки меток на осях графика
import timeit # импортируем библиотеку для подсчета времени выполнения кодирования

def string_to_bits(s): # метод перевода строки s в биты
    bits = [] # список для хранения битов
    for char in s.encode('cp1251'): # Перебираем символы строки s в кодировке cp1251
        bits.extend([bin(char)[2:].zfill(8)]) # Преобразуем символ в битовую строку и добавляем ее в список
    return ''.join(bits) # возвращаем битовую строку

def bits_to_string(b): # метод перевода бит в строку
    chars = [] # Список для хранения символов
    for i in range(0, len(b), 8): # Перебираем битовую строку по 8 символов
        chars.append(int(b[i:i+8], 2)) # Преобразуем 8 символов в число и добавляем его в список
    return bytes(chars).decode('cp1251') # Возвращаем строку в кодировке cp1251

def nrzi_signal(signal_levels, encoded_signal): #
    x = [0]  # начинаем отрисовку с нулевой точки
    y = [0]  # начинаем отрисовку с нулевой точки

    current_level = 0 #  Переменная для хранения текущего уровня сигнала
    for bit in signal_levels: #  Перебираем биты закодированного сигнала
        if bit == '1': # Если бит равен 1
            current_level = 1 - current_level  # меняем состояние с 0 на 1 или с 1 на 0
        x.append(x[-1])  # оставляем координату x неизменной
        y.append(current_level)  # задаем координату y текущего уровня
        x.append(x[-1]+1)  # переходим на следующую координату x
        y.append(current_level)  # продолжаем рисовать график на текущем уровне

    plt.plot(x, y, color='red', linewidth=3) # указываем параметры для графика сигнала
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1)) # устанавливаем стороны клетки поля графика 
    plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(1)) # устанавливаем стороны клетки поля графика
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1)) # устанавливаем стороны клетки поля графика
    plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(1)) # устанавливаем стороны клетки поля графика
    plt.grid(which='both', color='k', linewidth=1) # указываем параметры для сетки поля 
    plt.title('NRZI Encoding') # указываем заголовок графика
    plt.xlabel('Bit') # указываем название для оси X
    plt.ylabel('Signal level') # указываем название для оси Y
    plt.suptitle(encoded_signal) # указываем заголовок всего графика. В заголовок, для удобства, я решил вписать биты сигнала 
    plt.show() 

def nrzi_encode_decode(): # метод для кодирования/декодирования
    input_string = input("Введите строку для кодирования: ") # вводим строку, которую хотим закодировать 
    # Кодирование
    start_time = timeit.default_timer() # запускаем таймер 
    bits = string_to_bits(input_string) # принимаем биты строки 
    signal = '1' # задаем значение переменной signal, которое используется для кодирования сигнала
    encoded_signal = '' # инициализируем переменную encoded_signal пустой строкой, в нее будут добавляться закодированные биты
    for bit in bits: # Перебираем биты из аргумента функции bits
        if bit == '0': # Если текущий бит равен 0
            encoded_signal += signal #  Добавляем в закодированный сигнал символ из переменной signal
        else: # Иначе
            signal = '0' if signal == '1' else '1' #  Меняем значение переменной signal на противоположное
            encoded_signal += signal # Добавляем в закодированный сигнал символ из переменной signal
    end_time = timeit.default_timer() # останавливаем таймер
    time = end_time - start_time # считаем время, затраченное на кодировку    

    current_level = 0 # переменная для хранения текущего уровня сигнала
    signal_levels = "" # пустая строка, в которую будем добавлять уровни сигнала
    for bit in encoded_signal: # перебор всех битов в строке 
        if bit == '1': # если значение равно 1
            current_level = 1 - current_level # меняем состояние на противоположное  
        signal_levels += str(current_level) # добавление текущее значение в переменную для уровней сигнала

    print("Кодированные биты: ", encoded_signal)
    print("Уровни сигнала:", signal_levels)
    print("Время кодирования:", "{:.8f}".format(time))

    current_level = 0 # переменная для хранения текущего уровня сигнала
    decoded_signal_levels = '' # пустая строка, в которую будем добавлять биты 
    for level in signal_levels: # цикл по всем уровня сигнала
        if level == str(current_level): #  проверяем, равен ли текущий уровень сигнала current_level уровню в level
            decoded_signal_levels += '0' # сли да, то добавляем в строку bits значение 0
        else: # иначе
            decoded_signal_levels += '1' # если нет, то добавляем 1 и изменяем значение current_level на противоположное 
            current_level = 1 - current_level 

    # Декодирование
    decoded_bits = '' # инициализируем переменную decoded_bits пустой строкой, в нее будут добавляться декодированные символы
    signal = '1' # задаем значение переменной signal, которое используется для декодирования сигнала
    for i in range(0, len(decoded_signal_levels)): # Перебираем все биты в закодированном сигнале
        if encoded_signal[i] == signal: # Если текущий бит равен символу из переменной signal
            decoded_bits += '0' # Добавляем в декодированные биты символ 0
        else: # Иначе
            decoded_bits += '1' # Добавляем в декодированные биты символ 1
            signal = encoded_signal[i] # Обновляем значение переменной signal на текущий символ из закодированного сигнала
    decoded_string = bits_to_string(decoded_bits) # Преобразуем декодированные биты в строку с помощью метода bits_to_string
    print("Декодированная строка: ", decoded_string)

    nrzi_signal(encoded_signal, signal_levels) # график кодирования

    return encoded_signal, decoded_string # вовзрат кодированного и декодированного сигнала

nrzi_encode_decode() 

'''
1. строка на вход 
2. переводим в биты
3. кодируем 
4. переводим в сигнал 
5. на основе сигнала строим график
6. переводим сигнал в кодированные биты
7. декодируем в биты
8. переводим биты в строку
'''