import cv2
import numpy as np

# ---------- INPUT ----------
cover_path = "cover.png"
secret_path = "secret.png"

# ---------- LOAD IMAGES ----------
cover_img = cv2.imread(cover_path, cv2.IMREAD_GRAYSCALE)
secret_img = cv2.imread(secret_path, cv2.IMREAD_GRAYSCALE)

if cover_img is None or secret_img is None:
    raise ValueError("Error loading images")

if cover_img.shape != secret_img.shape:
    raise ValueError("Cover and Secret images must be same size")

# ---------- SENDER SIDE ----------
cover = cover_img.astype(np.int16)
secret = secret_img.astype(np.int16)

# Generate stego-key (Zero-Steganography)
stego_key = secret - cover
np.save("stego_key.npy", stego_key)

print("MVP: Stego-key generated")
print("Cover image remains unchanged")

# ---------- RECEIVER SIDE ----------
loaded_key = np.load("stego_key.npy")
recovered_secret = cover + loaded_key

# Normalize pixel values
recovered_secret = np.clip(recovered_secret, 0, 255).astype(np.uint8)

cv2.imwrite("recovered_secret.png", recovered_secret)

print("MVP: Secret image successfully recovered")