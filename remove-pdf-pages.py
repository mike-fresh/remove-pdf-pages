#!/usr/bin/env python3

import PyPDF2
import tkinter as tk
import sys

class PdfPageRemover:
    def __init__(self, pdf_files: list[str]):
        self.pdf_files = pdf_files
        self.py_pdf_files = [PyPDF2.PdfReader(x) for x in self.pdf_files]
        self.max_pages = max([len(x.pages) for x in self.py_pdf_files])
        self.pages_to_remove = ''
        self.remove_list = []
        self.window = tk.Tk()
        self.window.title("Remove pages from PDFs")
        self.window.geometry("300x120")
        self.window.resizable(False, False)
        self.window.configure(background="#000000")
        self.label = tk.Label(self.window, text="Remove pages:", bg="#000000", fg="#ffffff")
        self.label.pack(pady=10)
        self.entry_box = tk.Entry(self.window)
        self.entry_box.pack()
        self.entry_box.focus_set()
        self.entry_box.bind("<Key>", lambda event: self.key_pressed(event))
        self.button = tk.Button(self.window, text="OK", command=self.submit)
        self.button.pack(pady=10)

    def submit(self):
        self.pages_to_remove = self.entry_box.get()
        self.remove_list = self.get_remove_list()
        self.remove_pages()
        self.window.destroy()

    def get_remove_list(self) -> list[int]:
        pages = self.pages_to_remove.split(",")
        pages = [x for x in pages if x]
        pages_to_remove: list[int] = []
        for page in pages:
            if "-" in page:
                # If there is a dash, it means a range of pages
                page = page.split("-", maxsplit=1)
                start, end = page
                start = int(start) if start else 1
                end = int(end) if end else self.max_pages
                pages_to_remove += list(range(start, end + 1))
            else:
                # Otherwise, it's just a single page
                pages_to_remove.append(int(page))
        return sorted(list(set(pages_to_remove)))

    def remove_pages(self):
        for file in self.pdf_files:
            pdf = PyPDF2.PdfReader(file)
            pdf_writer = PyPDF2.PdfWriter()
            for page in range(1, len(pdf.pages) + 1):
                if page not in self.remove_list:
                    pdf_writer.add_page(pdf.pages[page - 1])
            # Save the PDFs
            with open(file, "wb") as out:
                pdf_writer.write(out)

    def key_pressed(self, event: tk.Event):
        allowed_keys = ("BackSpace", "Delete", "Tab")
        if event.keysym == "Escape":
            self.window.destroy()
        elif event.keysym == "KP_Enter" or event.keysym == "Return":
            self.submit()
        elif event.keysym not in allowed_keys and event.char not in "0123456789,-":
            return "break"
        else:
            return "pass"

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: remove-pdf-pages.py file1.pdf file2.pdf ...")
        sys.exit(1)
    app = PdfPageRemover(args)
    app.window.mainloop()
