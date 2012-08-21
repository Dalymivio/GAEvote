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

def create(colour, text):
    
    path = os.path.join(os.path.dirname(__file__), 'assets/helvR12.pil')
    font = ImageFont.load(path)
    
    textWidth, textHeight = font.getsize(text)
    
    image = Image.new('RGBA', (textWidth+105, textHeight), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0,0), (textWidth+5, 20)], fill=None, outline='black')
    draw.text((0,0), text, font=font, fill='black')
    s = StringIO.StringIO()
    image.save(s, 'PNG')
    
    return s.getvalue()