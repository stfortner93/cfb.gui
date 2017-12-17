from bs4 import BeautifulSoup
from url2 import *
import requests
import copy
import sqlite3
from sqlite import *
import sys
from cs50 import SQL

#"""
#This is a program to try and create a cfb ranking system. Note that I am not a very good programmer. I actually kinda
#suck. There is a lot going on here, probably a little to much. Anyway. Just try to follow along and good luck!
#"""
#First off, actually creating our database and then creating our tables for the database. The create table fuctions
# are housed in the sqlite.py file.
def database_create():
    conn = sqlite3.connect("cfb3.sqlite")
    db = conn.cursor()
    db2 = conn.cursor()
    create_off()
    create_def()
    create_win()
    create_scoreboard()

#Web scraping the data, then inserting it into the tables
def database_insert():
    for urlList in url_MasterList:
        if (urlList == urlOffList):
            for url in urlList:
                for urloff in url:
                    page = requests.get(urloff)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    if (url == urlOffTotalList):
                            for tr in soup.find_all('tr')[1:]:
                                tds = tr.find_all('td')
                                a = (tds[1].text)
                                b = (tds[2].text)
                                c = (tds[3].text)
                                d = (tds[4].text)
                                e = (tds[5].text)
                                f = (tds[6].text)
                                g = (tds[7].text)
                                db.execute("INSERT or IGNORE INTO offensive (team) VALUES (?)", (a,))
                                db.execute("UPDATE offensive SET games_played = ?, plays = ?, \
                                    yards = ?, yards_play = ?, touchdowns = ?, ypg = ? WHERE team = ?", \
                                    (b,c, d, e, f, g, a,))
                                conn.commit()
                    elif url == urlOffScorList:
                            for tr in soup.find_all('tr')[1:]:
                                tds = tr.find_all('td')
                                a = (tds[7].text)
                                b = (tds[9].text)
                                c = (tds[10].text)
                                d = (tds[1].text)
                                db.execute("INSERT or IGNORE INTO offensive (team) VALUES (?)", (d,))
                                db.execute("UPDATE offensive SET field_goals = ?, points = ?, ppg = ? WHERE team = ?", \
                                    (a, b, c, d))
                                conn.commit()
        elif (urlList == urlDefList):
            for url in urlList:
                for urldef in url:
                    page = requests.get(urldef)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    if (url == urlDefTotalList):
                            for tr in soup.find_all('tr')[1:]:
                                tds = tr.find_all('td')
                                a = (tds[1].text)
                                b = (tds[2].text)
                                c = (tds[3].text)
                                d = (tds[4].text)
                                e = (tds[5].text)
                                f = (tds[6].text)
                                g = (tds[7].text)
                                db.execute("INSERT or IGNORE INTO defensive (team) VALUES (?)", (a,))
                                db.execute("UPDATE defensive SET games_played = ?, plays = ?, \
                                    yards = ?, yards_play = ?, touchdowns = ?, ypg = ? WHERE team = ?", \
                                    (b,c, d, e, f, g, a,))
                                conn.commit()
                    elif url == urlDefScorList:
                            for tr in soup.find_all('tr')[1:]:
                                tds = tr.find_all('td')
                                a = (tds[7].text)
                                b = (tds[9].text)
                                c = (tds[10].text)
                                d = (tds[1].text)
                                db.execute("INSERT or IGNORE INTO defensive (team) VALUES (?)", (d,))
                                db.execute("UPDATE defensive SET field_goals = ?, points = ?, ppg = ? WHERE team = ?", (a, b, c, d,))
                                conn.commit()
        elif (urlList == urlWinList):
            for url in urlList:
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                for tr in soup.find_all('tr')[1:]:
                    tds = tr.find_all('td')
                    a = (tds[1].text)
                    b = (tds[2].text)
                    c = (tds[3].text)
                    d = (tds[4].text)
                    e = (tds[5].text)
                    db.execute("INSERT or IGNORE INTO win (team) VALUES (?)", (a,))
                    db.execute("UPDATE win SET won = ?, lost = ?, \
                        tied = ?, winning_percentage = ? WHERE team = ?", \
                        (b,c,d,e,a,))
                    conn.commit()

def off_ranking():
    db.execute("SELECT * FROM offensive")
    for row in range(1, 130):
        db.execute("SELECT plays, games_played, ypg, ppg from offensive WHERE rank = ?", (row,))
        stats = db.fetchone()
        plays_game = round((stats[0] / stats[1]), 2)
        ypg_ppg = round((stats[2] / stats[3]), 2)
        plays_ppg = round(((plays_game / stats[3] * 10)), 2)
        ranking = round((plays_ppg / ((plays_game * ypg_ppg) / 100)), 2)
        db.execute("UPDATE offensive SET plays_game = ?, ypg_ppg = ?, plays_ppg = ?, ranking = ? \
            WHERE rank = ?", (plays_game, ypg_ppg, plays_ppg, ranking, row,))
        conn.commit()

