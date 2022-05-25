import json
from datetime import datetime
from discord.ext import tasks
import discord
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

content = []
# await bot.wait_until_ready()
print("DokjaBot activated")

count = 0


@bot.command()
async def m(ctx, *args):
    cmds = []
    manhwas = []
    id_guild = ctx.message.guild.id
    with open('channel_listed.txt', 'r') as r:
        for line in r:
            if line is not None:
                id_line = (line.split("  ")[0])
                if str(id_line) == str(id_guild):
                    manhwas.append(line)
    for line in manhwas:
        line = line.split("  ")
        cmds.append(line[2])


    if cmds.__contains__(args[0]):
        # Now look into chapters and find it
        # Now look into chapters and find it
        for manhwa in manhwas:
            manhwa = manhwa.split("  ")
            if manhwa[2] == args[0]:
                # Now we found the manhwa we wanted
                source = manhwa[4].replace(" ", "")
                if source == 'Reaper_Scans':
                    embed = \
                        getReaperScans(manhwa[3], manhwa[5], manhwa[6], int(manhwa[7]), int(manhwa[8]), int(manhwa[9]),
                                       int(manhwa[10]), int(manhwa[11]), int(manhwa[12]))[0]
                    await ctx.send(embed=embed)
                elif source == 'MangaClash':
                    embed = \
                        getMangaClash(manhwa[3], manhwa[5], manhwa[6], int(manhwa[7]), int(manhwa[8]), int(manhwa[9]),
                                      int(manhwa[10]), int(manhwa[11]), int(manhwa[12]))[0]
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("We don't support this source")
    elif args[0] == "list":
        release_list = "\n"
        for line in manhwas:
            line = line.split("  ")
            release_list += f"{line[1]}: !m {line[0]}\n"
        embed = discord.Embed(title=f"List of Manhwas/Mangas",
                              description=f"The list of commands for \n " + "Manhwas and Mangas in system" + f"\n {release_list}",
                              color=discord.Color.from_rgb(246, 214, 4))
        await ctx.send(embed=embed)
    elif args[0] == "test":
        '''embed = getMangaClashReleased("The Beginning After The End","https://mangaclash.com/manga/the-beginning-after-the-end/","https://mangaclash.com/manga/the-beginning-after-the-end/chapter-", 0,0,0)[0]
        await ctx.send(embed = embed)'''
    elif args[0] == "listen":
        if args[1] == "add":
            #  0     1      2               3                       4                       5                                                           6                                               7  8  9  10  11 12  = 13
            # listen add after_fall The_World_After_the_Fall  Reaper_Scans  https://reaperscans.com/series/the-world-after-the-fall/  https://reaperscans.com/series/the-world-after-the-fall/chapter-  0  0  0  18  0  6
            if len(args) == 13:
                id_guild = ctx.message.guild.id
                id_channel = ctx.message.channel.id
                # await ctx.send(str(id_channel)+" "+str(id_guild))
                basic_url_used = []
                chapter_url_used = []
                args_ = []
                cmd = str(args[2])
                args_.append(args[2])
                title = str(args[3]).split("_")
                title_ = ''
                for word in title:
                    title_ += f'{word} '
                args_.append(title_)
                args_.append(args[4])
                args_.append(args[5])
                args_.append(args[6])
                args_.append(args[7])
                args_.append(args[8])
                args_.append(args[9])
                args_.append(args[10])
                args_.append(args[11])
                args_.append(args[12])
                channel_listed = []
                cmds_ = []
                with open('channel_listed.txt', 'r') as r:
                    for line in r:
                        if line is not None:
                            channel_listed.append(line.replace('\n', ''))
                            url_basic_line = line.split("  ")

                            cmd_ = line.split(" ")
                            cmd_ = cmd_[4]
                            basic_url_used.append(url_basic_line[6])
                            chapter_url_used.append(url_basic_line[7])
                            cmds_.append(cmd_)
                if not (cmds_.__contains__(cmd)):
                    if not (basic_url_used.__contains__(args_[3])):
                        if not (chapter_url_used.__contains__(args_[4])):
                            # Now we need to check just to write it to the file
                            new_listed = f'{id_guild}  {id_channel}  {args_[0]}  {args_[1]}  {args_[2]}  {args_[3]}  {args_[4]}  {args_[5]}  {args_[6]}  {args_[7]}  {args_[8]}  {args_[9]}  {args_[10]}'
                            channel_listed.append(new_listed)
                            with open('channel_listed.txt', 'w') as wr:
                                for new in channel_listed:
                                    wr.write(new + " \n")
                            await  ctx.send(f'The command {cmd} with title {title_} has been added to bookmarked')
                        else:
                            await  ctx.send(
                                "The chapter link you wanted to use is already in use, please don't duplicate")
                    else:
                        await  ctx.send("The chapter link you wanted to use is already in use, please don't duplicate")
                else:
                    await  ctx.send('The command you wanted to use is already in use')
            else:
                await ctx.send('You missed something')
    else:
        await  ctx.send('Unknown command!')


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


