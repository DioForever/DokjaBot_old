import json
from datetime import datetime
from discord.ext import tasks
import discord
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

last_chapters = {

}
content = []
# await bot.wait_until_ready()
print("DokjaBot activated")
with open('chapters_latest.txt', 'r') as f:
    for line in f:
        if line is not None:
            line_ = line.split('-')
            last_chapters[line_[0]] = float(line_[1])
        # Title Source  url  url_chapter r g b rHour rMinute rDay
manhwas = []

with open('chapters_listed', 'r') as r:
    for line in r:
        if line is not None:
            manhwas.append(line)

cmds = []
count = 0
for line in manhwas:
    line = line.split("  ")
    index = count
    cmds.append(line[0])


@bot.command()
async def m(ctx, arg):
    global release_list
    title = str(arg).lower()
    if cmds.__contains__(arg):
        # Now look into chapters and find it
        for manhwa in manhwas:
            manhwa = manhwa.split("  ")
            if manhwa[0] == arg:
                # Now we found the manhwa we wanted
                source = manhwa[2]
                if source == 'Reaper_Scans':
                    embed = \
                        getReaperScans(manhwa[1], manhwa[3], manhwa[4], int(manhwa[5]), int(manhwa[6]), int(manhwa[7]),
                                       int(manhwa[8]), int(manhwa[9]), int(manhwa[10]))[0]
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("We don't support this source")
    elif arg == "list":
        release_list = "\n"
        for line in manhwas:
            line = line.split("  ")
            release_list += f"{line[1]}: !m {line[0]}\n"
        embed = discord.Embed(title=f"List of Manhwas/Mangas",
                              description=f"The list of commands for \n " + "Manhwas and Mangas in system" + f"\n {release_list}",
                              color=discord.Color.from_rgb(246, 214, 4))
        await ctx.send(embed=embed)


@bot.command()
async def supl(ctx):
    datet = datetime.today().strftime("%Y%m%d")
    odpoved = req.get("https://skripta.ssps.cz/substitutions.php/?date=" + datet)
    print("https://skripta.ssps.cz/substitutions.php/?date=" + datet)
    data = json.loads(odpoved.content)

    for i in data["ChangesForClasses"]:
        if (i["Class"]["Abbrev"] == "1.B"):
            for j in i["CancelledLessons"]:
                predmet = j["Subject"]
                ucitel = j["ChgType2"]
                skupina = j["Group"]
                typ = j["ChgType1"]
                hodina = j["Hour"]
                messageToSend = f"1.B {predmet} {ucitel} {skupina} {typ} {hodina}. hodina"
                await ctx.send(messageToSend)


@bot.command()
async def m_subscribe_all(ctx):
    subscription_all = []
    with open('chapters_release_ping', 'r') as f:
        for line in f:
            subscription_all.append(line)
    # Now check if user is in the list

    await bot.wait_until_ready()
    channel = bot.get_channel(977231331199164466)
    await channel.send('Pinging {}'.format(ctx.author.mention))
    await channel.send('<@401845652541145089>')


@bot.command()
async def m_tbate(ctx):
    TBATE_Web = req.get("https://beginningafterend.com/?2022-05%3F2022-05-20")
    soupTBATE = bs(TBATE_Web.content, features="html.parser")
    date = datetime.today().strftime("%Y-%m-%d")

    chapterTBATE = soupTBATE.find("li", class_="su-post")
    a_text = chapterTBATE.find("a")

    chapter_number = 0
    for a in str(a_text).split():
        if a.__contains__("<"):
            for item in a.split('<'):
                if item.isdigit():
                    chapter_number = item

    url_chapter = "https://beginningafterend.com/manga/the-beginning-after-the-end-chapter-" + chapter_number + "/?" + date
    web_Chapter = req.get(url_chapter)
    soup_Chapter = bs(web_Chapter.content, features="html.parser")
    headers2 = soup_Chapter.find("div", class_="tickcounter")
    today_bool = False
    date_split = url_chapter.split('?')
    date_length = len(date_split)
    date1 = date_split[date_length - 1]

    message_finall = getTime(18, 0, 4)[0]
    countdown_end_bool = False

    if date1 == date:
        countdown_end_bool = True

    if headers2 is None and today_bool:
        message_release = ("Has been released")
    elif not (headers2 is None) and today_bool and not countdown_end_bool:
        message_release = ("Has not been translated yet or is on break")
    else:
        message_release = (f"Will be released in {message_finall}")

    embed = discord.Embed(title=f"The Beginning After The End", url="https://beginningafterend.com",
                          description=f"Chapter {chapter_number} \n " + message_release + "\n Link to chapter: " + url_chapter,
                          color=discord.Color.from_rgb(5, 77, 17))
    embed.set_image(url="https://digitalcrime.news/wp-content/uploads/2022/03/a-221.jpg")
    await ctx.send(embed=embed)


