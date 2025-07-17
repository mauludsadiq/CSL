# binary_map.py

# Simple 6-bit encoding for 64 symbols
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
binary_lookup = {char: format(i, '06b') for i, char in enumerate(alphabet)}
inverse_lookup = {v: k for k, v in binary_lookup.items()}

def encode_to_binary(text):
    return ' '.join(binary_lookup.get(char, '000000') for char in text)

def decode_from_binary(binary_string):
    bits = binary_string.strip().split()
    return ''.join(inverse_lookup.get(b, '?') for b in bits)
