def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result

def decrypt(text, shift):
    return caesar_cipher(text, -shift)

# Test
if __name__ == "__main__":
    message = "HELLO WORLD"
    shift = 3
    encrypted = caesar_cipher(message, shift)
    decrypted = decrypt(encrypted, shift)
    
    print(f"Original: {message}")
    print(f"Encrypted (shift {shift}): {encrypted}")
    print(f"Decrypted: {decrypted}")
