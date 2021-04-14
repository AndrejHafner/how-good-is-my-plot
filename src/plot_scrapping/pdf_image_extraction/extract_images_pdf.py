import fitz
import os
import operator

from pathlib import Path
from bs4 import BeautifulSoup, Tag
from functools import reduce
from src.plot_scrapping.utils import save_json_metadata
from tqdm import  tqdm


def extract_images_pdf(filename):
    doc = fitz.open(filename)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            if pix.n >= 5:       # this is GRAY or RGB
                yield fitz.Pixmap(fitz.csRGB, pix)
            yield pix

def parse_metadata(file_path, type):
    with open(file_path, "r") as f:
        data = reduce(operator.concat, f.readlines(), "")
        xml = BeautifulSoup(data, "lxml")
        title = xml.find("naslov").text
        keywords = [el.text for el in xml.find("tujjezik_kljucnebesede").contents if isinstance(el, Tag) and len(el.text.strip()) > 0]
        author_tag = next(iter([el for el in xml.find("osebe").contents if isinstance(el, Tag) and el["vloganaziv"] == "Avtor"]))
        author = f"{author_tag['ime']} {author_tag['priimek']}"
        url = xml.find("url").text
        return {"title": title,
                "keywords": keywords,
                "author": author,
                "url": url,
                "type": type}


if __name__ == '__main__':
    src_dir = "./pdfs/fri_diplome"
    dst_dir = "./extracted_images/fri_bachelor_thesis"
    type_of_work = "bachelor_thesis"


    Path(dst_dir).mkdir(parents=True, exist_ok=True)
    index = 0

    for folder in tqdm(os.listdir(src_dir)):
        metadata = parse_metadata(os.path.join(src_dir, folder, "metaData.xml"), type_of_work)
        pdf_filename = next(iter([el for el in os.listdir(os.path.join(src_dir, folder)) if ".pdf" in el]))

        for image in extract_images_pdf(os.path.join(src_dir, folder, pdf_filename)):
            try:
                image.writeImage(os.path.join(dst_dir, f"{index}.jpeg"))
                save_json_metadata(dst_dir, f"{index}", metadata)
                index += 1
            except:
                print(f"Failed to save image from: {pdf_filename}")
