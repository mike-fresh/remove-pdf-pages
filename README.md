# Remove PDF Pages
This is a simple script to remove pages from PDF files. 
It can be used as a shell script or act as an extension to Thunar file manager.
# Installation of dependencies
     pip3 install PyPDF2
# Configuration of Thunar custom action
Add this to your `~/.config/Thunar/uca.xml` file:

    <action>
        <icon></icon>
        <name>Remove PDF pages</name>
        <unique-id>1677018688647949-1</unique-id>
        <command>/path/to/script/remove-pdf-pages.py %N</command>
        <description></description>
        <patterns>*.pdf;*.PDF;*Pdf</patterns>
        <other-files/>
    </action>

# Usage
To run as a shell script:

    python3 remove-pdf-pages.py file1.pdf file2.pdf ...
Or just right click in Thunar to selected files and choose `Remove PDF pages`