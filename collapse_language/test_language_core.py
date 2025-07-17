from collapse_vm_parser import parse_CSL_text
from phoneme_map import get_phoneme_info
from binary_encoder import encode_csl_to_binary, decode_binary_to_csl

# Input: Collapse Symbolic Language (CSL) text
input_text = "ABCXYZ"

print("\n🧠 CSL Node Parse")
parsed_nodes = parse_CSL_text(input_text)
for node in parsed_nodes:
    print(f"• {node}")

print("\n🔊 Phoneme + Frequency Map")
for char in input_text:
    phoneme, freq = get_phoneme_info(char)
    print(f"• {char} → {phoneme} @ {freq} Hz")

print("\n💾 Binary Encoding")
binary = encode_csl_to_binary(input_text)
print(f"• Encoded: {binary}")
print(f"• Decoded: {decode_binary_to_csl(binary)}")
