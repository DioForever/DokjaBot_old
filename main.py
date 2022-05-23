import json
from datetime import datetime
from discord.ext import tasks
import discord
import pandas as pd
import requests as r
from bs4 import BeautifulSoup as bs
from discord.ext import commands
from pypresence import Presence


bot = commands.Bot(command_prefix="!")
print('The DokjaBot has been activated')

rpc = Presence(887378737149145128)
rpc.connect()
rpc.update(state="Reading",details='I am having fun',large_image='rpcphoto.png')

last_chapters = {
    "The Challenger": 0,
    "The Great Mage Returns After 4000 Years": 0,
    "Is this Hero for Real?": 0,
    "Archmage Streamer": 0,
    "tbate": 0,
    "fff_trashero": 0,
}
content=[]
# await bot.wait_until_ready()
with open('chapters.txt','r') as f:
    for line in f:
        line_ = line.split('-')
        last_chapters[line_[0]]=int(line_[1])





@bot.command()
async def supl(ctx):
    datet = datetime.today().strftime("%Y%m%d")
    odpoved = r.get("https://skripta.ssps.cz/substitutions.php/?date=" + datet)
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
    #Now check if user is in the list

    await bot.wait_until_ready()
    channel = bot.get_channel(977231331199164466)
    await channel.send('Pinging {}'.format(ctx.author.mention))
    await channel.send('<@401845652541145089>')

@bot.command()
async def m_list(ctx):
    all = ("\n  The Beginning after the end - !m_tbate \n" +
           "    The Challenger - !m_the_challenger \n" +
           "    Is this Hero for Real? - !m_hero_for_real \n" +
           "    Archmage Streamer - !m_archmage_streamer \n" +
           "    FFF-Class Trashero - !m_fth \n" +
           "    The Great Mage Returns After 4000 Years - !m_mage_returns \n")
    embed = discord.Embed(title=f"List of Manhwas/Mangas",
                          description=f"The list of commands for \n " + "Manhwas and Mangas in system" + f"\n {all}",
                          color=discord.Color.from_rgb(246, 214, 4))
    await ctx.send(embed=embed)


@bot.command()
async def m_tbate(ctx):
    TBATE_Web = r.get("https://beginningafterend.com/?2022-05%3F2022-05-20")
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
    web_Chapter = r.get(url_chapter)
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
    FFF_Web = r.get("https://manhuazone.com/manga/5-fff-class-tras-hero/")
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
    web_Chapter = r.get(url_chapter)
    soup_Chapter = bs(web_Chapter.content, features="html.parser")
    date_split = url_chapter.split('?')
    date_length = len(date_split)
    chapter_number = int(chapter_number) + 1
    message_release = (
        f"The Chapter {chapter_number} will be released in some time, \n this comic doesn´t have specific \n time for releases \n it typically releases \n once 10-20 days a few chapters at once \n "
        f"Last chapter was released on {last_release}")
    chapter_number = int(chapter_number) - 1
    embed = discord.Embed(title=f"FFF-Class Trashero", url="https://manhuazone.com/manga/5-fff-class-tras-hero/",
                          description=f"Chapter {chapter_number} \n " + message_release + "\n Link to last chapter: " + url_chapter,
                          color=discord.Color.from_rgb(167, 14, 191))
    embed.set_image(url="https://i0.hdslb.com/bfs/comic-static/70c263ce2dffe3fdd94369955d0c2bc6cde0c70b.png@600w.jpg")
    await ctx.send(embed=embed)


@bot.command()
async def m_archmage_streamer(ctx):
    embed = getReaperScans("Archmage Streamer", "https://reaperscans.com/series/archmage-streamer/",
                           "https://reaperscans.com/series/archmage-streamer/chapter-", 0, 180, 246, 18, 0, 4)[0]
    await ctx.send(embed=embed)


@bot.command()
async def m_hero_for_real(ctx):
    embed = getReaperScans("Is this Hero for Real?", "https://reaperscans.com/series/is-this-hero-for-real/",
                           "https://reaperscans.com/series/is-this-hero-for-real/chapter-", 0, 0, 0, 18, 0, 0)[0]
    await ctx.send(embed=embed)


@bot.command()
async def m_mage_returns(ctx):
    embed = getReaperScans("The Great Mage Returns After 4000 Years",
                           "https://reaperscans.com/series/the-great-mage-that-returned-after-4000-years/",
                           "https://reaperscans.com/series/the-great-mage-that-returned-after-4000-years/chapter-", 93,
                           0, 174, 18, 0, 3)[0]
    await ctx.send(embed=embed)


