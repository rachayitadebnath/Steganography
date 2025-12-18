# Steganography- Zero-Steganography Image Hiding System

A secure and innovative web-based steganography system that transfers secret images **without modifying the cover image**, making it completely undetectable by traditional steganalysis methods.

## 🌟 What is Zero-Steganography?

Traditional steganography embeds secret data into a cover image by modifying its pixels, which can be detected by steganalysis tools. **Zero-steganography** takes a completely different approach:

- ✅ **Cover image remains 100% unchanged** (no pixel modifications)
- ✅ **Generates a mathematical key** (stego-key) instead of embedding data
- ✅ **Undetectable by steganalysis** since the cover image is pristine
- ✅ **Perfect recovery** of the secret image using the key

### How It Works

```
Sender Side:
Secret Image - Cover Image = Stego-Key
(Store this key separately)

Receiver Side:
Cover Image + Stego-Key = Secret Image
(Perfect reconstruction)
```

## 🎨 Features

- 🖼️ **Dual Mode Interface**: Separate sender and receiver modes
- 🌓 **Dark/Light Theme Toggle**: Switch between dark and light modes with persistent preference
- 📤 **File Upload**: Support for PNG, JPG, JPEG, BMP, and TIFF formats
- 🔒 **Secure Processing**: Session-based file handling with unique IDs
- 💾 **Easy Download**: Download stego-keys and recovered images
- 📱 **Responsive Design**: Works on all screen sizes
- 🎨 **Modern UI**: Beautiful black and orange color scheme

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/Steganography
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python app.py
```

The application will start at `http://127.0.0.1:5001`

Open your web browser and navigate to the URL above.

## 📖 Usage Guide

### Sender Mode (Hiding a Secret Image)

1. Click on **"Sender Mode"** from the home page
2. Upload a **cover image** (the image that will remain unchanged)
3. Upload a **secret image** (the image you want to hide)
4. Click **"Generate Stego-Key"**
5. Download the generated stego-key file (`.npy` format)
6. Share the **original cover image** and the **stego-key** with the receiver

**Important**: Keep the cover image exactly as it is! Any modification will break the recovery process.

### Receiver Mode (Recovering the Secret Image)

