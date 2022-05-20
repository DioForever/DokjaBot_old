from calendar import weekday

import ctx as ctx
import day as day
import requests as r
from discord.ext import commands
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd
import re

bot = commands.Bot(command_prefix="!")
''''
@bot.command()
async def supl(ctx):
    datet = datetime.today().strftime("%Y%m%d")
    odpoved = r.get("https://skripta.ssps.cz/substitutions.php/?date=" + datet)

    data = json.loads(odpoved.content)

    for i in data["ChangesForClasses"]:
        if (i["Class"]["Abbrev"] == "1.B"):
            for j in i ["CancelledLessons"]:
                predmet = j["Subject"]
                ucitel = j["ChgType2"]
                skupina = j["Group"]
                typ = j["ChgType1"]
                hodina = j["Hour"]
                messageToSend = f"1.B {predmet} {ucitel} {skupina} {typ} {hodina}. hodina"
                await ctx.send(messageToSend)
'''
'''@bot.command()
async def m_tbate(ctx):
'''


@bot.command()
async def m_tbate(ctx):
    TBATE_Web = r.get("https://beginningafterend.com/?2022-05%3F2022-05-20")
    soupTBATE = bs(TBATE_Web.content)
    released = False
    date = datetime.today().strftime("%Y-%m-%d")
    # print(soupTBATE.prettify())
    # chapterTBATE = soupTBATE.findAll(string=re.compile("The-Begin"))
    # print('SPACE U KNOW')
    chapterTBATE = soupTBATE.find("li", class_="su-post")
    a_text = chapterTBATE.find("a")
    # print(a_text)
    # a_text_splited = a_Text.split("")

    chapter_number = 0
    for a in str(a_text).split():
        # print(a)
        if a.__contains__("<"):
            for item in a.split('<'):
                if item.isdigit():
                    chapter_number = item
                # print("second" + item)
    # Check if player has a countdown or not
    # https://beginningafterend.com/manga/the-beginning-after-the-end-chapter-146/?2022-05-20

    message_chapter = (">>> The Beginning After The End - Chapter " + chapter_number)
    message_release = ""

    url_chapter = "https://beginningafterend.com/manga/the-beginning-after-the-end-chapter-" + chapter_number + "/?" + date
    # print(url_chapter)
    web_Chapter = r.get(url_chapter)
    soup_Chapter = bs(web_Chapter.content)
    headers2 = soup_Chapter.find("div", class_="tickcounter")
    # print(headers2)
    countdown_left = 0
    today_bool = False
    date_split = url_chapter.split('?')
    date_length = len(date_split)
    date1 = date_split[date_length - 1]

    temp = pd.Timestamp(date)
    day = temp.day_of_week
    # Released on Friday at 18:00 / 6PM
    release = 18
    hour = int(datetime.today().strftime("%H")) * 60 * 60
    min = int(datetime.today().strftime("%M")) * 60
    sec = int(datetime.today().strftime("%S"))
    time_sec = hour + min + sec + day * 24 * 60 * 60
    # Time in seconds until release
    countdown_left = int((18 * 60 * 60 - time_sec) / 60 + 4 * 24 * 60)
    print(countdown_left)
    # if (countdown_left <= 0):
    # countdown_left = countdown_left + (2 * 24 * 60 + (8 * 24 * 60))
    if (countdown_left <= 0):
        countdown_left = countdown_left + 7 * 24 * 60
    print(countdown_left)
    if abs(countdown_left) > (24 * 60):
        days_r = int(countdown_left / 60 / 24)
        countdown_left = countdown_left - days_r*24*60
    else:
        days_r = 0
    print(countdown_left)
    if abs(countdown_left) > 60:
        hour_r = int(countdown_left/60)
        countdown_left = countdown_left - hour_r*60
    else:
        hour_r = 0
    min_r = countdown_left
    print(countdown_left)

    message_finall = f"{days_r} days  {hour_r} hours {min_r} minutes"

    countdown_end_bool = False
    if countdown_left <= 0:
        countdown_end_bool = True

    if date1 == date:
        countdown_end_bool = True

    if headers2 is None and today_bool:
        released = True
        message_finall = ("Has been released")
    elif not (headers2 is None) and today_bool and not countdown_end_bool:
        released = True
        message_finall = ("Has not been translated yet or is on break")

    '''else:
        temp = pd.Timestamp(date)
        day = temp.day_of_week
        # Released on Friday at 18:00 / 6PM
        release = 18
        hour = int(datetime.today().strftime("%H")) * 60 * 60
        min = int(datetime.today().strftime("%M")) * 60
        sec = int(datetime.today().strftime("%S"))
        time_sec = hour + min + sec + day*24*60*60
        countdown_left = int((18 * 60 * 60 - time_sec) / 60 + 4*24*60)
        #print(countdown_left)'''

    # It does not have a countdown -> meaning: its been released

    '''    if released:
        message_release = ("Has been released")
    else:
        message_release = (f"Will be released in {countdown_left} minutes")
    message_finall = message_chapter + "\n" + message_release + " \n" + "Link to chapter: "+url_chapter'''
    # await ctx.send("The Beginning After The End - Chapter "+chapter_number)
    # print(chapterTBATE)

    await ctx.send(message_finall)


bot.run('ODg3Mzc4NzM3MTQ5MTQ1MTI4.GKxdP8.yh1GiPrn7OZdr6smO4s3TkeLn_RIFdlcI-Ll68')
