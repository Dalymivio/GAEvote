# PIL module

from PIL import Image, ImageDraw, ImageFont

import StringIO
import os

def create(width, colour, text, ratio):
    
    path = os.path.join(os.path.dirname(__file__), 'assets/Nikodecs24.pil')
    font = ImageFont.load(path)
    
    textWidth, textHeight = font.getsize(text)
    
    fill = (0, 0, colour, 255)
    
    image = Image.new('RGBA', (width+200, textHeight), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.text((width - textWidth, 0), text, font=font, fill='black')
    draw.rectangle([(width, 0), (width+(ratio*2), textHeight)], fill=fill, outline=None)
    
    small_image = image.resize((image.size[0]/2, image.size[1]/2), Image.ANTIALIAS)

    s = StringIO.StringIO()
    small_image.save(s, 'PNG')
    
    return s.getvalue()

def width(text):
    path = os.path.join(os.path.dirname(__file__), 'assets/Nikodecs24.pil')
    font = ImageFont.load(path)
    
    return font.getsize(text)[0]