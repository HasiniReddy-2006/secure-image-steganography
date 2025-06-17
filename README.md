# secure-image-steganography
Steganographic Encryption: Enhancing Digital Image Privacy

# 🔐 Secure Image Steganography

A Python-based project that combines **cryptography** and **image steganography** to securely hide encrypted messages inside digital images.

## 📌 Project Overview

This project provides a dual-layer security approach:
- **Encryption:** Uses Fernet (AES-based symmetric encryption) to encrypt the message.
- **Steganography:** Embeds the encrypted message into an image using Least Significant Bit (LSB) manipulation.

The result is a stego-image that looks unchanged but secretly carries a hidden message retrievable only with the correct key.

---

## 🚀 Features

- Symmetric key encryption using `cryptography` library (Fernet).
- Image processing using `Pillow (PIL)`.
- Embed and extract messages from `.png` or `.jpg` images.
- Easy-to-use command-line interface.

---

## 🛠️ Requirements

- Python 3.6+
- Required libraries:
  ```bash
  pip install cryptography pillow
