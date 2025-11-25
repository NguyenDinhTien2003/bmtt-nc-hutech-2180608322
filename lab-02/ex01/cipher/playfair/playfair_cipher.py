class PlayfairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace('J', 'I')
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # J is omitted
        matrix = [key_letter for key_letter in key if key_letter not in 'J']

        for letter in alphabet:
            if letter not in key_set and letter != 'J':
                matrix.append(letter)

        playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return -1, -1 # Should not happenclass PlayfairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace('J', 'I')
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # J is omitted
        matrix = [key_letter for key_letter in key if key_letter not in 'J']

        for letter in alphabet:
            if letter not in key_set and letter != 'J':
                matrix.append(letter)

        playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return -1, -1 # Should not happen
    def playfair_encrypt(self, plain_text, playfair_matrix):
        # 1. Clean and prepare text
        plain_text = plain_text.upper().replace('J', 'I')
        
        # 2. Split into pairs, adding 'X' for duplicates or odd length
        i = 0
        digrams = []
        while i < len(plain_text):
            char1 = plain_text[i]
            if i + 1 == len(plain_text) or char1 == plain_text[i+1]:
                char2 = 'X'
                i -= 1 # Stay on current char next iteration
            else:
                char2 = plain_text[i+1]
            
            digrams.append((char1, char2))
            i += 2 # Move to the next pair

        encrypted_text = ""
        for char1, char2 in digrams:
            row1, col1 = self.find_letter_coords(playfair_matrix, char1)
            row2, col2 = self.find_letter_coords(playfair_matrix, char2)

            if row1 == row2: # Same row
                encrypted_text += playfair_matrix[row1][(col1 + 1) % 5]
                encrypted_text += playfair_matrix[row2][(col2 + 1) % 5]
            elif col1 == col2: # Same column
                encrypted_text += playfair_matrix[(row1 + 1) % 5][col1]
                encrypted_text += playfair_matrix[(row2 + 1) % 5][col2]
            else: # Rectangle
                encrypted_text += playfair_matrix[row1][col2]
                encrypted_text += playfair_matrix[row2][col1]
        
        return encrypted_text
    def playfair_decrypt(self, cipher_text, playfair_matrix):
        cipher_text = cipher_text.upper().replace('J', 'I')
        
        decrypted_text = ""
        for i in range(0, len(cipher_text), 2):
            char1 = cipher_text[i]
            char2 = cipher_text[i+1]
            
            row1, col1 = self.find_letter_coords(playfair_matrix, char1)
            row2, col2 = self.find_letter_coords(playfair_matrix, char2)

            if row1 == row2: # Same row
                decrypted_text += playfair_matrix[row1][(col1 - 1) % 5]
                decrypted_text += playfair_matrix[row2][(col2 - 1) % 5]
            elif col1 == col2: # Same column
                decrypted_text += playfair_matrix[(row1 - 1) % 5][col1]
                decrypted_text += playfair_matrix[(row2 - 1) % 5][col2]
            else: # Rectangle
                decrypted_text += playfair_matrix[row1][col2]
                decrypted_text += playfair_matrix[row2][col1]

        # Final cleanup (removing X's inserted for pairing is complex and often skipped in basic labs)
        return decrypted_text