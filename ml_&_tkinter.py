import tkinter as tk
from tkinter import messagebox, filedialog
from urllib.request import urlopen
from urllib.error import URLError
from PIL import Image, ImageTk
import subprocess
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import tldextract  
import ssl
import socket
import urllib3
import certifi

# Define the makeTokens function
def makeTokens(url):
    # Extract features from the URL
    features = []

    # Tokenize by slash, hyphen, and dot as before
    tkns_By_SLASH = str(url.encode('utf-8')).split('/')
    for i in tkns_By_SLASH:
        tokens = str(i).split('-')
        tkns_By_Dot = []
        for j in range(0, len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')
            tkns_By_Dot = tkns_By_Dot + temp_Tokens
        features += tkns_By_SLASH + tkns_By_Dot

    # Remove common elements
    features = list(set(features))
    if 'com' in features:
        features.remove('com')

    # Extract additional features using tldextract
    ext = tldextract.extract(url)
    features.extend([ext.subdomain, ext.domain, ext.suffix])

    return features

# Load the machine learning model
def load_model():
    # Load Url Data
    urls_data = pd.read_csv("phishing_site_urls.csv")
    y = urls_data["label"]
    url_list = urls_data["url"]

    # Using Custom Tokenizer
    vectorizer = TfidfVectorizer(tokenizer=makeTokens)
    X = vectorizer.fit_transform(url_list)
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model Building
    logit = LogisticRegression()
    logit.fit(X_train, y_train)

    return vectorizer, logit

def check_url():
    entered_url = url_entry.get()

    # Call the machine learning model for prediction
    prediction = predict_url(entered_url)

    if prediction == "bad":
        messagebox.showinfo("Result", "This is a fake URL!")
    else:
        messagebox.showinfo("Result", "URL is secure.")

def predict_url(url):
    # Use the loaded machine learning model for prediction
    X_predict = vectorizer.transform([url])
    result = logit.predict(X_predict)
    return result[0]

root = tk.Tk()
root.title("Defence Cops")
root.configure(bg="black")

window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}+0+0")

bg_image = Image.open("another.jpg")
bg_image = bg_image.resize((window_width, window_height))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

heading_label = tk.Label(root, text="Defence Cops", font=("Helvetica", 38), fg="light green", bg="black")
heading_label.pack(pady=20)

# Load the machine learning model 
vectorizer, logit = load_model()

url_frame = tk.Frame(root, bg="black")
url_frame.pack(expand=True)

label = tk.Label(url_frame, text="Enter URL:", font=("Helvetica", 16), fg="light green", bg="black")
label.pack(pady=10)

url_entry = tk.Entry(url_frame, width=50, font=("Helvetica", 14), bg="light green", fg="black")
url_entry.pack(pady=10)

check_button = tk.Button(root, text="Check URL", command=check_url, font=("Helvetica", 16), bg="light green", fg="black")
check_button.pack(pady=10)

def is_ssl_certified(url):
    try:
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        response = http.request('GET', url)
        # If the response status is 200, then the SSL certificate is considered valid
        if response.status == 200:
            return True
        else:
            return False
    except urllib3.exceptions.MaxRetryError:
        
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def check_ssl_certification():
    entered_url = url_entry.get()

    # Check SSL certification
    ssl_result = is_ssl_certified(entered_url)
    if ssl_result:
        ssl_message = "SSL Certified"
    else:
        ssl_message = "Not SSL Certified"

    messagebox.showinfo("SSL Certification", ssl_message)

ssl_button = tk.Button(root, text="Check SSL Certification", command=check_ssl_certification, font=("Helvetica", 16), bg="light green", fg="black")
ssl_button.pack(pady=10)

'''def select_image():
    file_path = filedialog.askopenfilename(title="Select Background Image", filetypes=[("Image files", ".png;.jpg;.jpeg;.gif")])
    if file_path:
        set_background_image(file_path)'''

# Add a button to select a background image
'''select_image_button = tk.Button(root, text="Select Background Image", command=select_image, font=("Helvetica", 14), bg="light green", fg="black")
select_image_button.pack(pady=10)'''

'''def set_background_image(another):
    bg_image = Image.open(another)
    bg_image = bg_image.resize((window_width, window_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label.configure(image=bg_photo)
    bg_label.image = bg_photo'''

# Run the Tkinter event loop
root.mainloop()
