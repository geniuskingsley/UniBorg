import os

from datetime import datetime

from pytz import timezone

from PIL import Image, ImageDraw, ImageFont

from pySmartDL import SmartDL

from telethon.tl import functions

from uniborg.util import admin_cmd

import asyncio

import shutil

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
VERY_PIC = "https://pes2020.sirv.com/mn.jpg" 

@borg.on(admin_cmd(pattern="autopp"))

async def autopic(event):

    downloaded_file_name = "./DOWNLOADS/original_pic.png"

    downloader = SmartDL(VERY_PIC, downloaded_file_name, progress_bar=False)

    downloader.start(blocking=False)

    photo = "photo_pfp.png"

    while not downloader.isFinished():

        place_holder = None

    counter = -5

    while True:

        shutil.copy(downloaded_file_name, photo)

        im = Image.open(photo)

        file_test = im.save(photo, "PNG")

        now_utc = datetime.now(timezone('UTC'))

        now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
     

        current_time = now_asia.strftime("°°°°°°°°°°°°°°°\n Time: %I:%M:%p\n Date: %d-%m-%y\n°°°°°°°°°°°°°°°")


        img = Image.open(photo)

        drawn_text = ImageDraw.Draw(img)

        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)

        drawn_text.text((200,350), current_time, font=fnt, fill=(19, 157, 232))

        img.save(photo)

        file = await event.client.upload_file(photo)  # pylint:disable=E0602

        try:

            await event.client(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602

                file

            ))

            os.remove(photo)

            counter -= 5

            await asyncio.sleep(65)

        except:

            return