@tasks.loop(seconds=60)
async def chapterReleaseCheck():
    await bot.wait_until_ready()
    # I need to get the chapters latest from the server.latest
    chapters_released = {}
    with open('server_latest.txt', 'r') as r_sl:
        if r_sl is not None:
            for line in r_sl:
                line = line.split("-")
                id_channel = line[0]
                name_number = f'{line[1]}-{line[2]}'
                chapters_released.setdefault(id_channel, name_number)

    # Now I need the channel_listed and check every one of them
    with open('channel_listed.txt', 'r') as r_cl:
        if r_cl is not None:
            for line in r_cl:
                line = line.split("  ")
                id_guild = line[0]
                id_channel = line[1]
                title = line[3]
                source = line[4].replace(" ", "")
                url_basic = line[5]
                url_chapter = line[6]
                r = line[7]
                g = line[8]
                b = line[9]
                # Now I need to check the source and according to that I need to send the embed
                if source == "Reaper_Scans":
                    getReaper = getReaperScansReleased(title, url_basic, url_chapter, int(r), int(g), int(b),
                                                       id_channel, id_guild)
                    if getReaper[0]:
                        embed = getReaper[1]
                        channel = bot.get_channel(int(id_channel))
                        await channel.send(embed=embed)


'''@tasks.loop(seconds=60)  # repeat after every 10 seconds
async def myLoop():
    await bot.wait_until_ready()
    channel = bot.get_channel(977231331199164466)

    with open('server_latest.txt', 'r') as f:
        for line in f:
            if line is not None:
                line_ = line.split('-')
                last_chapters.setdefault(line_[1], line_[2])
            # Title Source  url  url_chapter r g b rHour rMinute rDay
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
                    last_chapter_number = number_current_chapter - 1
                    contains = False
                else:
                    last_chapter_number = last_chapters[line[1]]
                    contains = True
                last_chapter_number = float(last_chapter_number)
                if (last_chapter_number) < number_current_chapter:
                    if contains is True:
                        last_chapters[line[1]] = number_current_chapter
                        content_new.append(f"{line[1]}-{number_current_chapter}")
                    else:
                        content_new.append(f"{line[1]}-{number_current_chapter}")
                    embed = getReaperScansReleased(line[1], line[3], line[4], int(line[5]), int(line[6]), int(line[7]))
                    await channel.send(embed=embed)
                    await channel.send(f'Ping of The {line[1]} {number_current_chapter}: {subscription}',
                                       delete_after=3)
            elif line[2] == 'MangaClash':
                number_current_chapter = float(
                    getMangaClashReleased(line[1], line[3], line[4], int(line[5]), int(line[6]), int(line[7]))[1])
                # number_last_chapter = float(getMangaClashReleased(line[1], line[3], line[4], int(line[5]), int(line[6]), int(line[7]))[2])
                if not last_chapters.keys().__contains__(line[1]):
                    number_last_chapter = number_current_chapter - 1
                    contains = False
                else:
                    number_last_chapter = float(str(last_chapters[line[1]]).split(" ")[0])
                    contains = True
                if number_last_chapter < number_current_chapter:
                    # New chapter was released!
                    if not last_chapters.keys().__contains__(line[1]):
                        last_chapter_number = number_current_chapter - 1
                        contains = False
                    else:
                        last_chapter_number = last_chapters[line[1]]
                        contains = True
                    if contains is True:
                        last_chapters[line[1]] = number_current_chapter
                        content_new.append(f"{line[1]}-{number_current_chapter}")
                    else:
                        content_new.append(f"{line[1]}-{number_current_chapter}")
                    embed = getMangaClashReleased(line[1], line[3], line[4], int(line[5]), int(line[6]),
                                                   int(line[7]))[0]
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

    # Save the last_chapters to the chapters_latest.txt file'''


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


