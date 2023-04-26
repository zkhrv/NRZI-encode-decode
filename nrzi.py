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
    for bit in signal_levels: #  Переменная для хранения текущего уровня сигнала
        if bit == '1': # Если бит равен 1
            current_level = 1 - current_level # меняем состояние с 0 на 1 или с 1 на 0
            x.append(x[-1]) # оставляем координату x неизменной
            y.append(current_level) # задаем координату y текущего уровня
            x.append(x[-1]+1) # переходим на следующую координату x
            y.append(current_level) # продолжаем рисовать график на текущем уровне
        else: # иначе
            x.append(x[-1]+1) # переходим на следующую координату x
            y.append(current_level) # продолжаем рисовать график на текущем уровне

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
    encoded_signal = bits # инициализируем переменную encoded_signal пустой строкой, в нее будут добавляться закодированные биты
    current_level = 0 # переменная для хранения текущего уровня сигнала
    signal_levels = "" # пустая строка, в которую будем добавлять уровни сигнала
    for bit in encoded_signal: # перебор всех битов в строке 
        if bit == '1': # если значение равно 1
            current_level = 1 - current_level # меняем состояние на противоположное  
        signal_levels += str(current_level) # добавление текущее значение в переменную для уровней сигнала
    end_time = timeit.default_timer() # останавливаем таймер    
    time = end_time - start_time # считаем время, затраченное на кодировку    
    print("Кодированные биты: ", encoded_signal)
    print("Уровни сигнала:", signal_levels)
    print("Время кодирования:", "{:.8f}".format(time))
    # Декодирование
    start_time = timeit.default_timer() # запускаем таймер
    current_level = 0 # переменная для хранения текущего уровня сигнала
    decoded_signal_levels = '' # пустая строка, в которую будем добавлять биты 
    for level in signal_levels: # цикл по всем уровня сигнала
        if level == str(current_level): #  проверяем, равен ли текущий уровень сигнала current_level уровню в level
            decoded_signal_levels += '0' # сли да, то добавляем в строку bits значение 0
        else: # иначе
            decoded_signal_levels += '1' # если нет, то добавляем 1 и изменяем значение current_level на противоположное 
            current_level = 1 - current_level 
    decoded_bits = decoded_signal_levels # инициализируем переменную decoded_bits пустой строкой, в нее будут добавляться декодированные символы
    decoded_string = bits_to_string(decoded_bits) # Преобразуем декодированные биты в строку с помощью метода bits_to_string
    end_time = timeit.default_timer() # останавливаем таймер    
    time = end_time - start_time # считаем время, затраченное на кодировку 
    print("Декодированная строка: ", decoded_string)
    print("Время декодирования:", "{:.8f}".format(time))
    nrzi_signal(encoded_signal, signal_levels) # график кодирования
    return encoded_signal, decoded_string # вовзрат кодированного и декодированного сигнала

nrzi_encode_decode() 