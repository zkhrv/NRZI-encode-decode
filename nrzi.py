import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 

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
    x = [] 
    y = [] 
    current_level = 0 
    for bit in encoded_signal: 
        if bit == '1': 
            current_level = 1 - current_level 
        x.append(len(x)) 
        y.append(current_level) 
    plt.plot(x, y, color='red', linewidth = 3)
    plt.xlabel(ticker.MultipleLocator(1)) #
    plt.grid(which='major', 
             color = 'k',
             linewidth = 2) 
    plt.minorticks_on() 
    plt.grid(which='minor', 
        color = 'gray', 
        linestyle = '-',
        linewidth = 1) 
    plt.title('NRZI Encoding') 
    plt.xlabel('Bit') 
    plt.ylabel('Signal level') 
    plt.show() 

def nrzi_encode_decode():
    input_string = input("Введите строку для кодирования: ")
    # Кодирование
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