@bot.command()
async def m_the_challenger(ctx):
    embed = getReaperScans("The Challenger",
                           "https://reaperscans.com/series/the-challenger/https://reaperscans.com/series/the-challenger/",
                           "https://reaperscans.com/series/the-challenger/chapter-", 246, 214, 4, 18, 0, 5)[0]
    await ctx.send(embed=embed)







@tasks.loop(seconds=60)  # repeat after every 10 seconds
async def myLoop():

    await bot.wait_until_ready()
    channel = bot.get_channel(977231331199164466)
    content = []
    with open('chapters.txt', 'r') as f:
        for line in f:
            content.append(line)
    number_chapter_challenger = getReaperScans("The Challenger",
                                               "https://reaperscans.com/series/the-challenger/https://reaperscans.com/series/the-challenger/",
                                               "https://reaperscans.com/series/the-challenger/chapter-", 246, 214, 4,
                                               18, 0, 3)[1]
    number_chapter_mage_returns = getReaperScans("The Great Mage Returns After 4000 Years",
                                                 "https://reaperscans.com/series/the-great-mage-that-returned-after-4000-years/",
                                                 "https://reaperscans.com/series/the-great-mage-that-returned-after-4000-years/chapter-",
                                                 93, 0, 174, 18, 0, 3)[1]
    number_chapter_hero_for_real = \
        getReaperScans("Is this Hero for Real?", "https://reaperscans.com/series/is-this-hero-for-real/",
                       "https://reaperscans.com/series/is-this-hero-for-real/chapter-", 0, 0, 0, 18, 0, 0)[1]
    number_chapter_archmage_streamer = \
        getReaperScans("Archmage Streamer", "https://reaperscans.com/series/archmage-streamer/",
                       "https://reaperscans.com/series/archmage-streamer/chapter-", 0, 180, 246, 18, 0, 4)[1]
    subscription = []
    with open('chapters_release_ping', 'r') as f:
        for line in f:
            subscription.append(line)
    content_new = []
    if last_chapters["The Challenger"] < number_chapter_challenger:
        last_chapters["The Challenger"] = number_chapter_challenger
        new_chapter = f"The Challenger has a new chapter {number_chapter_challenger}!"
        changed = True
        content_new.append(f"The Challenger-{number_chapter_challenger}")

        embed = getReaperScansReleased("The Challenger",
                                       "https://reaperscans.com/series/the-challenger/https://reaperscans.com/series/the-challenger/",
                                       "https://reaperscans.com/series/the-challenger/chapter-", 246, 214, 4)
        await channel.send(embed=embed)
        await channel.send(f'Ping of The Challenger {number_chapter_challenger}: {subscription}',delete_after=3)
    if last_chapters["The Great Mage Returns After 4000 Years"] < number_chapter_mage_returns:
        last_chapters["The Great Mage Returns After 4000 Years"] = number_chapter_mage_returns
        new_chapter = f"The Great Mage Returns After 4000 Years has a new chapter {number_chapter_mage_returns}!"
        changed = True
        content_new.append(f"The Great Mage Returns After 4000 Years-{number_chapter_mage_returns}")
        embed = getReaperScansReleased("The Great Mage Returns After 4000 Years",
                                       "https://reaperscans.com/series/the-great-mage-that-returned-after-4000-years/",
                                       "https://reaperscans.com/series/the-great-mage-that-returned-after-4000-years/chapter-",
                                       93, 0, 174)
        await channel.send(embed=embed)
        await channel.send(f'Ping of The Great Mage Returns After 4000 Years {number_chapter_mage_returns}: {subscription}',delete_after=3)
    if last_chapters["Is this Hero for Real?"] < number_chapter_hero_for_real:
        last_chapters["Is this Hero for Real?"] = number_chapter_hero_for_real
        new_chapter = f"Is this Hero for Real? has a new chapter {number_chapter_archmage_streamer}!"
        changed = True
        content_new.append(f"Is this Hero for Real?-{number_chapter_hero_for_real}")
        embed = getReaperScansReleased("Is this Hero for Real?", "https://reaperscans.com/series/is-this-hero-for-real/",
                               "https://reaperscans.com/series/is-this-hero-for-real/chapter-", 0, 0, 0)
        await channel.send(embed=embed)
        await channel.send(f'Ping of Is this Hero for Real? {number_chapter_hero_for_real}: {subscription}',delete_after=3)
    if last_chapters["Archmage Streamer"] < number_chapter_archmage_streamer:
        last_chapters["Archmage Streamer"] = number_chapter_archmage_streamer
        new_chapter = f"Archmage Streamer has a new chapter {number_chapter_archmage_streamer}!"
        changed = True
        content_new.append(f"Archmage Streamer-{number_chapter_archmage_streamer}")
        embed = getReaperScansReleased("Archmage Streamer", "https://reaperscans.com/series/archmage-streamer/",
                               "https://reaperscans.com/series/archmage-streamer/chapter-", 0, 180, 246)
        await channel.send(embed=embed)
        await channel.send(f'Ping of Archmage Streamer {number_chapter_archmage_streamer}: {subscription}',delete_after=3)


    # Save the last_chapters to the chapters.txt file
    '''    for con in content:
        for co in content_new:
            con_ = con.split('-')[0]
            co_ = co.split('-')[0]
            if con_==co_:
                content.remove(con)'''
    with open('chapters.txt', 'w') as wf:
        # Check if there are some that have to be updated
        for c in content:
            for c_ in content_new:
                cs = c.split('-')[0]
                cs_ = c_.split('-')[0]
                if cs_ == cs:
                    content.remove(c)

        # Write it down
        for c in content_new:
            wf.write(c+" \n")
        for c in content:
            wf.write(c)

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
    web = r.get(url=urlbasic)
    chapter_number = 0
    soup = bs(web.content, features="html.parser")
    chapter = soup.find("li", class_="wp-manga-chapter")
    thumbnail_text = str(chapter.find("img", class_="thumb"))
    thumbnail_text = thumbnail_text.split('"')
    url_thumbnail = thumbnail_text[len(thumbnail_text) - 2]
    # Now I have the thumbnail

    # Now I need the chapter number
    chapter_text = str(chapter.find("p", class_="chapter-manhwa-title")).split()
    chapter_number = int(str(chapter_text[2]).split('<')[0])
    # Now I have the number as well

    urlchapter = f"https://reaperscans.com/series/archmage-streamer/chapter-{chapter_number}/"

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
        chapter_number += 1
        message_release = f"The Chapter {chapter_number} will be released in {getTime(rHour, rMin, rDay)[0]}"
        chapter_number -= 1
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
    web = r.get(url=urlbasic)
    chapter_number = 0
    soup = bs(web.content, features="html.parser")
    chapter = soup.find("li", class_="wp-manga-chapter")
    thumbnail_text = str(chapter.find("img", class_="thumb"))
    thumbnail_text = thumbnail_text.split('"')
    url_thumbnail = thumbnail_text[len(thumbnail_text) - 2]
    # Now I have the thumbnail

    # Now I need the chapter number
    chapter_text = str(chapter.find("p", class_="chapter-manhwa-title")).split()
    chapter_number = int(str(chapter_text[2]).split('<')[0])
    # Now I have the number as well

    urlchapter = f"https://reaperscans.com/series/archmage-streamer/chapter-{chapter_number}/"

    # Now get the time of release and if it already was released today or not

    chapters_released = ""
    if last_chapters[Title]-chapter_number!=-1:
        #It has more than 1 released chapter at once, so it was mass release or somethin like that
        for number in range(last_chapters[Title],chapter_number+1):
            chapters_released+= str(number)+", "
        message_release = f"The Chapters {chapters_released} was released!"
    else:
        message_release = f"The Chapter {chapters_released} was released!"
    # Now display it

    if len(chapters_released)>1:
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                          description=f"{message_release} \n Link to latest chapter: {urlchapter}",
                          color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")
    else:
        embed = discord.Embed(title=f"{Title}", url=f"{urlbasic}",
                          description=f"{message_release} \n Link to the chapter: {urlchapter}" ,
                          color=discord.Color.from_rgb(r1, g, b))
        embed.set_image(url=f"{url_thumbnail}")
    return embed

# <@401845652541145089>


myLoop.start()
bot.run('ODg3Mzc4NzM3MTQ5MTQ1MTI4.GKxdP8.yh1GiPrn7OZdr6smO4s3TkeLn_RIFdlcI-Ll68')