# Automated Signature Inserter

## Overview
The **Automated Signature Inserter** is a Python-based tool designed to streamline the process of adding signatures and stamps to PDF documents. This program automates the placement of signatures at specified locations based on either textual markers or predefined templates, significantly reducing manual effort and ensuring consistency.

## Features
- **Dynamic Signature Placement**: Automatically detects predefined text in PDF documents and places the signature near the detected location.
- **Color Detection**: Supports detecting blue and green stamps or signatures while removing unnecessary white backgrounds to ensure clean and transparent overlays.
- **Selective Page Processing**: Only modifies pages containing relevant markers, leaving other pages untouched.
- **Separate Output for Key Pages**: Extracts and saves modified pages with the first or second stamp into a separate folder (`APK`), appending `_APK` to the filename for easy identification.
- **Customizable Parameters**: Includes scaling options, positional adjustments, and custom search keywords for greater flexibility.
- **Batch Processing**: Processes multiple PDF files from a specified directory (`source`) and saves outputs in designated folders (`podpisane` for all modified files and `APK` for key pages).

## How It Works
1. **Input PDFs**: The program scans the `source` directory for all PDF files to process.
2. **Signature Detection**: Uses either a text-based marker (e.g., "representative's signature") or predefined image matching to identify the placement location for signatures.
3. **Stamp Cleaning**: Enhances transparency by removing unnecessary white areas around the signature or stamp.
4. **Output Files**:
   - **All modified PDFs**: Saved in the `podpisane` folder.
   - **Key pages with stamps**: Extracted and saved in the `APK` folder for easy reference.

## Dependencies
The tool requires the following Python libraries:
- `PyMuPDF` (fitz) – for reading and modifying PDFs.
- `PyPDF2` – for writing updated PDFs.
- `reportlab` – for generating pages with added graphics (e.g., signatures).
- `Pillow` – for image manipulation.
- `OpenCV` – for advanced image processing and color detection.
- `NumPy` – for efficient numerical operations during image processing.
