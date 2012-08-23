# PIL module

from PIL import Image, ImageDraw, ImageFont

import StringIO
import os

def test(colour):
    
    image = Image.new("RGB", (100, 20), colour)
    
    """Since we cannot write to FS using a stringbuffer instead""" 
    s = StringIO.StringIO()
    image.save(s, 'PNG')
    
    return s.getvalue()

def create(width, colour, text, ratio):
    
    path = os.path.join(os.path.dirname(__file__), 'assets/Deja.pil')
    font = ImageFont.load(path)
    
    textWidth, textHeight = font.getsize(text)
    
    fill = (0, 0, colour, 255)
    
    image = Image.new('RGBA', (width+100, textHeight), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.text((width - textWidth, 0), text, font=font, fill='black')
    draw.rectangle([(width, 0), (width+ratio, textHeight)], fill=fill, outline=None)

    s = StringIO.StringIO()
    image.save(s, 'PNG')
    
    return s.getvalue()

def width(text):
    path = os.path.join(os.path.dirname(__file__), 'assets/Deja.pil')
    font = ImageFont.load(path)
    
    return font.getsize(text)[0]