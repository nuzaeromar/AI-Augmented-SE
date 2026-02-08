class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        ciphertext = []
        for ch in plaintext:
            if ch.isalpha():
                ascii_offset = 65 if ch.isupper() else 97
<<<<<<< Updated upstream
                shifted_char = chr((ch.lower() - 'a' + shift) % 26 + ascii_offset)
                ciphertext.append(shifted_char)
=======
                # work with lowercase for calculation, then reapply original case offset
                shifted = (ord(ch.lower()) - ord('a') + shift) % 26
                ciphertext.append(chr(shifted + ascii_offset))
>>>>>>> Stashed changes
            else:
                ciphertext.append(ch)
        return ''.join(ciphertext)

<<<<<<< Updated upstream
    def vigenere_cipher(self, plain_text):
        encrypted_text = []
        key_index = 0
        for ch in plain_text:
            if ch.isalpha():
                shift = self.key[key_index % len(self.key)].lower() - 'a'
                encrypted_char = chr((ch.lower() - 'a' + shift) % 26 + ord('a'))
                encrypted_text.append(encrypted_char.upper() if ch.isupper() else encrypted_char)
=======
    def vigenere_cipher(self, plain_text: str) -> str:
        encrypted_text = []
        key_len = len(self.key)
        if key_len == 0:
            return plain_text  # No key, return unchanged
        key_index = 0
        for ch in plain_text:
            if ch.isalpha():
                shift = ord(self.key[key_index % key_len].lower()) - ord('a')
                base_char = (ord(ch.lower()) - ord('a') + shift) % 26
                encrypted_char = chr(base_char + ord('a'))
                if ch.isupper():
                    encrypted_char = encrypted_char.upper()
                encrypted_text.append(encrypted_char)
>>>>>>> Stashed changes
                key_index += 1
            else:
                encrypted_text.append(ch)
        return ''.join(encrypted_text)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 0:
            raise ValueError("Rails must be greater than zero.")
<<<<<<< Updated upstream
        fence = [[] for _ in range(rails)]
=======
        # Initialize fence rows
        fence = ['' for _ in range(rails)]
>>>>>>> Stashed changes
        direction = -1
        row = 0

        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction

            fence[row].append(ch)
            row += direction

        encrypted_text = []
        for i in range(rails):
            encrypted_text.extend(fence[i])

        return ''.join(encrypted_text)
