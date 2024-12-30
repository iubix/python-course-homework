from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent)

BASE_PATH = pathlib.Path(__file__).parent

def get_valid_code():
    
    image_obj = Image.new('RGB', (255, 35), (230, 245, 250))
    image_draw = ImageDraw.Draw(image_obj)
    image_font = ImageFont.truetype(str(BASE_PATH / 'font.ttf'), size = 30)
    
    code = ''
    for i in range(6):
        #大写字母,小写字母,数字三种
        image_alpha = chr(random.randint(97, 122))
        image_Alpha = chr(random.randint(65, 90))
        image_digit = str(random.randint(0, 9))
        font_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        random_code = random.choice([image_alpha, image_Alpha, image_digit])
        
        image_draw.text(
            (i*30 + 40, 2), 
            random_code, 
            font = image_font, 
            fill = font_color
        )
        code += random_code

    image_obj.save(BASE_PATH / 'validation.png')
    

if __name__ == '__main__':
    get_valid_code()
    