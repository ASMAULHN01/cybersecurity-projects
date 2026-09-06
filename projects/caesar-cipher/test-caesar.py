from caesar_cipher import caesar_cipher, decrypt

message = "HELLO WORLD"
shift = 3

encrypted = caesar_cipher(message, shift)
decrypted = decrypt(encrypted, shift)

print(f"Original: {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
