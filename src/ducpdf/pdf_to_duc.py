"""
PDF to DUC format converter for PyMuPDF.
This module provides functionality to convert PDF documents to DUC format.
"""


#Imports ______________________________________________________________
#Standard Python Library Imports
import os
import uuid
import json
from typing import Dict, List, Optional, Union

# Import PyMuPDF
import pymupdf
import flatbuffers

# DUC-related Imports: Used to create and structure the DUC format output
# Handle binary data (images) with BinaryFilesClass
# Manage application state with AppStateClass
# Use proper element types from ElementTypes enum

import ducpy
from ducpy.utils import ElementTypes
from ducpy.utils import enums
from ducpy.classes import AppStateClass, DucElementClass, BinaryFilesClass
from ducpy.Duc.BinaryFileData import BinaryFileData


#Class ______________________________________________________________

class PDFToDucConverter:


    def __init__(self, pdf_path: str):
        
        """Initialize the converter with a PDF file path.
        
        Args:
            pdf_path: Path to the PDF file to convert
        """
        self.pdf_path = pdf_path # path to the PDF file
        self.pdf_doc = pymupdf.open(pdf_path) # opens the PDF file
            
        # Initialize ducpy components
        self.app_state = AppStateClass.AppState(
            grid_size=10,  # Default grid size
            view_background_color="#ffffff"
        )
        
        # Dictionary to store binary file data (images), keyed by file_id
        self.binary_files: Dict[str, BinaryFileData] = {}
        # list to store DUC elements (text, images, etc.)
        self.elements = [] 



        
    def convert_page(self, page_number: int) -> List[DucElementClass]:

        """Convert a single PDF page to DUC elements.
        
        Args:
            page_number: The page number to convert (0-based)
            
        Returns:
            List of DUC elements representing the page content
        """

        page = self.pdf_doc[page_number] # gets the page object
        elements = [] # list to store DUC elements
        builder = flatbuffers.Builder(0)  # Create a new builder instance
        

        # Extract text blocks
        blocks = page.get_text("dict")["blocks"] # gets the text blocks from the page

        for block in blocks: 
            if block.get("type") == 0:  # Text block
                for line in block["lines"]: # iterates through the lines in the block
                    for span in line["spans"]: # iterates through the spans*** in the line
                         # Generate a unique ID for the element
                        element_id = str(uuid.uuid4())
                        
                        # Sanitize text for potential encoding issues
                        text_content = span["text"].encode('utf-8', 'replace').decode('utf-8')

                        # Create text element using ducpy
                        text_element = DucElementClass.DucTextElement(
                            id=element_id,
                            type="text",
                            x=span["bbox"][0],
                            y=span["bbox"][1],
                            width=span["bbox"][2] - span["bbox"][0],
                            height=span["bbox"][3] - span["bbox"][1],
                            text=text_content, # Use sanitized text
                            font_size=span["size"],
                            font_family=enums.FontFamily.ROBOTO_MONO,
                            text_align=enums.TextAlign.LEFT,
                            vertical_align=enums.VerticalAlign.TOP,
                            is_deleted=False,
                            background=[],
                            scope="mm",  # Using millimeters as the default scope
                            # Missing DucElement attributes with defaults
                            stroke=[],
                            opacity=100.0,
                            angle=0.0,
                            seed=0,
                            version=0,
                            version_nonce=0,
                            group_ids=[],
                            locked=False,
                            z_index=0,
                            is_visible=True,
                            roundness=0.0,
                            label="Text Element",  # Generic label
                            subset=None,
                            blending=None,
                            frame_id=None,
                            bound_elements=None,
                            updated=0,
                            index=None,
                            link=None,
                            custom_data=None,
                            # Missing DucTextElement attributes with defaults
                            container_id=None,
                            original_text=None, # Could set to span['text'] if needed
                            line_height=1.0,
                            auto_resize=True
                        )
                        elements.append(text_element)
                        




        # Gets all images from the PDF page + Returns a list of image references
        # images = page.get_images() 

        # for img_index, img in enumerate(images):  # iterates through the images

        #     # gets the xref of the image **
        #     xref = img[0] 
        #     # Uses the xref to locate and extract the actual image data from the PDF
        #     base_image = self.pdf_doc.extract_image(xref) 
        #     """
        #     Returns a dictionary containing:
        #     width: image width
        #     height: image height
        #     image: the actual image data
        #     Other metadata about the image
        #     """
        #     if base_image:
        #         # Generate a unique ID for the element
        #         element_id = str(uuid.uuid4())
        #         file_id = f"image_{page_number}_{img_index}"
                
        #         # Get image bounding box
        #         try:
        #             img_bbox = page.get_image_bbox(img)
        #             img_x = img_bbox.x0
        #             img_y = img_bbox.y0
        #             img_width = img_bbox.width
        #             img_height = img_bbox.height
        #         except Exception: # Fallback if bbox retrieval fails
        #             img_x = 0
        #             img_y = 0
        #             img_width = base_image["width"]
        #             img_height = base_image["height"]

        #         # Create image element using ducpy
        #         image_element = DucElementClass.DucImageElement(
        #             id=element_id,
        #             type="image",
        #             x=img_x,
        #             y=img_y,
        #             width=img_width,
        #             height=img_height,
        #             file_id=file_id,
        #             is_deleted=False,
        #             background=[],
        #             scope="mm",  # Using millimeters as the default scope
        #             status="pending",  # Default status for new images
        #             # Missing DucElement attributes with defaults
        #             stroke=[],
        #             opacity=100.0,
        #             angle=0.0,
        #             seed=0,
        #             version=0,
        #             version_nonce=0,
        #             group_ids=[],
        #             locked=False,
        #             z_index=0,
        #             is_visible=True,
        #             roundness=0.0,
        #             label="Image Element", # Generic label
        #             subset=None,
        #             blending=None,
        #             frame_id=None,
        #             bound_elements=None,
        #             updated=0,
        #             index=None,
        #             link=None,
        #             custom_data=None,
        #             # Missing DucImageElement attributes with defaults
        #             scale=(1.0, 1.0),
        #             crop=None
        #         )
        #         elements.append(image_element)
                
        #         # Store binary data in the BinaryFilesClass
        #         # Convert to bytes if it's not already
        #         image_data = base_image["image"]

        #         if not isinstance(image_data, bytes):
        #             image_data = bytes(image_data)
                    
                
        return elements

        # ** 
        # XRef is a unique identifier for an image in the PDF file. It's like a pointer or reference number that 
        # tells the PDF reader where to find the actual image data in the file. 
        # Think of it as an address or index number for the image in the PDF's internal structure

        # ***
        # spans are pieces of text with the same formatting (font, size, color, etc.)
        




    def convert(self, output_path: str):
        """Convert the entire PDF document to DUC format.
        
        Args:
            output_path: Path where to save the DUC file
        """
        # Convert each page
        for page_num in range(len(self.pdf_doc)):
            page_elements = self.convert_page(page_num)
            # Add page elements to elements list
            self.elements.extend(page_elements)
        
        # Create a Duc object
        # duc = ducpy.Duc(
        #     source="PyMuPDF to DUC converter",
        #     version=5,
        #     elements=self.elements,
        #     appState=self.app_state,
        #     binaryFiles=self.binary_files
        # )
        
        # Serialize and save using ducpy functionality
        serialized_duc = ducpy.serialize.save_as_flatbuffers(self.elements, self.app_state, self.binary_files, "PyMuPDF to DUC converter")
        
        # Make sure we have the correct file extension
        if not output_path.endswith('.duc'):
            output_path = f"{output_path}.duc"
            
        # Write the file
        with open(output_path, "wb") as f:
            f.write(serialized_duc)
            
        print(f"Saved DUC file to {output_path}")

            
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'pdf_doc'):
            self.pdf_doc.close()

    def dump_text_extraction_to_json(self, json_output_path: str):
        """Dump the extracted text elements as JSON for debugging purposes."""
        # Reset elements and extract text from all pages
        self.elements = []
        for page_num in range(len(self.pdf_doc)):
            page_elements = self.convert_page(page_num)
            self.elements.extend(page_elements)
        
        # Serialize text elements into simple dictionaries
        serialized_elements = []
        for el in self.elements:
            if hasattr(el, "text"):
                serialized_elements.append({
                    "id": el.id,
                    "type": el.type,
                    "x": el.x,
                    "y": el.y,
                    "width": el.width,
                    "height": el.height,
                    "text": el.text,
                    "font_size": el.font_size,
                    "opacity": el.opacity
                })
        
        with open(json_output_path, "w", encoding="utf-8") as f:
            json.dump(serialized_elements, f, indent=2, ensure_ascii=False)
        
        print(f"Dumped text extraction JSON to {json_output_path}")


def convert_pdf_to_duc(pdf_path: str, output_path: str):
    """Convenience function to convert a PDF file to DUC format.
    
    Args:
        pdf_path: Path to the input PDF file
        output_path: Path where to save the output DUC file
    """
    converter = PDFToDucConverter(pdf_path)
    converter.convert(output_path) 