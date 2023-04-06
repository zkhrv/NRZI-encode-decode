import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 
import timeit 

def string_to_bits(s):
    bits = []
    for char in s.encode('cp1251'):
        bits.extend([bin(char)[2:].zfill(8)])
    return ''.join(bits)

def bits_to_string(b):
    chars = []
    for i in range(0, len(b), 8):
        chars.append(int(b[i:i+8], 2))
    return bytes(chars).decode('cp1251')

def plot_encoded_signal(encoded_signal):
    x = [0]  # начинаем отрисовку с нулевой точки
    y = [0]  # начинаем отрисовку с нулевой точки

    current_level = 0
    for bit in encoded_signal:
        if bit == '1':
            current_level = 1 - current_level  # меняем состояние с 0 на 1 или с 1 на 0
        x.append(x[-1])  # оставляем координату x неизменной
        y.append(current_level)  # задаем координату y текущего уровня
        x.append(x[-1]+1)  # переходим на следующую координату x
        y.append(current_level)  # продолжаем рисовать график на текущем уровне

    plt.plot(x, y, color='red', linewidth=3)
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(1))
    plt.grid(which='both', color='k', linewidth=1)
    plt.title('NRZI Encoding')
    plt.xlabel('Bit')
    plt.ylabel('Signal level')
    plt.suptitle(encoded_signal)
    plt.show()

def nrzi_encode_decode():
    input_string = input("Введите строку для кодирования: ")
    # Кодирование
    start_time = timeit.default_timer()
    end_time = timeit.default_timer()
    time = end_time - start_time
    bits = string_to_bits(input_string)
    signal = '1'
    encoded_signal = ''
    for bit in bits:
        if bit == '0':
            encoded_signal += signal
        else:
            signal = '0' if signal == '1' else '1'
            encoded_signal += signal
    print("Кодированный сигнал: ", encoded_signal)
    print("Время кодирования:", "{:.8f}".format(time))

    # Декодирование
    decoded_bits = ''
    signal = '1'
    for i in range(0, len(encoded_signal)):
        if encoded_signal[i] == signal:
            decoded_bits += '0'
        else:
            decoded_bits += '1'
            signal = encoded_signal[i]
    decoded_string = bits_to_string(decoded_bits)
    print("Декодированная строка: ", decoded_string)

    # График кодирования
    plot_encoded_signal(encoded_signal)

    return encoded_signal, decoded_string

nrzi_encode_decode()