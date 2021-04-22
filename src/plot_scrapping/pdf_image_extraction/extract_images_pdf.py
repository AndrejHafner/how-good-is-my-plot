import fitz
import os
import operator

from pathlib import Path
from bs4 import BeautifulSoup, Tag
from functools import reduce
from src.plot_scrapping.utils import save_json_metadata
from tqdm import tqdm
from PIL import Image
from io import BytesIO


def extract_images_pdf(filename):
    doc = fitz.open(filename)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            try:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n >= 5:       # this is GRAY or RGB
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    data = BytesIO(pix1.getImageData())
                    yield Image.open(data)

                data = BytesIO(pix.getImageData())
                yield Image.open(data)
            except:
                print(f"Error extracting image from: {filename}")
                continue


def parse_metadata(file_path, type):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
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
    except:
        print(f"Failed metadata parsing for: {file_path}")
        return None


def resize_image(img, side_length):
    if img.height < side_length or img.width < side_length:
        return img

    if img.height > img.width: # Set width to side length and keep aspect ratio
        scale_ratio = side_length / img.width
        new_height  = round(img.height * scale_ratio)
        return img.resize((side_length, new_height))
    else:  # Set height to side length and keep aspect ratio
        scale_ratio = side_length / img.height
        new_width  = round(img.width * scale_ratio)
        return img.resize((new_width, side_length))


if __name__ == '__main__':
    src_dir = "D:/project/FRI/druga gradiva FRI"
    dst_dir = "D:/project/extracted_images/fri_other"
    type_of_work = "fri_other"

    image_side_length = 480

    Path(dst_dir).mkdir(parents=True, exist_ok=True)
    index = 0

    for folder in tqdm(os.listdir(src_dir)):
        metadata = parse_metadata(os.path.join(src_dir, folder, "metaData.xml"), type_of_work)
        if metadata is None:
            continue

        pdf_filename = next(iter([el for el in os.listdir(os.path.join(src_dir, folder)) if ".pdf" in el]))

        for image in extract_images_pdf(os.path.join(src_dir, folder, pdf_filename)):
            try:
                if image.height < 100 or image.width < 100 or (image.height < 200 and image.width < 200):
                    continue
                resized_image = resize_image(image, image_side_length)
                resized_image.save(os.path.join(dst_dir, f"{index}.jpeg"))
                save_json_metadata(dst_dir, f"{index}", metadata)
                index += 1
            except:
                print(f"Failed to save image from: {pdf_filename}")