1. Click on **"Receiver Mode"** from the home page
2. Upload the **original cover image** (must be identical to the sender's cover)
3. Upload the **stego-key file** (`.npy` file received from sender)
4. Click **"Recover Secret Image"**
5. View and download the recovered secret image

## 🗂️ Project Structure

```
Steganography/
├── app.py                  # Flask web application (main server)
├── zero_stego.py          # Zero-steganography algorithm implementation
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── index.html        # Home page
│   ├── sender.html       # Sender mode page
│   └── receiver.html     # Receiver mode page
├── static/               # Generated at runtime
│   ├── uploads/          # Uploaded images
│   ├── keys/             # Generated stego-keys
│   └── recovered/        # Recovered secret images
└── README.md             # This file
```

## 📝 Code Explanation (Beginner-Friendly)

### Part 1: `zero_stego.py` - The Brain of the Operation

This file contains all the mathematical magic that makes zero-steganography work.

#### Importing Libraries

```python
import cv2          # OpenCV - for reading/writing images
import numpy as np  # NumPy - for mathematical operations on images
import os          # OS - for file system operations
```

**What do these do?**
- `cv2`: Helps us load and save images
- `numpy`: Treats images as arrays of numbers so we can do math on them
- `os`: Helps us work with files and folders

---

#### Function 1: `load_image()`

```python
def load_image(image_path, grayscale=True):
    """Load an image from file path."""
    if grayscale:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError(f"Error loading image: {image_path}")
    
    return img
```

**What it does:**
- Loads an image from your computer
- `grayscale=True`: Converts the image to black & white (simpler to work with)
- `cv2.imread()`: OpenCV function that reads the image file
- Returns the image as a grid of numbers (each number is a pixel's brightness)

**Why grayscale?**
- Simpler math (one number per pixel instead of three for RGB)
- Faster processing
- Still demonstrates the concept perfectly

---

#### Function 2: `resize_to_match()`

```python
def resize_to_match(secret_img, cover_img):
    """Resize secret image to match cover image dimensions."""
    return cv2.resize(secret_img, (cover_img.shape[1], cover_img.shape[0]))
```

**What it does:**
- Makes sure both images are the same size
- `shape[0]`: Height of the image
- `shape[1]`: Width of the image
- `cv2.resize()`: Stretches or shrinks the secret image to match the cover

**Why is this needed?**
We can only do math (addition/subtraction) on images of the same size!

---

#### Function 3: `generate_stego_key()` ⭐ **MOST IMPORTANT**

```python
def generate_stego_key(cover_img, secret_img):
    """
    Generate stego-key using zero-steganography.
    The cover image remains completely unchanged.
    """
    cover = cover_img.astype(np.int16)
    secret = secret_img.astype(np.int16)
    
    stego_key = secret - cover
    return stego_key
```

**What it does - The Magic Formula:**
```
Stego-Key = Secret Image - Cover Image
```

**Step by step:**
1. `astype(np.int16)`: Convert images to a number type that can be negative
   - Normal images use 0-255 (can't be negative)
   - We need negative numbers because `secret - cover` might be negative
   
2. `stego_key = secret - cover`: Subtract cover from secret
   - If secret pixel = 150 and cover pixel = 100, key = 50
   - If secret pixel = 80 and cover pixel = 120, key = -40

3. Return this key (contains the "difference" between the two images)

**Example:**
```
Secret pixel: 200
Cover pixel:  150
Key:          50    (200 - 150 = 50)

Later, to recover:
Cover pixel:  150
Key:          50
Recovered:    200   (150 + 50 = 200) ✓
```

---

#### Function 4: `save_stego_key()`

```python
def save_stego_key(stego_key, output_path):
    """Save the stego-key to a .npy file."""
    np.save(output_path, stego_key)
```

**What it does:**
- Saves the stego-key as a `.npy` file
- `.npy`: NumPy's special format for saving arrays
- Preserves all the negative numbers and exact values

---

#### Function 5: `load_stego_key()`

```python
def load_stego_key(key_path):
    """Load a stego-key from a .npy file."""
    return np.load(key_path)
```

**What it does:**
- Loads the stego-key from a `.npy` file
- Returns the key as an array of numbers

---

#### Function 6: `recover_secret_image()` ⭐ **RECOVERY MAGIC**

```python
def recover_secret_image(cover_img, stego_key):
    """
    Recover the secret image using the cover image and stego-key.
    """
    cover = cover_img.astype(np.int16)
    recovered = cover + stego_key
    
    recovered = np.clip(recovered, 0, 255).astype(np.uint8)
    return recovered
```

**What it does - The Recovery Formula:**
```
Secret Image = Cover Image + Stego-Key
```

**Step by step:**
1. Convert cover to `int16` (to handle addition safely)
2. `recovered = cover + stego_key`: Add the key back to the cover
3. `np.clip(recovered, 0, 255)`: Make sure all values are between 0 and 255
   - Sometimes math can give us 256 or -1, which aren't valid pixels
   - `clip` forces them into the valid range
4. `astype(np.uint8)`: Convert back to normal image format (0-255)

**Example:**
```
Cover pixel:  150
Key:          50
Recovered:    200   (150 + 50 = 200)
This matches the original secret pixel! ✓
```

---

#### Functions 7-8: Helper Functions

```python
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
```

**`save_image()`**: Writes the image to disk
**`calculate_psnr()`**: Measures quality (higher = better reconstruction)

---

#### Functions 9-10: Main Processing Functions

```python
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
```

**What it does (Sender's workflow):**
1. Load both images
2. Resize secret if needed
3. Generate the stego-key (secret - cover)
4. Save the key
5. Return image dimensions

```python
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
```

**What it does (Receiver's workflow):**
1. Load cover image
2. Load stego-key
3. Recover secret (cover + key)
4. Save recovered image
5. Return the image

---

### Part 2: `app.py` - The Web Server

This file creates the website that users interact with.

#### Importing Libraries

```python
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import uuid
from zero_stego import process_sender, process_receiver, load_image, calculate_psnr
```

**What these do:**
- `Flask`: Creates the web server
- `render_template`: Shows HTML pages to users
- `request`: Gets data from users (like uploaded files)
- `send_file`: Lets users download files
- `os`: File system operations
- `uuid`: Generates unique IDs for each session
- Our functions from `zero_stego.py`

---

#### Setting Up the Server

```python
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
```

**What it does:**
- `Flask(__name__)`: Creates a new web application
- `MAX_CONTENT_LENGTH`: Limits uploads to 16MB (16 × 1024 × 1024 bytes)

---

#### Creating Folders

```python
UPLOAD_FOLDER = 'static/uploads'
KEYS_FOLDER = 'static/keys'
RECOVERED_FOLDER = 'static/recovered'

for folder in [UPLOAD_FOLDER, KEYS_FOLDER, RECOVERED_FOLDER]:
    os.makedirs(folder, exist_ok=True)
```

**What it does:**
- Creates three folders to organize files:
  - `uploads/`: Stores uploaded images
  - `keys/`: Stores generated stego-keys
  - `recovered/`: Stores recovered secret images
- `exist_ok=True`: Don't crash if folder already exists

---

#### File Validation

```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

**What it does:**
- Only allows image files
- `rsplit('.', 1)[1]`: Gets the file extension (e.g., "png" from "image.png")
- `.lower()`: Converts to lowercase ("PNG" → "png")
- Checks if extension is in our allowed list

---

#### Route 1: Home Page

```python
@app.route('/')
def index():
    return render_template('index.html')
```

**What it does:**
- `@app.route('/')`: When user visits the homepage
- Shows `index.html` (the main menu)

---

#### Route 2: Sender Page (Most Complex!)

```python
@app.route('/sender', methods=['GET', 'POST'])
def sender():
    if request.method == 'POST':
        # User submitted the form
        if 'cover' not in request.files or 'secret' not in request.files:
            return render_template('sender.html', error='Please upload both cover and secret images')
        
        cover_file = request.files['cover']
        secret_file = request.files['secret']
        
        if cover_file.filename == '' or secret_file.filename == '':
            return render_template('sender.html', error='Please select both files')
        
        if not (allowed_file(cover_file.filename) and allowed_file(secret_file.filename)):
            return render_template('sender.html', error='Invalid file type. Use PNG, JPG, BMP, or TIFF')
        
        session_id = str(uuid.uuid4())[:8]
        
        cover_path = os.path.join(UPLOAD_FOLDER, f'{session_id}_cover.png')
        secret_path = os.path.join(UPLOAD_FOLDER, f'{session_id}_secret.png')
        key_path = os.path.join(KEYS_FOLDER, f'{session_id}_stego_key.npy')
        
        cover_file.save(cover_path)
        secret_file.save(secret_path)
        
        try:
            shape = process_sender(cover_path, secret_path, key_path)
            return render_template('sender.html', 
                                   success=True,
                                   session_id=session_id,
                                   key_path=key_path,
                                   cover_path=cover_path,
                                   shape=f"{shape[0]}x{shape[1]}")
        except Exception as e:
            return render_template('sender.html', error=str(e))
    
    return render_template('sender.html')
```

**Step by step:**

1. **Check request type:**
   - `GET`: User just opened the page → Show empty form
   - `POST`: User submitted the form → Process the files

2. **Validate files:**
   - Check if both files were uploaded
   - Check if filenames aren't empty
   - Check if file types are allowed

3. **Generate unique session ID:**
   - `uuid.uuid4()`: Creates a random unique ID
   - `[:8]`: Take first 8 characters (e.g., "a3f7b921")
   - Prevents file name conflicts if multiple users upload at once

4. **Create file paths:**
   - `os.path.join()`: Safely combines folder and filename
   - Example: `"static/uploads/a3f7b921_cover.png"`

5. **Save uploaded files:**
   - Stores them on the server's disk

6. **Process (generate stego-key):**
   - Calls `process_sender()` from `zero_stego.py`
   - If successful: Show success message with download link
   - If error: Show error message

7. **Return result:**
   - Shows `sender.html` with success/error info

---

#### Route 3: Receiver Page

```python
@app.route('/receiver', methods=['GET', 'POST'])
def receiver():
    if request.method == 'POST':
        if 'cover' not in request.files or 'key' not in request.files:
            return render_template('receiver.html', error='Please upload both cover image and stego-key')
        
        cover_file = request.files['cover']
        key_file = request.files['key']
        
        if cover_file.filename == '' or key_file.filename == '':
            return render_template('receiver.html', error='Please select both files')
        
        if not allowed_file(cover_file.filename):
            return render_template('receiver.html', error='Invalid image file type')
        
        if not key_file.filename.endswith('.npy'):
            return render_template('receiver.html', error='Stego-key must be a .npy file')
        
        session_id = str(uuid.uuid4())[:8]
        
        cover_path = os.path.join(UPLOAD_FOLDER, f'{session_id}_cover.png')
        key_path = os.path.join(KEYS_FOLDER, f'{session_id}_key.npy')
        recovered_path = os.path.join(RECOVERED_FOLDER, f'{session_id}_recovered.png')
        
        cover_file.save(cover_path)
        key_file.save(key_path)
        
        try:
            recovered = process_receiver(cover_path, key_path, recovered_path)
            return render_template('receiver.html',
                                   success=True,
                                   session_id=session_id,
                                   recovered_path=recovered_path)
        except Exception as e:
            return render_template('receiver.html', error=str(e))
    
    return render_template('receiver.html')
```

**Similar to sender, but:**
- Expects cover image + stego-key (not secret image)
- Validates `.npy` file extension
- Calls `process_receiver()` to recover the secret
- Shows the recovered image on success

---

#### Route 4: Download Files

```python
ALLOWED_DOWNLOAD_DIRS = [KEYS_FOLDER, RECOVERED_FOLDER]

@app.route('/download/<path:filepath>')
def download_file(filepath):
    abs_path = os.path.abspath(filepath)
    allowed = False
    for allowed_dir in ALLOWED_DOWNLOAD_DIRS:
        abs_allowed = os.path.abspath(allowed_dir)
        if abs_path.startswith(abs_allowed + os.sep) or abs_path == abs_allowed:
            if os.path.isfile(abs_path):
                allowed = True
                break
    
    if not allowed:
        return "Access denied", 403
    
    return send_file(abs_path, as_attachment=True)
```

**What it does (Security important!):**
1. **Convert to absolute path:** Full path on the computer
2. **Check if file is in allowed directories:** Prevents downloading system files
3. **Verify file exists:** Makes sure it's actually a file
4. **If allowed:** Send file to user's browser
5. **If not allowed:** Show "Access denied" (HTTP 403 error)

**Why this security?**
Without it, hackers could download ANY file on the server!

---

#### Starting the Server

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

**What it does:**
- `if __name__ == '__main__'`: Only run if this is the main script
- `host='0.0.0.0'`: Accept connections from any IP address
- `port=5001`: Use port 5001 (like an apartment number for web traffic)
- `debug=True`: Show helpful error messages (turn off in production!)

---

## 🔒 Security Considerations

1. **File Size Limit**: Maximum 16MB uploads (prevents server overload)
2. **File Type Validation**: Only allows image formats (prevents malicious files)
3. **Download Protection**: Users can only download from allowed directories
4. **Session IDs**: Unique IDs prevent file conflicts and unauthorized access
5. **No Database**: Files are temporary (consider cleanup for production)

## 🧮 Mathematical Explanation

### The Core Concept

For each pixel position (x, y):

**Encoding:**
```
Key[x,y] = Secret[x,y] - Cover[x,y]
```

**Decoding:**
```
Secret[x,y] = Cover[x,y] + Key[x,y]
```

**Example with actual pixel values:**
```
Cover pixel:  150 (gray)
Secret pixel: 200 (lighter gray)
Key:          50  (the difference)

To recover:
Cover:        150
Key:          50
Recovered:    200 ✓ (exactly matches original secret!)
```

### Why This Works

The math is based on simple algebra:
```
If: K = S - C
Then: S = C + K
```

Where:
- K = Stego-Key
- S = Secret Image
- C = Cover Image

## 🎓 Educational Value

This project demonstrates:

1. **Image Processing**: Working with images as numerical arrays
2. **Web Development**: Flask, HTML, CSS, JavaScript
3. **File Handling**: Uploads, downloads, and file system operations
4. **Security**: Input validation and access control
5. **UI/UX Design**: Responsive design and theme switching
6. **Mathematics**: Practical application of subtraction/addition
7. **Steganography**: A novel approach to hiding information

## 🛠️ Technologies Used

- **Backend**: Python 3, Flask
- **Image Processing**: OpenCV (cv2), NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **File Storage**: NumPy binary format (.npy)

## 📊 Advantages of Zero-Steganography

| Traditional Steganography | Zero-Steganography |
|--------------------------|-------------------|
| Modifies cover image | Cover unchanged |
| Detectable by analysis | Undetectable |
| Capacity limits | No embedding limits |
| Quality degradation | Perfect recovery |
| Single file transmission | Two-part transmission |

## ⚠️ Limitations

1. **Two-Part Transmission**: Requires sending both cover image and stego-key separately
2. **Key Size**: Stego-key is same size as the secret image (no compression)
3. **Exact Cover Required**: Any modification to cover image breaks recovery
4. **Grayscale Only**: Current implementation works with grayscale images

## 🚀 Future Improvements

- [ ] Support for color (RGB) images
- [ ] Compression of stego-keys
- [ ] Encryption of stego-keys
- [ ] Batch processing multiple images
- [ ] Email integration for secure key sharing
- [ ] Quality metrics (PSNR) display
- [ ] Image preview before upload

## 📚 Learning Resources

- **Steganography**: Study of hiding information
- **OpenCV**: Learn image processing: https://opencv.org/
- **NumPy**: Master array operations: https://numpy.org/
- **Flask**: Build web apps: https://flask.palletsprojects.com/

## 🤝 Contributing

Feel free to fork this project and add your own improvements!

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as a demonstration of zero-steganography concepts.

---

**Remember**: The cover image must remain EXACTLY the same. Even a single pixel change will break the recovery process!

Happy Hiding! 🦕🔐
