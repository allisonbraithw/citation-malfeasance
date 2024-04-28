import os
from PyPDF2 import PdfReader

# Define the path to your folder containing the PDFs
folder_path = 'papers/'

# Prepare a long string to store all the extracted texts
all_texts = ""

# Iterate over each file in the specified folder
for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
        # Construct full file path
        file_path = os.path.join(folder_path, filename)
        
        # Attempt to open and read the PDF file
        try:
            reader = PdfReader(file_path)
            text = []
            
            # Read each page of the PDF
            for page in reader.pages:
                text.append(page.extract_text())
            
            # Join all pages' text and add it to the main string with formatting
            all_texts += f" ----{filename[:-4]}----- \n{''.join(text)}\n----End of {filename[:-4]}----- \n"
        
        except Exception as e:
            print(f"Failed to process {filename}: {str(e)}")

output_file_path = "concatenated_papers.txt"
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(all_texts)
