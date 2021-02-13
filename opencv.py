import cv2 as cv
import discord
import random as ra

def resize(img, width=500):
    const = img.shape[0]/img.shape[1]
    height = int(const * width)
    dim = (width, height)
    return cv.resize(img, dim, interpolation=cv.INTER_CUBIC)

async def url_to_image(Member : discord.Member):
    filename = f"{ra.randint(0, 1000)}.jpg"
    await Member.avatar_url.save(filename)
    file = discord.File(fp=filename)
    return (file, filename)

async def grey(Member : discord.member):
    file, file_name = await url_to_image(Member)
    img = cv.imread(file_name)
    img = resize(img)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imwrite(file_name, img)
    file = discord.File(fp=file_name)
    return(file, file_name)