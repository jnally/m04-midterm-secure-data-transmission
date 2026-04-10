# Module 4 Midterm: Build a Secure Data Transmission App with Hashing and Encryption
**Author:** Jeremy Nally  
**Course:** SDEV245 - Security and Secure Coding  

## Overview
This is a Secure Data Transmission Simulator App designed to demonstrate the implementation of cryptographic standards. It allows for the secure transmission of both plain text and files of any size by utilizing SHA-256 hashing for verifying integrity and AES-128 symmetric encryption for confidentiality.

## The CIA Triad
This solution is built upon the three core pillars of information security:

### Confidentiality
Confidentiality protects data from unauthorized disclosure. 
* **Implementation:** This app uses AES-128 symmetric encryption via the `cryptography.fernet` library in Python. 
* **Role:** By transforming plaintext into an encrypted format (ciphertext), the data remains unreadable to anyone without the shared secret key in order to ensure private communication across potentially insecure channels.

### Integrity
Integrity ensures that data remains accurate and has not been altered or tampered with during transmission.
* **Implementation:** I implemented SHA-256 hashing. 
* **Role:** Before transmission, a hash is generated (it acts like a digital fingerprint). After decryption, the hash is recalculated. Any mismatch between the original and final hash immediately alerts the user that the data's integrity has been compromised.

### Availability
Availability ensures that authorized users have reliable access to the data and system resources.
* **Implementation:** The app utilizes streaming files in pieces in order to manage any file size.
* **Role:** Instead of loading an entire file into memory (RAM), which could cause the program to crash when handling large files, the app processes data in 64KB blocks. This prevents overwhelming system memory and ensures the tool works regardless of file size. The only hardware limitation would be disk space for output files.

## Entropy and Key Generation
The strength of the security model depends entirely on the quality of the encryption keys.

### The Role of Entropy
Entropy is the measure of randomness or unpredictability in a system. In cryptography, high entropy is very important. If a key is predictable (has low entropy), it can be easily cracked via brute-force or dictionary attacks by threat actors.

### Key Generation Process
Keys in this application are generated using `Fernet.generate_key()`.
* **CSPRNG:** This process relies on the operating system’s Cryptographically Secure Pseudorandom Number Generator (CSPRNG). 
* **Security:** The operating system collects entropy from non-deterministic hardware sources (like thermal noise or microscopic disk-timing variations). This results in a 128-bit key that is statistically indistinguishable from true randomness. This makes it impossible for a threat actor to predict or replicate.

## Technical Implementation Details
* **Length-Prefixed Framing:** Because Fernet adds metadata to every block, encrypted chunks vary in size. To handle this in a stream, I implemented a 4-byte Big-Endian length header before every chunk to tell the decryption logic exactly how many bytes to pull next.
* **Secure File Handling:** All file writing operations use exclusive creation mode (`xb`) to prevent accidentally overwriting existing files.
* **User Experience:** The app features input validation that allows the user to cancel out of file name input and return to the main menu at any time by pressing Enter without input.
