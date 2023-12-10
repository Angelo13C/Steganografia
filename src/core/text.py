ZERO_WIDTH_JOINER = "\u200D"
ZERO_WIDTH_NON_JOINER = "\u200C"

#Converti una stringa in una stringa di 0 e 1 corrispondente al codice utf8 di ogni carattere dell'originale
def stringToBinary(string):
    return ''.join(format(ord(i), '08b') for i in string)
#Converti una stringa di 0 e 1 in una stringa di ZERO_WIDTH_NON_JOINER e ZERO_WIDTH_JOINER (che sono invisibili)
def binaryToHidden(binary):
    return binary.replace("0", ZERO_WIDTH_NON_JOINER).replace("1", ZERO_WIDTH_JOINER)

#Converti una stringa di ZERO_WIDTH_NON_JOINER e ZERO_WIDTH_JOINER (che sono invisibili) in una stringa di 0 e 1 
def hiddenToBinary(hidden):
    return ''.join([c for c in hidden if c in set(ZERO_WIDTH_JOINER + ZERO_WIDTH_NON_JOINER)]).replace(ZERO_WIDTH_JOINER, "1").replace(ZERO_WIDTH_NON_JOINER, "0")
#Converti una stringa di 0 e 1 nella stringa corrispondente al codice utf8 della stringa binaria
def binaryToString(binary):
    return ''.join(chr(int(binary[i*8:i*8+8],2)) for i in range(len(binary)//8))