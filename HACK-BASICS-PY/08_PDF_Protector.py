import PyPDF2
import sys

def create_password_protected_pdf(input_pdf,output_pdf,password):
    try:
        # Opens the input file in binary read mode ('rb').
        # with ensures the file is properly closed afterward.
        with open(input_pdf,'rb') as pdf_file:

            # Creates a PdfReader object to read the pages of the PDF.
            pdf_reader=PyPDF2.PdfReader(pdf_file)

            # Creates a PdfWriter object to write new PDF content.
            pdf_writer=PyPDF2.PdfWriter()

            # Loops through all pages of the input PDF and adds them to the writer object one by one.
            for page_num in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            # Applies password protection using the given password.
            pdf_writer.encrypt(password)

            # Opens the output file in binary write mode ('wb').
            # Writes the encrypted PDF to disk.
            with open(output_pdf,'wb') as output_file:
                pdf_writer.write(output_file)

            print(f"Password protected PDF saved as {output_pdf}")

    except FileNotFoundError:
        print(f"The file {input_pdf} was not found.")
    except PyPDF2.utils.PdfReadError:
        print(f"The file {input_pdf} is not a valid PDF.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) !=4:
        print("Usage: python 3 script.py <input_pdf> <output_pdf> <password>")
        # sys.exit(1) exits the program with a status code 1 (which typically indicates an error).
        sys.exit(1)

    # These lines extract the arguments from the command line and assign them to variables.
    input_pdf  = sys.argv[1]
    output_pdf = sys.argv[2]
    password   = sys.argv[3]

    create_password_protected_pdf(input_pdf,output_pdf,password)

# This ensures that main() only runs when the script is executed directly,
# not when it's imported as a module in another script.
if __name__ == "__main__":
    main()



# ------------------------------------------------------------------------------
# 1. Open the python terminal
# CMD:
# python .\08_PDF_Protector.py "Hello World.pdf" "Hello Worldv2.pdf" 1234
# ------------------------------------------------------------------------------













