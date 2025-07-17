from semantic_translator import translate_collapse
from collapse_audio.emitter import emit_waveform
from encoder.binary_map import encode_to_binary
from validator.cgs_validator import validate_cgs

# Prompt user
user_input = input("CSL >> ").strip()

# ✅ Validate CSL syntax
if not validate_cgs(user_input):
    print("❌ Invalid CSL input.")
    exit()

# ✅ Translate semantics + binary
semantic = translate_collapse(user_input)
binary = encode_to_binary(user_input)

# ✅ Output
print("\n🧠 Semantic Collapse:")
print(semantic)

print("\n💾 Binary Encoding:")
print(binary)

# ✅ Safe audio length check
if len(user_input) > 120:
    print("\n⚠️ Skipping audio: input too long for stable waveform.")
else:
    print("\n🔊 Audio Emission:")
    emit_waveform(user_input)