@bot.command()
async def m_fth(ctx):
    FFF_Web = req.get("https://manhuazone.com/manga/5-fff-class-tras-hero/")
    soupFFF = bs(FFF_Web.content, features="html.parser")
    chapterFFF = soupFFF.find("li", class_="wp-manga-chapter")
    a_text = chapterFFF.find("a")
    chapter_number = 0
    print(chapterFFF)
    last_release = chapterFFF.find("i")
    last_release = str(last_release).replace("<i>", "")
    last_release = str(last_release).replace("</i>", "")

    for a in str(a_text).split():

        if a.isdigit():
            chapter_number = a

    url_chapter = f"https://ww2.fff-classtrashero.com/manga/fff-class-trashero-chapter-{chapter_number}/"
    web_Chapter = req.get(url_chapter)
    soup_Chapter = bs(web_Chapter.content, features="html.parser")
    date_split = url_chapter.split('?')
    date_length = len(date_split)
    chapter_number = int(chapter_number) + 1
    message_release = (
        f"The Chapter {chapter_number} will be released in some time, \n this comic doesnÂ´t have specific \n time for releases \n it typically releases \n once 10-20 days a few chapters at once \n "
        f"Last chapter was released on {last_release}")
    chapter_number = int(chapter_number) - 1
    embed = discord.Embed(title=f"FFF-Class Trashero", url="https://manhuazone.com/manga/5-fff-class-tras-hero/",
                          description=f"Chapter {chapter_number} \n " + message_release + "\n Link to last chapter: " + url_chapter,
                          color=discord.Color.from_rgb(167, 14, 191))
    embed.set_image(url="https://i0.hdslb.com/bfs/comic-static/70c263ce2dffe3fdd94369955d0c2bc6cde0c70b.png@600w.jpg")
    await ctx.send(embed=embed)


@tasks.loop(seconds=60)  # repeat after every 10 seconds
async def myLoop():
    await bot.wait_until_ready()
    channel = bot.get_channel(977231331199164466)
    content = []
    subscription = []
    with open('chapters_latest.txt', 'r') as f:
        for line in f:
            content.append(line)

    with open('chapters_release_ping', 'r') as f:
        for line in f:
            subscription.append(line)
    content_new = []

    with open('chapters_listed', 'r') as r:
        for line in r:
            # Get the released chapter as Name-number_chapter
            line = line.split("  ")
            if line[2] == 'Reaper_Scans':
                number_current_chapter = \
                    float(getReaperScans(line[1], line[3], line[4], int(line[5]), int(line[6]), int(line[7]),
                                         int(line[8]), int(line[9]), int(line[10]))[1])
                if not last_chapters.keys().__contains__(line[1]):
                    print(last_chapters.keys(), line[1],'Not')
                    print(line[1]  + line[1],'Not')
                    last_chapter_number = number_current_chapter - 1
                    contains = False
                else:
                    last_chapter_number = last_chapters[line[1]]
                    print(last_chapter_number, line[1],'Yes')
                    contains = True
                if last_chapter_number < number_current_chapter:
                    print(last_chapter_number, line[1],'new')
                    print(number_current_chapter, line[1],'new')
                    if contains is True:
                        last_chapters[line[1]] = number_current_chapter
                        content_new.append(f"{line[1]}-{number_current_chapter}")
                    else:
                        content_new.append(f"{line[1]}-{number_current_chapter}")
                    embed = getReaperScansReleased(line[1], line[3], line[4], int(line[5]), int(line[6]), int(line[7]))
                    await channel.send(embed=embed)
                    await channel.send(f'Ping of The {line[1]} {number_current_chapter}: {subscription}',
                                       delete_after=3)
                with open('chapters_latest.txt', 'w') as wf:
                    # Check if there are some that have to be updated
                    for c in content:
                        for c_ in content_new:
                            cs = c.split('-')[0]
                            cs_ = c_.split('-')[0]
                            if cs_ == cs:
                                content.remove(c)

                    # Write it down
                    for c in content_new:
                        wf.write(c + " \n")
                    for c in content:
                        wf.write(c)

    # Save the last_chapters to the chapters_latest.txt file


def getTime(rHour, rMinute, rDay):
    date = datetime.today().strftime("%Y-%m-%d")
    temp = pd.Timestamp(date)
    day = temp.day_of_week
    # Released on Friday at 18:00 / 6PM
    release = 18
    hour = int(datetime.today().strftime("%H")) * 60 * 60
    min = int(datetime.today().strftime("%M")) * 60
    sec = int(datetime.today().strftime("%S"))
    time_sec = hour + min + sec + day * 24 * 60 * 60
    # Time in seconds until release
    countdown_left = int((rHour * 60 * 60 + rMinute * 60 - time_sec) / 60 + rDay * 24 * 60)
    negative = True
    if countdown_left > 0:
        negative = False

    if countdown_left <= 0:
        countdown_left = countdown_left + 7 * 24 * 60
    if abs(countdown_left) > (24 * 60):
        days_r = int(countdown_left / 60 / 24)
        countdown_left = countdown_left - days_r * 24 * 60
    else:
        days_r = 0
    if abs(countdown_left) > 60:
        hour_r = int(countdown_left / 60)
        countdown_left = countdown_left - hour_r * 60
    else:
        hour_r = 0
    min_r = countdown_left

    message_finall = f"{days_r} days  {hour_r} hours {min_r} minutes"

    return message_finall, negative


