import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from google.cloud import vision
from google.oauth2 import service_account
import io
import sys
import csv
import os

# Load the credentials path from the environment variable
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if credentials_path is None:
    print("[ERROR] GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
    sys.exit(1)

def initialize_vision_client():
    """Initializes the Google Vision API client with credentials."""
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    return client

# Function to correct the perspective of an image using four-point transform
def perspective_correction(image, contour):
    """Performs perspective correction based on the largest contour."""
    # Approximate the contour to 4 points (if possible)
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Ensure we have a quadrilateral
    if len(approx) == 4:
        # Apply four-point perspective transform
        corrected = four_point_transform(image, approx.reshape(4, 2))
        return corrected
    else:
        print("The contour does not form a quadrilateral. Using bounding box approximation.")
        # If not a quadrilateral, use a bounding rectangle
        rect = cv2.boundingRect(contour)
        approx = np.array([[rect[0], rect[1]], 
                           [rect[0] + rect[2], rect[1]], 
                           [rect[0] + rect[2], rect[1] + rect[3]], 
                           [rect[0], rect[1] + rect[3]]], dtype=np.float32)
        corrected = four_point_transform(image, approx)
        return corrected

# Preprocess the image for visualization and save intermediate steps (grayscale, binarization, contours, perspective correction)
def preprocess_image_for_visualization(image_path):
    """Applies grayscale, binarization, contour detection, and perspective correction, saving intermediate steps."""
    print("[INFO] Reading the image...")
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Unable to open the image file at {image_path}")
        sys.exit(1)

    # Grayscale conversion
    print("[INFO] Converting to grayscale...")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('grayscale_image.png', gray)
    print("[INFO] Grayscale image saved")

    # Apply adaptive thresholding to make text stand out (binarized image)
    print("[INFO] Applying adaptive thresholding...")
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite('binarized_image.png', adaptive_thresh)
    print("[INFO] Binarized image saved")

    # Detect contours in the binarized image
    print("[INFO] Detecting contours...")
    contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        print("[ERROR] No contours found!")
        sys.exit(1)

    # Draw contours for visualization
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    cv2.imwrite('contour_detected_image.png', contour_image)
    print("[INFO] Contour detection image saved")

    # Find the largest contour for perspective correction (assuming it's the receipt)
    print("[INFO] Finding the largest contour...")
    largest_contour = max(contours, key=cv2.contourArea)

    # Perform perspective correction using four-point transform
    print("[INFO] Applying perspective correction...")
    corrected = perspective_correction(image, largest_contour)
    cv2.imwrite('perspective_corrected_image.png', corrected)
    print("[INFO] Perspective corrected image saved")

    return corrected

# Detect and format text using Google Cloud Vision API and save to CSV
def detect_text(path):
    """Detects text in the file using Google Cloud Vision API and saves the sales data to a CSV."""
    
    # Manually load the credentials
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    
    # Initialize the Vision client with credentials
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Open and process the original image (not the preprocessed one)
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Call text detection API
    print("[INFO] Detecting text from the receipt...")
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    
    if not annotations:
        print("[INFO] No text detected.")
        return []

    # List to hold text lines grouped by their y-coordinate
    line_groups = []

    # Process each annotation (skip the first one, it's the full text)
    for annotation in annotations[1:]:
        # Get bounding box vertices (the four corners of the word)
        vertices = annotation.bounding_poly.vertices
        text = annotation.description.strip()
        
        # Determine the y-coordinate of the word (average of the top two vertices)
        y_coord = (vertices[0].y + vertices[1].y) // 2
        
        # Try to find an existing line group that is close enough in y-coordinate
        found_group = False
        for group in line_groups:
            group_y = group['y']
            # If the current word's y-coordinate is close to the group's y, add it to this group
            if abs(y_coord - group_y) < 10:  # Adjust the threshold as needed
                group['words'].append((vertices[0].x, text))
                found_group = True
                break

        # If no matching group is found, create a new group for this line
        if not found_group:
            line_groups.append({'y': y_coord, 'words': [(vertices[0].x, text)]})

    # Sort the groups by their y-coordinate (top to bottom)
    line_groups.sort(key=lambda g: g['y'])

    # Prepare the final formatted text (without modification) and extract sales data
    formatted_text = ""
    sales_data = []

    for group in line_groups:
        # Sort words in each group by their x-coordinate (left to right)
        group['words'].sort(key=lambda w: w[0])
        
        words = [word[1] for word in group['words']]

        # Combine the words into the formatted text for the output
        formatted_line = " ".join(words)
        formatted_text += formatted_line + "\n"

        # Check if we have a valid item, quantity, and price line
        if len(words) >= 3 and words[-1].replace('.', '', 1).isdigit() and words[-2].isdigit():
            # Skip lines that look like barcodes or long numbers (more than 2 numbers in a line)
            number_count = sum(1 for word in words if word.replace('.', '', 1).isdigit())
            if number_count > 2:
                continue

            # Avoid detecting long numbers like phone numbers or barcodes as quantities/prices
            if len(words[-1]) <= 5 and len(words[-2]) <= 5:  # Ensuring numbers are reasonable for qty/price
                item_name = " ".join(words[:-2])  # Everything before the last two elements is the item name
                qty = int(words[-2])             # Second-to-last is the quantity
                total = float(words[-1])         # Last is the price
                sales_data.append([item_name, qty, total])

    # Save the sales data to a CSV file
    with open('sales_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Item', 'Quantity', 'Total'])  # Write header
        csvwriter.writerows(sales_data)  # Write sales data rows

    print("[INFO] Sales data saved to sales_data.csv")

    # Output the formatted text to a file
    with open('google_vision_extracted_text.txt', 'w', encoding='utf-8') as f:
        f.write(formatted_text)

    print("[INFO] Formatted Text:\n", formatted_text)

    return sales_data  # Return the extracted sales data

# Main workflow
if __name__ == "__main__":
    # Check if the image path was provided as an argument
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python shoper.py <image_path>")
        sys.exit(1)

    # Get the image path from the command-line argument
    receipt_image_path = sys.argv[1]

    # Step 1: Preprocess the image just for visualization (grayscale, binarization, contour detection, perspective correction)
    corrected_image = preprocess_image_for_visualization(receipt_image_path)

    # Save the corrected image for text extraction
    corrected_image_path = "corrected_image_for_text.png"
    cv2.imwrite(corrected_image_path, corrected_image)

    # Step 2: Use the corrected image for text extraction using Google Vision API
    detect_text(corrected_image_path)