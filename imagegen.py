# PIL module

from PIL import Image

import cStringIO

def test(colour):
    
    image = Image.new("RGB", (100, 20), colour)
    
    """Since we cannot write to FS using a stringbuffer instead""" 
    s = cStringIO.StringIO()
    image.save(s, 'PNG')
    
    return s.getvalue()