# Reaper Scans

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

    if chapter_number == round(chapter_number, 0):
        urlchapter = f"{urlchapter}{int(chapter_number)}/"
    else:
        moment_number = str(chapter_number).replace('.', '-')
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
    if digit.isalpha():
        d = datetime.date(datetime.today())
        d = d.strftime('%d')
        digit = int(d)
    else:
        digit = digit.replace(",", '')
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


def getReaperScansReleased(Title, urlbasic, urlchapter, r1, g, b, id_channel, id_guild):
    content = []
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

    if chapter_number == round(chapter_number, 0):
        urlchapter = f"{urlchapter}{int(chapter_number)}/"
    else:
        moment_number = str(chapter_number).replace('.', '-')
        urlchapter = f"{urlchapter}{moment_number}/"

    last_chapters = {}
    content_new = []
    content_new_ = f'{id_guild}-{Title}-{chapter_number}'
    content_new.append(content_new_)
    # Now get the time of release and if it already was released today or not
    with open('server_latest.txt', 'r') as r_sl:
        if r_sl is not None:
            for line in r_sl:
                if line is not None:
                    line_ = line.split('-')
                    if line_[0] == id_guild:
                        content_element = f'{line_[0]}-{(line_[1])}-{(line_[2])}'
                        content.append(content_element)
                        last_chapters.setdefault(line_[1], f'{line_[2]}')
                # Title Source  url  url_chapter r g b rHour rMinute rDay


    last_chapter = 0
    new = False
    if last_chapters.keys().__contains__(Title):
        # It isnt newly added to the database!
        name_number = str(last_chapters[Title])
        title = name_number[0]
        last_chapter = name_number

        message_release = f"The Chapters {chapter_number} was released!"
    else:
        # It is new so set new to True
        new = True
        last_chapter = int(chapter_number) - 1
        message_release = f"The {Title} was added to existing bookmarks!"

    if new is False:
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"{message_release} \n Link to the chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")
    else:
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                              description=f"{message_release} \n Link to the chapter: {urlchapter}",
                              color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")
    released = False
    if float(chapter_number) > float(last_chapter):
        released = True

    # now I will edit the server_latest file

    with open('server_latest.txt', 'w') as wf:
        # Check if there are some that have to be updated
        for line in content:
            for line_new in content_new:
                id_g_new = line_new.split("-")[0]
                id_g = line.split("-")[0]
                if id_g_new == id_g:
                    # found the same server
                    # Now I need to check for the Title
                    title_new = line_new.split("-")[1]
                    title_ = line.split("-")[1]
                    if title_ == title_new:
                        # Its the same manga! so delete the old one
                        content.remove(line)

        # Write it down
        for c in content_new:
            wf.write(c + " \n")
        for c in content:
            wf.write(c)

    return released, embed


# Manga Clash

def getMangaClash(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    '''
        Thumbnail:  Y
        CHAPTER_NUMBER: Y
        URL_CHAPTER: Y
        CHECK_RELEASES: Y
    '''

    # Now get the time of release and if it already was released today or not

    web = req.get(url=f"{urlbasic}")
    menu_soup = bs(web.content, features="html.parser")
    chapter_text = (menu_soup.find("li", class_="wp-manga-chapter"))
    chapter_text = str(chapter_text.find("a"))
    chapter_text = chapter_text.split(">")[1]
    chapter_number = float(chapter_text.replace("</a", "").split(" ")[1])
    # now we have chapter_number

    # Mow I need the second chapter release date

    chapter_second = str(menu_soup.find_all("li", class_="wp-manga-chapter")[1])
    chapter_second = chapter_second.split('>')[5]
    chapter_second = chapter_second.split('<')[0]
    date_text = chapter_second

    # Returns the time until release
    until_release = getTime(rHour, rMin, rDay)

    # Now I will add the number of chapter to the url of chapter
    if chapter_number == int(chapter_number):
        urlchapter = str(urlchapter) + f'{int(chapter_number)}/'
        # It is a full number
    else:
        m_chapter_number = str(chapter_number).replace(".", '-')
        urlchapter = str(urlchapter) + f'{m_chapter_number}/'
    # Now I have the URL for the chapter

    # now I need the chapter_thumbnail
    thumbnail_text = (menu_soup.find("div", class_="summary_image"))
    thumbnail_text = str(thumbnail_text.find("img")).split('"')[5]
    url_thumbnail = thumbnail_text

    next_chapter = chapter_number + 1

    last_chapters = {}
    # Check if the last_chapters has the  current chapter number, if does it has not been released yet
    if last_chapters[Title] == chapter_number:
        released = False
    else:
        released = True

    if until_release[1] is True and released is True:
        message_release = f'The Chapter {int(next_chapter)} is being translated \n or is on break or has random releases'
    else:
        message_release = f'The Chapter {next_chapter} will be released in {until_release[0]}'
    embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                          description=f"The Chapter {chapter_number} \n " + message_release + f"\n Link to latest chapter: {urlchapter}",
                          color=discord.Color.from_rgb(r1, g, b))
    embed.set_image(url=f"{url_thumbnail}")
    return embed, chapter_number