def getReaperScans(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    web = req.get(url=urlbasic)
    chapter_number = 0
    soup = bs(web.content, features="html.parser")
    chapter = soup.find("li", class_="wp-manga-chapter")
    thumbnail_text = str(chapter.find("img", class_="thumb"))
    thumbnail_text = thumbnail_text.split('"')
    url_thumbnail = thumbnail_text[len(thumbnail_text) - 2]
    # Now I have the thumbnail

    # Now I need the chapter number
    chapter_text = str(chapter.find("p", class_="chapter-manhwa-title")).split()
    chapter_number = float(str(chapter_text[2]).split('<')[0])
    # Now I have the number as well

    if chapter_number == round(chapter_number,0):
        urlchapter = f"{urlchapter}{int(chapter_number)}/"
    else:
        moment_number = str(chapter_number).replace('.','-')
        urlchapter = f"{urlchapter}{moment_number}/"

    # Now get the time of release and if it already was released today or not
    time_left = getTime(rHour, rMin, rDay)[0]
    released_today = False

    second_chapter = soup.find_all("span", class_="chapter-release-date")
    date_second_chapter = str(second_chapter[1]).replace("</i> </span>", "")
    date_second_chapter = str(date_second_chapter).split('>')
    date_second_chapter = date_second_chapter[2]
    digit = (date_second_chapter.split())
    digit = (digit[1])
    digit = digit.replace(",", "")
    digit = int(digit)
    digit += 7
    word = (date_second_chapter.split())[1]
    date_last_chapter = date_second_chapter.replace(word, str(digit))
    date_now = datetime.date(datetime.today())
    date_now = date_now.strftime('%b %d, %Y')
    if date_now == date_second_chapter:
        released_today = True

    if getTime(rHour, rMin, rDay)[1] is True and released_today is True:
        message_release = f"The chapter is being translated or is on a break"
    else:
        m_chapter_number = int(chapter_number)
        m_chapter_number += 1
        message_release = f"The Chapter {m_chapter_number} will be released in {getTime(rHour, rMin, rDay)[0]}"
    # Now display it

    embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                          description=f"The Chapter {chapter_number} \n " + message_release + f"\n Link to latest chapter: {urlchapter}",
                          color=discord.Color.from_rgb(r1, g, b))
    embed.set_image(url=f"{url_thumbnail}")
    return embed, chapter_number


def getReaperScansReleased(Title, urlbasic, urlchapter, r1, g, b):
    subscription = []
    with open('chapters_release_ping', 'r') as f:
        for line in f:
            subscription.append(line)
    web = req.get(url=urlbasic)
    chapter_number = float(0)
    soup = bs(web.content, features="html.parser")
    chapter = soup.find("li", class_="wp-manga-chapter")
    thumbnail_text = str(chapter.find("img", class_="thumb"))
    thumbnail_text = thumbnail_text.split('"')
    url_thumbnail = thumbnail_text[len(thumbnail_text) - 2]
    # Now I have the thumbnail

    # Now I need the chapter number
    chapter_text = str(chapter.find("p", class_="chapter-manhwa-title")).split()
    chapter_number = float(str(chapter_text[2]).split('<')[0])
    # Now I have the number as well

    if chapter_number == round(chapter_number,0):
        urlchapter = f"{urlchapter}{int(chapter_number)}/"
    else:
        moment_number = str(chapter_number).replace('.','-')
        urlchapter = f"{urlchapter}{moment_number}/"

    # Now get the time of release and if it already was released today or not

    chapters_released = ""
    if not last_chapters.__contains__(Title):
        last_chapter_number = chapter_number - 1
    else:
        last_chapter_number = last_chapters[Title]
    if last_chapter_number - chapter_number != -1:
        # It has more than 1 released chapter at once, so it was mass release or somethin like that
        for number in range(int(last_chapters[Title]), int(chapter_number) + 1):
            chapters_released += str(number) + ", "
        message_release = f"The Chapters {chapters_released} was released!"
    else:
        message_release = f"The Chapter {chapters_released} was released!"
    # Now display it

    if len(chapters_released) > 1:
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"{message_release} \n Link to latest chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")
    else:
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"{message_release} \n Link to the chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")
    return embed


# <@401845652541145089>


myLoop.start()
bot.run('ODg3Mzc4NzM3MTQ5MTQ1MTI4.GKxdP8.yh1GiPrn7OZdr6smO4s3TkeLn_RIFdlcI-Ll68')
