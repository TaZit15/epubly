import ebooklib
from ebooklib import epub
import webview
from processing import clean_html
from processing import provide_images
import ctypes

html = """
<html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>ePubly</title>
    </head>
    <body>
        <div class="button-container">
            <button class="choose-file" id="epub_button" onClick="choose_epub()">epub</button>
        </div>
        <div id="start">
        </div>
        <script>
            function loadEpub(ch1) {
                var container = document.getElementById('start')
                container.innerHTML = ch1.content
            }

            function choose_epub() {
                pywebview.api.choose_epub().then(loadEpub)
            }
            
        </script>
    </body>
</html>
"""


class Api:
    def __init__(self):
        print("### DEBUG: Api initialized ###")

    def choose_epub(self):
        print("### DEBUG: Window called function choose_epub() ###")
        file_types = ('EPUB (*.epub)', 'All files (*.*)')
        path = window.create_file_dialog(webview.OPEN_DIALOG, directory='', allow_multiple=False, save_filename='',
                                         file_types=file_types)
        content = {}
        book = epub.read_epub(str(path[0]))
        print("### DEBUG: starting indexing epub documents ###")
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                name = item.get_name()
                chapter_content = item.get_content()
                content[name] = str(chapter_content)
                print(f"{name}")
        print("### DEBUG: finished indexing epub documents ###")
        ch1 = {}

        res = next(iter(content))
        rawtext = str(content[res])
        print(f"### DEBUG: raw text: {rawtext[:1000]}...")
        print("###")
        print("### DEBUG: sending raw text to processing.py: clean_html() ###")
        cleantext = clean_html(rawtext)
        print("### DEBUG: retrieving cleaned text ###")
        print(cleantext[:1000])
        print("###")
        print("### DEBUG: sending cleaned text to processing.py: provide_images() ###")
        image_text = provide_images(cleantext, str(path[0]), window_size)
        print("### DEBUG: retrieving finalized text ###")
        print(image_text[:1000])
        print("###")
        ch1['content'] = image_text
        print("##### DEBUG: finished extracting and processing of ch1, return ch1 to html template #####")
        return ch1


if __name__ == '__main__':
    api = Api()
    user32 = ctypes.windll.user32
    user_x = user32.GetSystemMetrics(0)
    user_y = user32.GetSystemMetrics(1)
    scaled_x = int(user_x*0.32)
    scaled_y = int(user_y*0.82)
    window_size = (scaled_x, scaled_y)
    window = webview.create_window('ePubly', html=html, js_api=api, min_size=window_size, resizable=False, text_select=True)
    webview.start()
