import hashlib
from cryptography.fernet import Fernet

# take string and generate SHA-256 hash
def make_text_hash(text):
    # initialize SHA-256 hash object
    hash = hashlib.sha256()

    # encode string to bytes and update hash object
    hash.update(text.encode('utf-8'))

    # return hexadecimal representation which is the recommended way to output
    return hash.hexdigest()

# open given file in binary mode, read block by block to generate SHA-256 hash
def make_file_hash(filepath, block_size=65536):
    # initialize SHA-256 hash object
    hash = hashlib.sha256()

    try:
        # open file in binary mode
        with open(filepath, 'rb') as f:
            # loop through file block by block and update hash until end of file
            for block in iter(lambda: f.read(block_size), b''):
                hash.update(block)
            # return hexadecimal representation
            return hash.hexdigest()
    except FileNotFoundError:
        return 'Error: File not found.'
    except Exception as e:
        return 'Error: ' + e
    
# generate AES key using fernet from cryptography
def generate_key():
    return Fernet.generate_key()
    
# AES encryption using fernet from cryptography
def text_encrypt(text, key):
    cipher = Fernet(key)
    return cipher.encrypt(text.encode('utf-8'))

# AES decryption using fernet from cryptography
def text_decrypt(text, key):
    cipher = Fernet(key)
    return cipher.decrypt(text.encode('utf-8'))

# TODO make AES file encryption happen
def file_encrypt():
    return

# TODO make AES file decryption happen
def file_decrypt():
    return

# present menu for SHA-256 hashing app
# option to hash text or hash a file using SHA-256 
def main():
    keep_going = True
    choice = ''
    text_input = ''
    file_input = ''

    # loop until 1 or 2 is not selected
    while keep_going:
        # menu
        print('\nModule 4 Midterm: Build a Secure Data Transmission App with Hashing and Encryption')
        print('Secure Data Transmission App Simulator (with SHA-256 Hashing and AES Encryption)')
        print('\nOptions:')
        print('1. Input text to transmit')
        print('2. Input file to transmit')
        print('3. Exit')
        
        # get menu selection
        choice = input('\nSelect an option (1, 2, or 3): ')
        
        # secure text transmission
        if choice == '1':
            text_input = input('\nEnter the text to transmit: ')

            text_input_hash = make_text_hash(text_input)
            print('\nOriginal Text SHA-256 Hash:', text_input_hash)
            
            key = generate_key()
            print('\nGenerated AES Shared Key (must be communicated secretly ahead of time):', key.decode('utf-8'))
            
            ciphertext = text_encrypt(text_input, key).decode('utf-8')
            print('\nEncrypted Text:', ciphertext)
            
            print('\nPretend encrypted message and hash was sent to someone with the shared key...')
            
            decrypted_text = text_decrypt(ciphertext, key).decode('utf-8')
            print('\nDecrypted Text:', decrypted_text)

            decrypted_text_hash = make_text_hash(decrypted_text)
            print('\nDecrypted Text SHA-256 Hash:', decrypted_text_hash)
            
            print('Check if original text hash (', text_input_hash, ') matches decrypted text hash (', decrypted_text_hash, ')...\n')
            if text_input_hash == decrypted_text_hash:
                print('The hashes match! Message integrity verified.')
            else:
                print('The hashes do not match. Message integrity not verified.')
            
        # secure file transmission
        elif choice == '2':
            # Note: The file needs to be in the same directory as the script, 
            # or you must provide the absolute path.
            file_input = input('\nEnter the exact file name or path : ')
            print('\nSHA-256 Hash:', make_file_hash(file_input))

        # exits on 3 or anything else   
        else:
            print('Exiting application.')
            keep_going = False


# execute main function
if __name__ == '__main__':
    main()