def def_ranking():
    db.execute("SELECT * FROM offensive")
    for row in range(1, 130):
        db.execute("SELECT plays, games_played, ypg, ppg from defensive WHERE rank = ?", (row,))
        stats = db.fetchone()
        plays_game = round((stats[0] / stats[1]), 2)
        ypg_ppg = round((stats[2] / stats[3]), 2)
        plays_ppg = round(((plays_game / stats[3] * 10)), 2)
        ranking = round((plays_ppg / ((plays_game * ypg_ppg) / 100)), 2)
        db.execute("UPDATE defensive SET plays_game = ?, ypg_ppg = ?, plays_ppg = ?, ranking = ? \
            WHERE rank = ?", (plays_game, ypg_ppg, plays_ppg, ranking, row,))
        conn.commit()

def scoreboard_insert():
    create_scoreboard()
    for urllist in (masterscorelist):
        for url in urllist:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            scores = soup.find_all('table', class_ = 'linescore')
            db.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_list = db.fetchall()
            print("150")
            if urllist == scorelist_1:
                #print(scores)
                score_insert(scores, table_list[4])
            elif urllist == scorelist_2:
                #print(scores)
                score_insert(scores, table_list[5])
            else:
                #print(scores)
                score_insert(scores, table_list[6])
            #db.execute("SELECT name FROM sqlite_master WHERE type='table';")
            #table_list = db.fetchall()
            #for table in table_list:
            #    print(table)
            #    if table == 'scoreboard_1':
            #        print("143")
            #        scoreboard_insert_two(urllist, table)
            #    elif table == "scoreboard_2":
            #        print("153")
            #        scoreboard_insert_two(urllist, table)
            #    elif table == "scoreboard_3":
            #        print("149")
            #        scoreboard_insert_two(urllist, table)

def scoreboard_insert_two(urllist, table):
    print("150")
    if urllist == scorelist_1:
        #print(scores)
        score_insert(scores, scoreboard_1)
    elif urllist == scorelist_2:
        #print(scores)
        score_insert(scores, scoreboard_2)
    else:
        #print(scores)
        score_insert(scores, scoreboard_3)

def score_insert(soup, table):
    i = 0
    x = 0
    y = 0
    tablename = table
    for game in soup:
        i += 1 #Gets each game
        scores = []
        for tr in game.find_all('tr')[1:]: #gets each team in game
            score = (tr.a.text, tr.find('td', class_ = 'final score').text)
            scores.extend(score)
        print(scores)
        a = scores[0]
        b = scores[1]
        c = scores[2]
        d = scores[3]
        db.execute("SELECT ? FROM" +tablename+ "WHERE team_one= ?", (c, a))
        vals = db.fetchall()
        if vals is None:
            x += 1
            db2.execute("INSERT INTO" +table+ "(team_one, score_one, team_two, score_two) VALUES (?, ?, ?, ?)", \
                (scores[0], scores[1], scores[2], scores[3], ))
            conn.commit()
        else:
            print(vals)
            y += 1
    print(i, x, y)

#Creating the stength of schedule for the offense.
def off_opp():
    teams_list = [] #Creating a list of all the teams
    db.execute("SELECT team FROM offensive")
    for row in db.fetchall():
        l = list(row)
        teams_list.append(l)
    for teams in (teams_list):  #Each team in the list
        team_test = [teams]
        #for team in range(teams):
        print(teams)
        db.execute("SELECT score_one, team_two FROM scoreboard_1 where team_one = ?", (teams[0],))
        check_list = db.fetchall()
        print(check_list)
        for check in check_list:
            #print(check)
            if check is None:
                print(team, "192")
                db2.execute("SELECT score_two, team_one FROM scoreboard_1 where team_two = ?", (team_test,))
                check2 = db2.fetchall()
                if check2 is None:
                    print(team, " 196")
                    #pass
                else:
                    print(team, " 199")
                    try:
                        points = int(check[0])
                        db2.execute("SELECT rank from defensive where team = ?", (check2[1],))
                        deff = db2.fetchone()
                        deff_rank = int(deff[0])
                        final = ((points * deff_rank)/100)
                        print(final)
                        team_test.extend(final)
                        print(team, "208")
                    except:
                        pass
            else:
                print("218")
                print("219")
                points = int(check[0])
                print(points)
                db2.execute("SELECT ranking from defensive where team = ?", (check[1],))
                deff = db2.fetchone()
                deff_rank = deff[0]
                final = round(((points * deff_rank)/100), 2)
                print(final)
                teams.append(final)
                print(teams)
    print(teams_list)

def main():
    database_create()
    #database_insert()
    #off_ranking()
    #def_ranking()
    scoreboard_insert()
    #off_opp()

if __name__ == '__main__':
    main()