def getMangaClashReleased(Title, urlbasic, urlchapter, r1, g, b):
    '''
        Thumbnail:  Y
        CHAPTER_NUMBER: Y
        URL_CHAPTER: Y
        CHECK_RELEASES: Y
    '''

    # Now get the time of release and if it already was released today or not

    web = req.get(url=f"{urlbasic}")
    menu_soup = bs(web.content, features="html.parser")
    chapter_text = (menu_soup.find("li", class_="wp-manga-chapter"))
    chapter_text = str(chapter_text.find("a"))
    chapter_text = chapter_text.split(">")[1]
    chapter_number = float(chapter_text.replace("</a", "").split(" ")[1])
    # now we have chapter_number

    # Now I will add the number of chapter to the url of chapter
    if chapter_number == int(chapter_number):
        urlchapter = str(urlchapter) + f'{int(chapter_number)}/'
        # It is a full number
    else:
        m_chapter_number = str(chapter_number).replace(".", '-')
        urlchapter = str(urlchapter) + f'{m_chapter_number}/'
    # Now I have the URL for the chapter

    # now I need the chapter_thumbnail
    thumbnail_text = (menu_soup.find("div", class_="summary_image"))
    thumbnail_text = str(thumbnail_text.find("img")).split('"')[5]
    url_thumbnail = thumbnail_text
    last_chapters = {}
    if last_chapters.keys().__contains__(Title):
        chapter_last_number = float(last_chapters.get(Title))
        # It has last chapter, so chose the last chapter
    else:
        chapter_last_number = chapter_number - 1
        # It doesnt have chapter, so set it as empty
    if chapter_number - chapter_last_number <= 1.0 and not 0.0:
        m_chapter_number = chapter_number
    elif chapter_number - chapter_last_number > 1.0:
        chapters_released = list(range(int(chapter_last_number) + 1, int(chapter_number)))
        m_chapter_number = ""
        for numbers in chapters_released:
            numbers = int(numbers)
            m_chapter_number += f'{str(numbers)}'
        # Now I have the list of all released chapters

    # Its more than 1 chapter

    embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                          description=f"The Chapter {m_chapter_number} was released! " + f"\n Link to latest chapter: {urlchapter}",
                          color=discord.Color.from_rgb(r1, g, b))
    embed.set_image(url=f"{url_thumbnail}")
    return embed, chapter_number, chapter_last_number
    # New chapter was RELEASED!!!!


# 1st Kiss

def get1stKiss(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    print("")


def get1stKissReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")


# Aqua Manga

def getAquaManga(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    print("")


def getAguaMangaReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")


# 365Manga

def get365Manga(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    print("")


def get365MangaReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")


# 247Manga

def get247Manga(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    print("")


def get247MangaReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")


# Webtoons.com

def getWebtoons(Title, urlbasic, urlchapter, r1, g, b, rHour, rMin, rDay):
    print("")


def getWebtoonsReleased(Title, urlbasic, urlchapter, r1, g, b):
    print("")


# <@401845652541145089>
'''@bot.command()
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
    await ctx.send(embed=embed)'''

chapterReleaseCheck.start()
bot.run('ODg3Mzc4NzM3MTQ5MTQ1MTI4.GKxdP8.yh1GiPrn7OZdr6smO4s3TkeLn_RIFdlcI-Ll68')
