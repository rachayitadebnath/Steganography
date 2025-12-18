import cv2
import numpy as np
import os

def load_image(image_path, grayscale=False):
    """Load an image from file path."""
    if grayscale:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError(f"Error loading image: {image_path}")
    
    return img

def resize_to_match(secret_img, cover_img):
    """Resize secret image to match cover image dimensions."""
    return cv2.resize(secret_img, (cover_img.shape[1], cover_img.shape[0]))

def generate_stego_key(cover_img, secret_img):
    """
    Generate stego-key using zero-steganography.
    The cover image remains completely unchanged.
    """
    cover = cover_img.astype(np.int16)
    secret = secret_img.astype(np.int16)
    
    stego_key = secret - cover
    return stego_key

def save_stego_key(stego_key, output_path):
    """Save the stego-key to a .npy file."""
    np.save(output_path, stego_key)

def load_stego_key(key_path):
    """Load a stego-key from a .npy file."""
    return np.load(key_path)

def recover_secret_image(cover_img, stego_key):
    """
    Recover the secret image using the cover image and stego-key.
    """
    cover = cover_img.astype(np.int16)
    recovered = cover + stego_key
    
    recovered = np.clip(recovered, 0, 255).astype(np.uint8)
    return recovered

def save_image(image, output_path):
    """Save an image to file."""
    cv2.imwrite(output_path, image)

def calculate_psnr(original, recovered):
    """Calculate Peak Signal-to-Noise Ratio between two images."""
    mse = np.mean((original.astype(np.float64) - recovered.astype(np.float64)) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def process_sender(cover_path, secret_path, key_output_path):
    """
    Sender-side processing:
    1. Load cover and secret images
    2. Generate stego-key
    3. Save stego-key
    Returns: cover image shape for reference
    """
    cover_img = load_image(cover_path)
    secret_img = load_image(secret_path)
    
    if cover_img.shape != secret_img.shape:
        secret_img = resize_to_match(secret_img, cover_img)
    
    stego_key = generate_stego_key(cover_img, secret_img)
    save_stego_key(stego_key, key_output_path)
    
    return cover_img.shape

def process_receiver(cover_path, key_path, output_path):
    """
    Receiver-side processing:
    1. Load cover image and stego-key
    2. Recover secret image
    3. Save recovered image
    Returns: recovered image
    """
    cover_img = load_image(cover_path)
    stego_key = load_stego_key(key_path)
    
    recovered = recover_secret_image(cover_img, stego_key)
    save_image(recovered, output_path)
    
    return recovered