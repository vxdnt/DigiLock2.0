import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import re
from PIL import Image

# Your OCR.Space API key


def detect(file_path):
    print(__name__)
    API_KEY = 'K81317463788957'
    # Function to open a file dialog and return the selected file path
    def browse_file():
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(title="Select Document", filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("PDF files", "*.pdf")])
        return file_path

    # Function to extract text from the image using OCR.Space API
    def extract_text_from_image(image_path, api_key):
        url = 'https://api.ocr.space/parse/image'
        with open(image_path, 'rb') as file:
            response = requests.post(url, files={'file': file}, data={'apikey': api_key, 'language': 'eng'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('IsErroredOnProcessing'):
                raise Exception(f"Error: {result.get('ErrorMessage')}")
            return result['ParsedResults'][0]['ParsedText']
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.content}")

    # Function to rotate image and perform OCR
    def extract_text_from_rotated_image(image_path, rotation_angle, api_key):
        img = Image.open(image_path)  # Open the image
        rotated_img = img.rotate(rotation_angle, expand=True)  # Rotate the image
        rotated_img.save("rotated_image.png")  # Save the rotated image temporarily
        
        # Perform OCR on the rotated image
        text = extract_text_from_image("rotated_image.png", api_key)
        
        # Optionally remove the temporary image
        # import os
        # os.remove("rotated_image.png")
        
        return text

    # Function to detect 12-digit numbers or 3 groups of 4 digits separated by spaces
    def detect_12_digit_number(text):
        pattern = r'\b\d{12}\b|\b\d{4} \d{4} \d{4}\b'
        numbers = re.findall(pattern, text)
        return numbers

    # Function to validate Aadhaar number format
    def isValidAadhaarNumber(number):
        regex = r'^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$|^[2-9]{1}[0-9]{11}$'
        return bool(re.match(regex, number))

    # Function to validate PAN card number format
    def isValidPanCardNo(panCardNo):
        regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
        return bool(re.match(regex, panCardNo) and len(panCardNo) == 10)

    # Function to validate passport number format
    def isValidPassportNo(s):
        pattern = r'^[A-Z][1-9]\d\s?\d{4}[1-9]$'
        return bool(re.match(pattern, s))

    # Main function to process the document
    def process_document(file_path):
        print("Please upload a document...")
        file_path = file_path  # Ask user to upload a document
        
        if not file_path:
            messagebox.showinfo("No file", "No file selected.")
            return
        
        # messagebox.showinfo("File Selected", f"Processing file: {file_path}")
        
        try:
            # Perform OCR on the original image
            text = extract_text_from_image(file_path, API_KEY)
            
            # Rotate image and perform OCR for each rotation (90, 180, 270 degrees)
            for angle in [90, 180, 270]:
                rotated_text = extract_text_from_rotated_image(file_path, angle, API_KEY)
                text += " " + rotated_text  # Combine text from all rotations
            
            # Detect 12-digit numbers or 3 groups of 4 digits separated by spaces
            detected_numbers = detect_12_digit_number(text)
            global message_detection
            global message_status
            if detected_numbers:
                for number in detected_numbers:
                    if isValidAadhaarNumber(number):
                        # messagebox.showinfo("Aadhaar Number Found", f"The document contains a valid Aadhaar number: {number}")
                        message_detection = f"Aadhar number is found, the document contains a valid aadhar number: {number}"
                        message_status = True
                        return  # Exit after finding Aadhaar number
                # messagebox.showinfo("Invalid Format", "Detected number does not match Aadhaar format.")
                message_detection = f"Invalid Format, Detected number does not match Aadhaar format."
                message_status = False
            else:
                # Check for PAN card number
                pan_card_numbers = re.findall(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', text)
                if pan_card_numbers:
                    for pan_card_number in pan_card_numbers:
                        if isValidPanCardNo(pan_card_number):
                            # messagebox.showinfo("PAN Card Number Found", f"The document contains a valid PAN card number: {pan_card_number}")
                            message_detection = f"PAN Card Number Found, the document contains a valid PAN card number: {pan_card_number}"
                            message_status = True
                            return  # Exit after finding PAN card number
                    # messagebox.showinfo("Invalid Format", "Detected PAN card number does not match format.")
                    message_detection = f"Invalid Format Detected PAN card number does not match format."
                    message_status = False
                else:
                    # Check for passport number
                    passport_numbers = re.findall(r'\b[A-Z][1-9]\d\s?\d{4}[1-9]\b', text)
                    if passport_numbers:
                        for passport_number in passport_numbers:
                            if isValidPassportNo(passport_number):
                                # messagebox.showinfo("Valid Passport Document", "It's a valid passport document.")
                                message_detection = f"Valid Passport Document, It's a valid passport document."
                                message_status = True
                                return  # Exit after finding valid passport number
                        # messagebox.showinfo("Invalid Format", "Detected passport number does not match format.")
                        message_detection = f"Invalid Format Detected passport number does not match format."
                        message_status = False
                    else:
                        # messagebox.showinfo("No Numbers Found", "No 12-digit numbers, PAN card numbers, or passport numbers detected")
                        message_detection = f"No Numbers Found, No 12-digit numbers, PAN card numbers, or passport numbers detected."
                        message_status = False
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Example usage
    if __name__ == "passport_aadhaar_pan":
        process_document(file_path)

    return message_detection, message_status