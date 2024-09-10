# receipt-recognition

## About
This repository contains two Python scripts for processing receipt images and visualizing sales data. Clone the repository, install the dependencies, and follow the setup instructions to process receipt images and visualize the extracted sales data.

## Tools and Technologies
<div> <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="100" height="100"/>&nbsp&nbsp; <img src="https://github.com/devicons/devicon/blob/master/icons/googlecloud/googlecloud-original-wordmark.svg" title="Google Cloud Vision" alt="Google Cloud Vision" width="100" height="100"/>&nbsp&nbsp; </div>
 
## Frameworks and Libraries
<div> <img src="https://github.com/devicons/devicon/blob/master/icons/opencv/opencv-original-wordmark.svg" title="OpenCV" alt="OpenCV" width="80" height="80"/>&nbsp&nbsp; <img src="https://github.com/devicons/devicon/blob/master/icons/numpy/numpy-original-wordmark.svg" title="Numpy" alt="Numpy" width="80" height="80"/>&nbsp&nbsp; <img src="https://github.com/devicons/devicon/blob/master/icons/matplotlib/matplotlib-original.svg" title="Matplotlib" alt="Matplotlib" width="80" height="80"/>&nbsp&nbsp; </div>

## How To Set Up and Run
## Requirements

The following Python packages are required to run the scripts:

opencv-python
numpy
imutils
google-cloud-vision
google-auth
python-dotenv (optional, for managing environment variables)
matplotlib (for data visualization)

## Setup

```bash
Clone the Repository Navigate to the Project Directory:

$ git clone https://github.com/your-repo/receipt-processing.git
$ cd receipt-recognition

Create a Virtual Environment (Optional):

# On Windows
$ python -m venv env
.\env\Scripts\activate

# On macOS/Linux
$ python3 -m venv env
source env/bin/activate

Install the Libraries
$ pip install opencv-python numpy imutils google-cloud-vision google-auth matplotlib

Google Cloud Vision API Setup:

Enable the Google Cloud Vision API and download your service account key as a JSON file.

Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your JSON key file:

#Windows:
$ set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service_account_key.json

#macOS/Linux:
$ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service_account_key.json

#Running the Scripts
##Processing the Receipt Image

Use shoper.py to process a receipt image and extract sales data:

$python shoper.py <image_path>

Example:
$ python shoper.py receipt.png

The script outputs extracted data to sales_data.csv and the formatted text to google_vision_extracted_text.txt.
Intermediate steps (grayscale, binarized, contour-detected, and perspective-corrected images) are saved as PNG files.

##Visualizing the Sales Data

Use infovis.py to generate a graph summarizing the sales data:

$ python infovis.py
The script reads from sales_data.csv and generates a graph of items, quantities, and total prices.


```
