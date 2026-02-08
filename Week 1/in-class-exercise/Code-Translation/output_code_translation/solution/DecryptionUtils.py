class DecryptionUtils:
    def __init__(self, key):
        self.key_ = key

    def caesar_decipher(self, ciphertext, shift):
<<<<<<< Updated upstream
        shift = shift % 26
        plaintext = []
        for c in ciphertext:
            if c.isalpha():
                base = 'A' if c.isupper() else 'a'
                shifted_char = chr((ord(c) - ord(base) - shift + 26) % 26 + ord(base))
                plaintext.append(shifted_char)
=======
        shift %= 26
        result = []
        for c in ciphertext:
            if c.isalpha():
                base = 'A' if c.isupper() else 'a'
                shifted = (ord(c) - ord(base) - shift) % 26 + ord(base)
                result.append(chr(shifted))
>>>>>>> Stashed changes
            else:
                result.append(c)
        return ''.join(result)

    def vigenere_decipher(self, ciphertext):
<<<<<<< Updated upstream
        decrypted_text = []
        key_length = len(self.key_)
        key_index = 0

        for c in ciphertext:
            if c.isalpha():
                shift = ord(self.key_[key_index % key_length].lower()) - ord('a')
                base = 'a' if c.islower() else 'A'
                decrypted_char = chr((ord(c.lower()) - ord('a') - shift + 26) % 26 + ord('a'))
                decrypted_text.append(decrypted_char.upper() if c.isupper() else decrypted_char)
=======
        decrypted = []
        key_len = len(self.key_)
        if key_len == 0:
            return ciphertext
        key_index = 0
        for c in ciphertext:
            if c.isalpha():
                shift = ord(self.key_[key_index % key_len].lower()) - ord('a')
                base_ord = ord('a')
                # work in lower case then restore case
                plain_ord = (ord(c.lower()) - base_ord - shift) % 26 + base_ord
                plain_char = chr(plain_ord)
                if c.isupper():
                    plain_char = plain_char.upper()
                decrypted.append(plain_char)
>>>>>>> Stashed changes
                key_index += 1
            else:
                decrypted_text.append(c)
        return ''.join(decrypted_text)

    def rail_fence_decipher(self, encrypted_text, rails):
<<<<<<< Updated upstream
        plain_text = []
        n = len(encrypted_text)
        if rails <= 1:
            return encrypted_text

=======
        if rails <= 1:
            return encrypted_text
        n = len(encrypted_text)
        # create placeholder fence
>>>>>>> Stashed changes
        fence = [['\n' for _ in range(n)] for _ in range(rails)]

        direction = -1
        row = 0
        col = 0
<<<<<<< Updated upstream

=======
        # mark the zig‑zag pattern positions
>>>>>>> Stashed changes
        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row][col] = '*'
            col += 1
            row += direction

<<<<<<< Updated upstream
        index = 0
=======
        # fill the marked positions with characters from the encrypted text
        idx = 0
>>>>>>> Stashed changes
        for r in range(rails):
            for c in range(n):
                if fence[r][c] == '*':
                    fence[r][c] = encrypted_text[index]
                    index += 1

<<<<<<< Updated upstream
        direction = -1
        row = 0
        col = 0

=======
        # read the fence in zig‑zag order to obtain the plaintext
        result = []
        direction = -1
        row = 0
        col = 0
>>>>>>> Stashed changes
        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction = -direction
            result.append(fence[row][col])
            col += 1
            row += direction

        return ''.join(result)
