import sys
from PIL import Image, ImageDraw

BORDER = {"light": (208, 215, 222, 255), "dark": (48, 54, 61, 255)}


def frame(src, dst, scheme, radius=28, width=None, height=None):
    im = Image.open(src).convert("RGBA")
    if width:
        height = height or round(im.height * width / im.width)
        im = im.resize((width, height), Image.LANCZOS)
    w, h = im.size
    mask = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * 4 - 1, h * 4 - 1), radius * 4, fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    line = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(line).rounded_rectangle((0, 0, w * 4 - 1, h * 4 - 1), radius * 4, outline=255, width=6)
    line = line.resize((w, h), Image.LANCZOS)
    out.paste(Image.new("RGBA", (w, h), BORDER[scheme]), (0, 0), line)
    out.save(dst, optimize=True)


if __name__ == "__main__":
    frame(sys.argv[1], sys.argv[2], sys.argv[3])
