# binary_encoder.py

CSL_TO_BINARY = {chr(ord('A') + i): format(i, '06b') for i in range(26)}
BINARY_TO_CSL = {v: k for k, v in CSL_TO_BINARY.items()}

def encode_csl_to_binary(text):
    return ' '.join(CSL_TO_BINARY[c] for c in text if c in CSL_TO_BINARY)

def decode_binary_to_csl(bits):
    return ''.join(BINARY_TO_CSL.get(b, '?') for b in bits.split())
