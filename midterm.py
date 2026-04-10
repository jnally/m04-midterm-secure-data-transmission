import hashlib
from cryptography.fernet import Fernet
import os

# take string and generate SHA-256 hash
def make_text_hash(text):
    hash = hashlib.sha256() # initialize SHA-256 hash object
    hash.update(text.encode('utf-8')) # encode string to bytes and update hash object
    return hash.hexdigest() # return hexadecimal representation which is the recommended way to output

# open given file in binary mode, read block by block to generate SHA-256 hash
def make_file_hash(filepath, block_size=65536):
    hash = hashlib.sha256() # initialize SHA-256 hash object
    with open(filepath, 'rb') as f: # open file in binary mode
        # loop through file block by block and update hash until end of file
        for block in iter(lambda: f.read(block_size), b''):
            hash.update(block)
        return hash.hexdigest() # return hexadecimal representation

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

# encrypts input file to output file using the AES key
# I originally was just going to let it handle files that Fernet could work with in memory,
# but I found the following thread:
# https://stackoverflow.com/questions/69312922/how-to-encrypt-large-file-using-python
# encrypts blocks of the file and writes to another file since Fernet can't handle large files directly
def file_encrypt(fin, fout, key, block_size=65536):
    cipher = Fernet(key)
    with open(fin, 'rb') as f_in, open(fout, 'xb') as f_out: # open files in binary mode (won't overwrite existing file)
        # loop until we run out of file (using walrus operator to check truthiness and streamline loop)
        while raw_block := f_in.read(block_size):
            enc_block = cipher.encrypt(raw_block) # encrypt block of file with AES
            f_out.write(len(enc_block).to_bytes(4,'big')) # write length of block to output file
            f_out.write(enc_block) # write encrypted block to output file

# decrypts input file to output file using the AES key
# checks for 4 byte header at start of each block to determine block size to decrypt
def file_decrypt(fin, fout, key):
    cipher = Fernet(key)
    with open(fin, 'rb') as f_in, open(fout, 'xb') as f_out: # open files in binary mode (won't overwrite existing file)
        while size_b := f_in.read(4): # check 4 bytes to determine block size to decrypt, loop until end of file
            block_size = int.from_bytes(size_b, 'big') # convert size to int
            enc_block = f_in.read(block_size) # read block of encrypted data
            raw_block = cipher.decrypt(enc_block) # decrypt data
            f_out.write(raw_block) # write decrypted data to output file

# Get input file (must exist). This is for the file to be encrypted. 
def get_input_file(prompt='Enter file to be read from: '):
    while True:
        filename = input(prompt)
        if not filename: # pressing Enter key lets user escape back to main program loop
            filename = None
            break
        if os.path.isfile(filename): # make sure file does exists, so encryption can proceed
            break
        print('File', filename, 'does not exist. Try again.')
    return filename

# Get output file (must not exist). This is for files that are being written to (the encrypted and decrypted files).
def get_output_file(prompt='Enter file to be written to: '):
    while True: 
        filename = input(prompt)
        if not filename: # pressing Enter key lets user escape back to main program loop
            filename = None
            break
        if not os.path.exists(filename): # make sure file does not exists to protect data
            break
        print('File', filename, 'exists. Try again.')
    return filename

# present menu for SHA-256 hashing app
# option to hash text or hash a file using SHA-256 
def main():
    keep_going = True
    while keep_going: # present menu and loop until 1 or 2 is not selected
        print('\nModule 4 Midterm: Build a Secure Data Transmission App with Hashing and Encryption')
        print('Secure Data Transmission App Simulator (with SHA-256 Hashing and AES Encryption)')
        print('\nOptions:')
        print('1. Input text to transmit')
        print('2. Input file to transmit')
        print('3. Exit')
               
        choice = input('\nSelect an option (1, 2, or 3): ')  # get menu selection
        
        if choice == '1': # secure text transmission
            try:
                print('\nSecure Text Transmission')
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
                
                print('\nCheck if original text hash (', text_input_hash, ')')
                print('matches decrypted text hash (', decrypted_text_hash, ')...\n')
                if text_input_hash == decrypted_text_hash:
                    print('The hashes match! Message integrity verified.')
                else:
                    print('The hashes do not match. Message integrity not verified.')
            except FileNotFoundError:
                print('Error: File not found.')
            except Exception as e:
                print('Error:', e)
            
        elif choice == '2': # secure file transmission
            # Note: The file needs to be in the same directory as the script, 
            # or you must provide the absolute path.
            print('\nSecure File Transmission')
            print('(Press "Enter" key without any input to quit at anytime.)')
            try:
                raw_file_input = get_input_file('\nEnter the exact file name or path of file to be encrypted: ')
                if raw_file_input is None:
                    print('Exiting file transmission...')
                    continue
                
                raw_file_hash = make_file_hash(raw_file_input)
                print('\nOriginal File SHA-256 Hash:', raw_file_hash)

                key = generate_key()
                print('\nGenerated AES Shared Key (must be communicated secretly ahead of time):', key.decode('utf-8'))

                enc_file_input = get_output_file('\nEnter the exact file name or path for encrypted output file: ')
                if enc_file_input is None:
                    print('Exiting file transmission...')
                    continue
                
                print('The file', raw_file_input, 'will be encrypted. The output will be in', enc_file_input, '.')
                file_encrypt(raw_file_input, enc_file_input, key)

                enc_file_hash = make_file_hash(enc_file_input)
                print('\nEncrypted File SHA-256 Hash:', enc_file_hash)
                
                print('\nPretend encrypted file and original file hash was sent to someone with the shared key...')

                dec_file_input = get_output_file('\nEnter the exact file name or path for decrypted output file: ')
                if dec_file_input is None:
                    print('Exiting file transmission...')
                    continue

                print('The file', enc_file_input, 'will be decrypted. The output will be in', dec_file_input, '.')
                file_decrypt(enc_file_input, dec_file_input, key)

                dec_file_hash = make_file_hash(dec_file_input)
                print('\nDecrypted File SHA-256 Hash:', dec_file_hash)
                
                print('\nCheck if original file hash (', raw_file_hash, ')')
                print('matches decrypted file hash (', dec_file_hash, ')...\n')
                if raw_file_hash == dec_file_hash:
                    print('The hashes match! File integrity verified.')
                else:
                    print('The hashes do not match. File integrity not verified.')
            except FileNotFoundError:
                print('Error: File not found.')
            except FileExistsError:
                print('Error: File already exists.') 
            except Exception as e:
                print('Error:', e)

        # exits on 3 or anything else   
        else:
            print('Exiting application.')
            keep_going = False

# execute main function
if __name__ == '__main__':
    main()
