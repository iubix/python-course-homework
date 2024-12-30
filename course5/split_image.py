from PIL import Image
import pathlib
import settings
import random

BASE_PATH = pathlib.Path(__file__).parent

#分割图片
def splitImage(image_path, rownum, colnum):

    image = Image.open(image_path)
    image_width, image_height = image.size

    if rownum <= image_height and colnum <= image_width:

        width = image_width // colnum
        height = image_height // rownum
        cnt = 0
        for i in range(rownum):
            for j in range(colnum):
                box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                region = image.crop(box)
                region.save(BASE_PATH / 'splitImage' / f"icon{cnt}.png")
                cnt += 1

    else:
        print("Invalid rownum or colnum")



#构建图片布局
def built_map():
    
    list_img = list(range(0, settings.MAP_TOTAL))

    random.shuffle(list_img)
    
    return list_img


if __name__ == '__main__':

    splitImage(r"Python_course\course5\111159609_p0.jpg", 2, 2)