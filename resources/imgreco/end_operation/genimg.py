import numpy as np
from util import cvimage as Image, ImageFont


def fuck(fontname, fontsize, text, savefile):
    font = ImageFont.truetype(fontname, int(fontsize))
    mask = font.getmask(text, "L")
    img = Image.new("L", mask.size)
    img.putdata(mask)

    lut = np.zeros(256, dtype=np.uint8)
    lut[127:] = 1
    maskim = img.point(lut, "1")

    bbox = maskim.getbbox()
    img = img.crop(bbox)
    img.save(savefile)


if __name__ == "__main__":
    names = (
        "Regular Drops",
        "Extra Drops",
        "Special Drops",
        "Lucky Drops",
        "First Clear",
        "Reward",
        "Sanity refunded",
        "1.2 x EXP & LMD",
        "1.0 x EXP & LMD",
    )
    for name in names:
        fuck(r"D:\projects\akimgreco\NotoSansCJKsc-Medium.otf", 25, name, name + ".png")
