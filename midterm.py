import hashlib

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
        print('\nModule 3: Assignment - Secure Hashing and Encryption')
        print('SHA-256 Hashing App')
        print('\nOptions:')
        print('1. Hash a text string')
        print('2. Hash a file')
        print('3. Exit')
        
        # get menu selection
        choice = input('\nSelect an option (1, 2, or 3): ')
        
        # hash text
        if choice == '1':
            text_input = input('\nEnter the text to hash: ')
            print('\nSHA-256 Hash:', make_text_hash(text_input),'\n')
            
        # hash file
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
