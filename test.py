try:
    import Image
except ImportError:
    from PIL import Image, ImageEnhance

from numpy import * 
import pytesseract

def initTable(threshold=140):
  table = []
  for i in range(256):
    if i < threshold:
         table.append(0)
    else:
         table.append(1)

  return table


im = Image.open('result.png')
im = im.convert('L')

enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(3.0)
enhancer = ImageEnhance.Brightness(im)
im = enhancer.enhance(10.0)


binaryImage = im.point(initTable(), '1')
binaryImage.show()


print(pytesseract.image_to_string(im)) 