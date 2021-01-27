from PIL import Image, ImageDraw

# 取得座標(x, y)附近的像素值
def getpixel(image, x, y):
    pixel_list = []

    # 取得3*3的像素值
    for i in range(-1, 2):
        for j in range(-1, 2):
            pixel = image.getpixel((x + j ,y + i))
            pixel_list.append(pixel)
    
    return(pixel_list)

# 將黑白圖片做Complement
def Complement(BinaryImage):
    width, height = BinaryImage.size
    ComplementImage = Image.new(BinaryImage.mode, (width, height) , (0))
    draw = ImageDraw.Draw(ComplementImage)

    for x in range(0, width):
        for y in range(0, height):
            new_pixel = 255 - BinaryImage.getpixel((x, y))          # 將像素值做Complement
            draw.point((x, y), fill = (new_pixel))                  # 將像素值填進新圖中

    return ComplementImage

# 設定起始的地點
def set_Initial_Point(BinaryImage, Initial_Point, Mode):
    Background_color = 255 - Mode
    width, height = BinaryImage.size
    InitialPointImage = Image.new(BinaryImage.mode, (width, height) , (Background_color))
    draw = ImageDraw.Draw(InitialPointImage)
    draw.point(Initial_Point, fill = (Mode))                        # 設定初始點的顏色

    return InitialPointImage

# 將OldImage做Dilation後，再與ComplementImage做intersection，即可得到新圖
def fill_region(OldImage, ComplementImage, Mode):
    Background_color = 255 - Mode
    width, height = OldImage.size
    FillRegionImage = Image.new(OldImage.mode, (width, height) , (Background_color))
    draw = ImageDraw.Draw(FillRegionImage)

    # Square Structuring Mask(dot is the center)
    Mask = [0, Mode, 0,
            Mode, Mode, Mode,
            0, Mode, 0]

    Mask_index = [1, 3, 4, 5, 7]                                    # 只取Mask中有用的位置

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            pixel_list = getpixel(OldImage, x, y)                   # 取得黑白圖片中座標(x,y)附近的像素值

            # 將pixel_list與Mask做Dilation
            for index in Mask_index:
                # 如果Dilation of pixel_list by Mask
                if pixel_list[index] == Mask[index]:
                    draw.point((x, y), fill = (Mode))               # 將像素值填進新圖中

            # 做intersection
            if ((FillRegionImage.getpixel((x, y)) != Background_color) and (ComplementImage.getpixel((x, y)) != Background_color)):
                draw.point((x, y), fill = (Mode))
            else:
                draw.point((x, y), fill = (Background_color))

    return FillRegionImage

# 當產生的新圖與之前一樣時就停止
def terminate(OldImage, NewImage):
    width, height = OldImage.size

    for x in range(0, width):
        for y in range(0, height):
            if (OldImage.getpixel((x, y)) != NewImage.getpixel((x, y))):
                return False

    return True

# 將黑白圖片與FillRegionImage做聯集
def union(BinaryImage, FillRegionImage, Mode):
    Background_color = 255 - Mode
    width, height = BinaryImage.size
    RegionFillingImage = Image.new(BinaryImage.mode, (width, height) , (Background_color))
    draw = ImageDraw.Draw(RegionFillingImage)

    for x in range(0, width):
        for y in range(0, height):
            # 做union
            if ((BinaryImage.getpixel((x, y)) != Background_color) or (FillRegionImage.getpixel((x, y)) != Background_color)):
                draw.point((x, y), fill = (Mode))

    return RegionFillingImage

# 做Region_Filling
def Region_Filling(BinaryImage, ComplementImage, Initial_Point, Mode):
    InitialPointImage = set_Initial_Point(BinaryImage, Initial_Point, Mode)         # 設定起始的地點
    OldImage = InitialPointImage

    # 創建FillRegion的圖
    FillRegionImage = fill_region(OldImage, ComplementImage, Mode)                  # 將OldImage做Dilation後，再與ComplementImage做intersection，即可得到新圖
    # 當產生的新圖與之前一樣時就停止
    while (not terminate(OldImage, FillRegionImage)):
        OldImage = FillRegionImage
        FillRegionImage = fill_region(OldImage, ComplementImage, Mode)              # 將OldImage做Dilation後，再與ComplementImage做intersection，即可得到新圖
        FillRegionImage.save("FillRegionImage.jpg")

    RegionFillingImage = union(BinaryImage, FillRegionImage, Mode)                  # 將黑白圖片與FillRegionImage做聯集

    return RegionFillingImage

def main():
    OriginalImage = Image.open('Original_fill_wirte.jpg')               # 載入原圖
    Initial_Point = (50, 50)                                            # 自訂初始點
    Mode = 255                                                          # 設定要填成黑或白的模式，黑為0，白為255

    # OriginalImage = Image.open('Original_fill_black.jpg')               # 載入原圖
    # Initial_Point = (250, 150)                                          # 自訂初始點
    # Mode = 0                                                            # 設定要填成黑或白的模式，黑為0，白為255

    BinaryImage = OriginalImage.convert('1')                            # 將原圖轉成黑白圖片

    # 創建Complement的圖
    ComplementImage = Complement(BinaryImage)                           # 將黑白圖片做Complement
    ComplementImage.save("ComplementImage.jpg")

    # 創建Region_Filling的圖
    RegionFillingImage = Region_Filling(BinaryImage, ComplementImage, Initial_Point, Mode)    # 做Region_Filling
    RegionFillingImage.save("RegionFillingImage.jpg")

if __name__ == "__main__":
    main()