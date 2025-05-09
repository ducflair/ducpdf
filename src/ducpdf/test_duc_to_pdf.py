#!/usr/bin/env python3
# Run this file in the terminal with command:
# python -m src.ducpdf.test_duc_to_pdf /path/to/your/file.pdf

"""
Test script for PDF to DUC conversion.
This script demonstrates how to use the PDF to DUC conversion functionality.
"""


# Imports ______________________________________________________________

import os
import sys
import io
import argparse

# Import PyMuPDF
try:
    import pymupdf
except ImportError:
    print("Error: PyMuPDF not installed. Please install it with: pip install pymupdf")
    sys.exit(1)

# Import ducpy for verification
try:
    import ducpy
except ImportError:
    print("Error: ducpy not installed. Please install it.")
    sys.exit(1)

# Import the conversion module directly
from src.ducpdf.pdf_to_duc import convert_pdf_to_duc




# functions ______________________________________________________________

def main():

    """Main function to test PDF to DUC conversion."""


    ## Deal with input pdf file path ----- 

    parser = argparse.ArgumentParser(description="Test script for PDF to DUC conversion.")
    parser.add_argument("pdf_file", help="Path to the PDF file to convert")
    parser.add_argument("--dump-json", action="store_true", help="Dump extracted text from PDF as JSON")
    args = parser.parse_args()

    pdf_path = args.pdf_file
    base_file_name = os.path.basename(pdf_path)
    base_name = os.path.splitext(base_file_name)[0]


    ## Deal with the outputs path ----- 
    
    # Define the outputs directory
    # Go up to the root of the project, then into tests/outputs
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    outputs_dir = os.path.join(project_root, "tests", "outputs")
    
    # Create outputs directory if it doesn't exist
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Generate output path in the outputs directory
    output_path = os.path.join(outputs_dir, f"{base_name}.duc")
    
    print(f"Converting {pdf_path} to {output_path}...")

    
    ## Convert PDF to DUC ----- 

    # Convert PDF to DUC
    convert_pdf_to_duc(pdf_path, output_path)

    ## Deal with the output file ----- 
    
    # Verify the output file exists
    if os.path.exists(output_path):
        print(f"Conversion completed. DUC file saved to {output_path}")
        
        # Optional: Verify that the file can be parsed by ducpy
        try:
            with open(output_path, "rb") as f:
                duc_data = f.read()
            
            # Wrap duc_data in an io.BytesIO stream
            duc_data_stream = io.BytesIO(duc_data)
            
            # Pass the stream to the parsing function
            parsed_duc = ducpy.parse.parse_duc.parse_duc_flatbuffers(duc_data_stream)
            
            # Print the type and keys of parsed_duc to understand its structure
            print(f"Type of parsed_duc: {type(parsed_duc)}")
            if isinstance(parsed_duc, dict):
                print(f"Keys in parsed_duc: {list(parsed_duc.keys())}")
                # Assuming elements are under the key 'elements'
                num_elements = len(parsed_duc.get('elements', [])) 
            else:
                # Fallback or error if not a dict, though the error says it is
                print("parsed_duc is not a dictionary as expected.")
                num_elements = 0 

            print(f"DUC file validated successfully. Contains {num_elements} elements.")
        except Exception as e:
            print(f"Warning: Could not validate DUC file: {e}")
    else:
        print(f"Error: DUC file was not created at {output_path}")

    # If the '--dump-json' flag is provided, dump the extracted text elements as JSON for debugging purposes
    if args.dump_json:
        from src.ducpdf.pdf_to_duc import PDFToDucConverter
        converter = PDFToDucConverter(pdf_path)
        json_output_path = os.path.join(outputs_dir, f"{base_name}.json")
        converter.dump_text_extraction_to_json(json_output_path)

if __name__ == "__main__":
    main() 