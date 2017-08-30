#coding:utf-8  
import sys,os  
from PIL import Image, ImageDraw ,ImageEnhance
import pytesseract
  
#二值判斷,如果確認是噪聲,用改點的上面一個點的灰度進行替換  
#該函數也可以改成RGB判斷的,具體看需求如何  
def getPixel(image, x, y, G, N):  
    L = image.getpixel((x, y))  
    if  L > G:
        L = True  
    else:  
        L = False  
  
    nearDots = 0  
    if  L == (image.getpixel((x - 1, y - 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x - 1, y)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x - 1, y + 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x, y - 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x, y + 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x + 1, y - 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x + 1, y)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x + 1, y + 1)) > G):  
        nearDots +=  1  
  
    if  nearDots < N:  
        return image.getpixel((x,y - 1))  
    else:  
        return None   
  
# 降噪   
# 根據一個點A的RGB值，與周圍的8個點的RBG值比較，設定一個值N（0 <N <8），當A的RGB值與周圍8個點的RGB相等數小於N時，此點為噪點   
# G: Integer 圖像二值化閥值   
# N: Integer 降噪率 0 <N <8   
# Z: Integer 降噪次數   
# 輸出   
# 0：降噪成功   
# 1：降噪失敗   
def clearNoise(image, G, N, Z):  
    draw = ImageDraw.Draw(image)  
  
    for i in range(0, Z):  
        for x in range(1, image.size[0] - 1):  
            for y in range(1, image.size[1] - 1):  
                color = getPixel(image, x, y, G, N)  
                if  color !=  None :  
                    draw.point((x, y), color)  

# Enhance
def enhance(image):
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(3.0)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(10.0)
    return image
  
#測試代碼  
def main():  
    #打開圖片  
    image = Image.open("./pic/ImageCode1.gif")
  
    #將圖片轉換成灰度圖片  
    image = image.convert("L")

    #第一次 Enhance
    image = enhance(image)
  
    #第一次去噪,G = 50,N = 4,Z = 4  
    clearNoise(image, 50 , 3 , 3)  
  

    #第二次 Enhance
    image = enhance(image)
  
    #第二次去噪,G = 50,N = 4,Z = 4  
    clearNoise(image, 50 , 4 , 4)  
  
    #保存圖片  
    # image.save( "./result/result.png" )  

    image.show()
    print(pytesseract.image_to_string(image))
  

if  __name__ ==  '__main__' :  
    main()  