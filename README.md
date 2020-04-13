# epubly
a shitty epub reader

it's an experiment

python 3.7.7
pywebview
ebooklib
bs4

it works by doing unnecessary stuff, processing the epub files from byte string to normal epub xhtml because I suck
at using that wonderful documented piece of code called ebooklib 

opened epub (not included) with 5 pictures à 600kb uses 1,4 GB RAM because why not

actually it's because I didn't want to serve the image files like a normal person per local webserver but as injected 
base64 strings directly inside the html file YES IT'S DUMB but it was a fun experiment haha

IT EVEN SCALES THE WINDOW AUTOMATICALLY wew

yeah, have fun with this...
