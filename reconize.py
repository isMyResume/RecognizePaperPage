import os
import re
from pathlib import Path

import pytesseract
from PIL import Image


def image_size_check(img_orig_size, coordinate):
    if coordinate['left'] == -1:
        coordinate['left'] = 0
    if coordinate['upper'] == -1:
        coordinate['upper'] = 0
    if coordinate['right'] == -1:
        coordinate['right'] = img_orig_size[0]
    if coordinate['lower'] == -1:
        coordinate['lower'] = img_orig_size[1]
    return coordinate


def page_reconize(full_filename, coordinate):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\kouploa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

    img_orig = Image.open(full_filename).convert("1")

    coordinate = image_size_check(img_orig.size, coordinate)


    croppedImage = img_orig.crop((coordinate['left'], coordinate['upper'], coordinate['right'], coordinate['lower']))

    ocr_result = pytesseract.image_to_string(croppedImage, lang='eng+kor')

    hangul = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')

    alphabet = re.compile('[a-zA-z]')
    parseText = re.sub(hangul, '', ocr_result)
    parseText = re.sub(alphabet, '', parseText)

    page_number = re.sub(r'[^0-9 _]', '', ocr_result)
    page_number = page_number.strip()
    page_number = page_number.replace(" ", "_")
    for char in page_number:
        page_number = page_number.replace("__", "_")

    if page_number != '':
        page_number_zfill = re.findall(r'[0-9]{,3}$', page_number)[0].zfill(5)
    else:
        page_number_zfill = '00000'

    return page_number_zfill



def book_reconize(dirname, coordinate):
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        filetime = os.path.getmtime(full_filename)
        page_number = page_reconize(full_filename, coordinate)

        if page_number == '':
            page_number = '000'
            file_rename = Path(filename).stem + "_" + page_number + Path(filename).suffix
        else:
            file_rename = Path(filename).stem + "_" + page_number + Path(filename).suffix

        os.rename(os.path.join(dirname, filename), os.path.join(dirname, file_rename))
