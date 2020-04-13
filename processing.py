import ebooklib
from ebooklib import epub
import base64
from bs4 import BeautifulSoup
import gc


def clean_html(text):
    print("### DEBUG: processing.py: started cleaning of html ###")
    # remove b' am anfang und ' am ende'
    text = text[2:]
    text = text[:-1]
    # replace \t undsoweiter
    newline = f"\n"
    tab = "    "
    text = text.replace("\\'", '"')
    text = text.replace("\\n", newline)
    text = text.replace("\\t", tab)
    text = text.replace("//", "/")
    # text = text.replace("&#13;", "\r")
    # replace utf literals to chars or html code
    text = text.replace("\\xc2\\xa0", " ")
    text = text.replace("\\xe2\\x80\\x9c", "“")  # “
    text = text.replace("\\xe2\\x80\\x9d", "”")  # ”
    text = text.replace("\\xc2\\xa9", "&#169;")  # copyright
    text = text.replace("\\xc2\\xa7", "&#167;")  # §
    text = text.replace("\\xe2\\x80\\x94", "&#8212;")  # em dash, langer --
    text = text.replace("\\xe2\\x80\\x93", "&#8211;")  # en dash, kurzes -
    text = text.replace("\\xe2\\x80\\xa2", "&#8226;")  # bullet
    text = text.replace("\\xe2\\x80\\xa6", "&#8230;")  # ellipsis, ...
    text = text.replace("\\xe2\\x80\\x99", "'")  # '
    text = text.replace("\\xe2\\x80\\x98", "'")  # '
    text = text.replace("&#13;", " ")
    print("### DEBUG: processing.py: finished cleaning of html, returning html to main.py ###")
    return text


# a = '##\xc2\xa7 PENIS \xe2\x80\x9c#'
# a = "b'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<!DOCTYPE html>\n<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\" epub:prefix=\"z3998: http://www.daisy.org/z3998/2012/vocab/structure/#\" lang=\"en\" xml:lang=\"en\">\n  <head/>\n  <body><h1 style=\"text-align: center;\">Konosuba Volume 1: Ah My Useless\xc2\xa0Goddess</h1>&#13;\n#"
# a = "##Konosuba Volume 1: Ah My Useless\xc2\xa0Goddess</h1>&#13;\n#"
# a = "##you\xe2\x80\x99ve died#"
# a = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html><html xmlns="http:/www.w3.org/1999/xhtml" xmlns:epub="http:/www.idpf.org/2007/ops" epub:prefix="z3998: http:/www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">  <head/>  <body><h1 style="text-align: center;">Konosuba Volume 1: Ah My Useless\xc2\xa0Goddess</h1> '
# a = 'ht\xe2\x80\x99ve been sho'
# b = clean_html(a)
# print(b)

def provide_images(text, path, screensize):
    print(f"### DEBUG: processing.py: provide_images() path: {path} ###")
    print(f"### DEBUG: processing.py: provide_images() screensize: {screensize} ###")
    # read .epub and convert all images to dict[img_name] = b64__img_data
    book = epub.read_epub(path)
    images_b64 = {}
    for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        image_data = item.get_content()
        image_name = item.get_name()
        image_data_64 = base64.b64encode(image_data)
        images_b64[image_name] = image_data_64
    print("### DEBUG: processing.py finished converting of images to b64 data ###")
    print("")

    image_srcs = []
    soup = BeautifulSoup(text, features="lxml")
    # gesamte img line in liste als string
    images_lines = [str(element) for element in soup.find_all('img')]
    # append image tag also
    for element in soup.find_all('image'):
        images_lines.append(str(element))
    print("### DEBUG: processing.py:   images_lines ###")
    print(images_lines)
    print("")

    # alle src als string im dict image
    images = soup.findAll('img')
    other_images = soup.findAll('image')
    for image in images:
        image_srcs.append(image['src'])
    for other in other_images:
        image_srcs.append(other['xlink:href'])

    print("### DEBUG: processing.py:   image_srcs ###")
    print(image_srcs)
    print("")



    # ersetze srcs in html text durch b64 data vom bild
    for image_line, image_src in zip(images_lines, image_srcs):
            print(f"### DEBUG: processing.py: Processing {image_line} ###")
            print("")
            print(f"### DEBUG: with src: {image_src}")
            image_line_b64 = image_line[:]
            print(f"### DEBUG: unprocessed image_line_b64, copy of: {image_line} : {image_line_b64}")
            tmp_image_src = image_src[3:]
            replacestring = str(images_b64[tmp_image_src])
            replacestring = "data:image/png;base64," + replacestring[2:]
            print(f"### DEBUG: created replace template string: {replacestring[:1000]}...")
            image_line_b64 = image_line_b64.replace(image_src, replacestring)
            print(f"### DEBUG: created replace string for html: {image_line_b64[:1000]}...")
            text = text.replace(image_line, image_line_b64)
            print("### DEBUG: replaced html string")
    print("### DEBUG: processing.py finished processing of images, returning html to main.py ###")
    print("")
    del image_data
    del image_data_64
    del image_line_b64
    del images_b64
    del replacestring
    del soup
    gc.collect()
    return text

#provide_images(''' <p><img alt="ln5" src="../Images/ln5.png"/><br/></p>  ''', "D:\\Dokumente\\PycharmProjects\\ePubly\\assets\\konosuba.epub", (614, 885))
# text = text.replace("")
