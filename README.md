# receipt-recognition

Receipt Processing and Visualization
This repository contains two Python scripts:

shoper.py: Processes receipt images, extracts item details, and saves them to a CSV file.
infovis.py: Visualizes the sales data from the CSV file.
Requirements
Libraries
To run the scripts, install the following Python packages:

opencv-python
numpy
imutils
google-cloud-vision
google-auth
python-dotenv (optional, for managing environment variables)
matplotlib (for data visualization)
Setup
Clone the Repository:

bash
Copy code
git clone https://github.com/your-repo/receipt-processing.git
cd receipt-processing
Create a Virtual Environment (Optional):

bash
Copy code
# On Windows
python -m venv env
.\env\Scripts\activate

# On macOS/Linux
python3 -m venv env
source env/bin/activate
Install the Libraries:

bash
Copy code
pip install opencv-python numpy imutils google-cloud-vision google-auth matplotlib
Google Cloud Vision API Setup:

Enable the Google Cloud Vision API and download your service account key as a JSON file.

Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your JSON key file:

Windows:

bash
Copy code
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service_account_key.json
macOS/Linux:

bash
Copy code
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service_account_key.json
Running the Scripts
1. Processing the Receipt Image
Use shoper.py to process a receipt image and extract sales data:

bash
Copy code
python shoper.py <image_path>
Example:

bash
Copy code
python shoper.py receipt.png
The script outputs extracted data to sales_data.csv and the formatted text to google_vision_extracted_text.txt.
Intermediate steps (grayscale, binarized, contour-detected, and perspective-corrected images) are saved as PNG files.
2. Visualizing the Sales Data
Use infovis.py to generate a graph summarizing the sales data:

bash
Copy code
python infovis.py
The script reads from sales_data.csv and generates a graph of items, quantities, and total prices.
