def hexToDecimal(hexadecimal_string):
    dictionary_hexa_to_decimal =  {'0': 0, '1' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, 'A' : 10 , 'B' : 11, 'C' : 12, 'D' : 13, 'E' : 14, 'F' : 15}  
    decimal = 0  
  
    length = len(hexadecimal_string) -1  
    
    for digit in hexadecimal_string:  
        decimal += dictionary_hexa_to_decimal[digit]*16**length  
        length -= 1 
    
    return decimal


if __name__ == "__main__":
    print(hexToDecimal("0186A0"))
