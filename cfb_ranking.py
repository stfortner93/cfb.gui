from bs4 import BeautifulSoup
from cbsurl import *
import requests
import copy
import sqlite3
from sqlite import *
from cbslist import *
import sys
from cs50 import SQL

def database_create():
    create_table()
    conn = sqlite3.connect("cfb5.sqlite")
    db = conn.cursor()
    db2 = conn.cursor()

def create_scores():
    scoreboard = []
    for scorelist in masterscorelist:
        page = requests.get(scorelist)
        soup = BeautifulSoup(page.content, 'html.parser')
        for line in soup.find_all("div", {"class":"live-update"}):
            scores = []
            for tr in line.find_all("tr")[1:]:
                teams = tr.find("a", {"class" :"team"})
                final = tr.find("td" ,{"class": "total-score"})
                if final:
                    team = (teams.get_text().strip())
                    t = team_correction_list(team)
                    score = (t, final.get_text().strip())
                    scores.extend(score)
            scoreboard.append(scores)
    #print(scoreboard)
    scoreboard_insert(scoreboard)

def scoreboard_insert(scoreboard):
    for lines in range(len(scoreboard)):
        try:
            line = scoreboard[lines]
            db.execute("SELECT team_two FROM scoreboard_1 WHERE team_one = ?", (line[0],))
            checks = db.fetchall()
            #if not checks:
            #    db.execute("INSERT INTO scoreboard_1 (team_one, score_one, team_two, score_two) VALUES (?, ?, ?, ?)", (line[0], line[1], line[2], line[3]))
            #    conn.commit()
            if not any(line[2] in check for check in checks):
                db.execute("INSERT INTO scoreboard_1 (team_one, score_one, team_two, score_two) VALUES (?, ?, ?, ?)", (line[0], line[1], line[2], line[3],))
                conn.commit()

        except:
            pass

def database_insert():
    for urlList in url_MasterList:
        if (urlList == urlOffList):
            for url in urlList:
                for urloff in url:
                    insert_offensive(url, urloff)
        elif (urlList == urlDefList):
            for url in urlList:
                for urldef in url:
                    insert_defensive(url, urldef)
        elif (urlList == urlWinList):
            for url in urlList:
                insert_win(url)

def insert_offensive(url, urloff):
    page = requests.get(urloff)
    soup = BeautifulSoup(page.content, 'html.parser')
    if (url == urlOffTotalList):
            for tr in soup.find_all('tr')[1:]:
                tds = tr.find_all('td')
                a = (tds[1].text)
                team = team_correction_list(a)
                b = (tds[2].text)
                c = (tds[3].text)
                d = (tds[4].text)
                e = (tds[5].text)
                f = (tds[6].text)
                g = (tds[7].text)
                db.execute("INSERT or IGNORE INTO offensive (team) VALUES (?)", (team,))
                db.execute("UPDATE offensive SET games_played = ?, plays = ?, \
                    yards = ?, yards_play = ?, touchdowns = ?, ypg = ? WHERE team = ?", \
                    (b,c, d, e, f, g, team,))
                conn.commit()
    elif url == urlOffScorList:
            for tr in soup.find_all('tr')[1:]:
                tds = tr.find_all('td')
                a = (tds[7].text)
                b = (tds[9].text)
                c = (tds[10].text)
                d = (tds[1].text)
                team = team_correction_list(d)
                db.execute("INSERT or IGNORE INTO offensive (team) VALUES (?)", (team,))
                db.execute("UPDATE offensive SET field_goals = ?, points = ?, ppg = ? WHERE team = ?", \
                    (a, b, c, team))
                conn.commit()

def insert_defensive(url, urldef):
    page = requests.get(urldef)
    soup = BeautifulSoup(page.content, 'html.parser')
    if (url == urlDefTotalList):
            for tr in soup.find_all('tr')[1:]:
                tds = tr.find_all('td')
                a = (tds[1].text)
                team = team_correction_list(a)
                b = (tds[2].text)
                c = (tds[3].text)
                d = (tds[4].text)
                e = (tds[5].text)
                f = (tds[6].text)
                g = (tds[7].text)
                db.execute("INSERT or IGNORE INTO defensive (team) VALUES (?)", (team,))
                db.execute("UPDATE defensive SET games_played = ?, plays = ?, \
                    yards = ?, yards_play = ?, touchdowns = ?, ypg = ? WHERE team = ?", \
                    (b,c, d, e, f, g, team,))
                conn.commit()
    elif url == urlDefScorList:
            for tr in soup.find_all('tr')[1:]:
                tds = tr.find_all('td')
                a = (tds[7].text)
                b = (tds[9].text)
                c = (tds[10].text)
                d = (tds[1].text)
                team = team_correction_list(d)
                db.execute("INSERT or IGNORE INTO defensive (team) VALUES (?)", (team,))
                db.execute("UPDATE defensive SET field_goals = ?, points = ?, ppg = ? WHERE team = ?", (a, b, c, team,))
                conn.commit()

def insert_win(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        a = (tds[1].text)
        team = team_correction_list(a)
        b = (tds[2].text)
        c = (tds[3].text)
        d = (tds[4].text)
        e = (tds[5].text)
        db.execute("INSERT or IGNORE INTO win (team) VALUES (?)", (team,))
        db.execute("UPDATE win SET won = ?, lost = ?, \
            tied = ?, winning_percentage = ? WHERE team = ?", \
            (b,c,d,e,team,))
        conn.commit()

def off_ranking():
    db.execute("SELECT * FROM offensive")
    for row in range(1, 130):
        db.execute("SELECT plays, games_played, ypg, ppg from offensive WHERE rank = ?", (row,))
        stats = db.fetchone()
        plays_game = round((stats[0] / stats[1]), 2)
        ypg_ppg = round((stats[2] / stats[3]), 2)
        plays_ppg = round(((plays_game / stats[3] * 10)), 2)
        ranking = round(((plays_game * ypg_ppg)/ plays_ppg), 2)
        #ranking = round((plays_ppg / ((plays_game * ypg_ppg) / 100)), 2)
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

def off_def_sos():
    for i in range(129):
        off_opp()
        #print("//////////////////////////////////////////////////////////////////")
        def_opp()
        print("///////////////////////////////////////////////////////////////////")

def off_opp():
    teams_list = [] #Creating a list of all the teams
    db.execute("SELECT team FROM offensive")
    for row in db.fetchall():
        l = list(row)
        teams_list.append(l)
    for teams in (teams_list):  #Each team in the list
        home_score = off_opp_home(teams)
        away_score = off_opp_away(teams)
        home_score.extend(away_score)
        weight = 0
        for i in range(len(home_score)):
            weight = round((weight + home_score[i]), 2)
        teams.append(weight)
        db.execute("SELECT ranking FROM offensive WHERE team = ?", (teams[0],))
        ranking = db.fetchone()

        new_ranking = round((((weight / 100) * ranking[0]) / 1.5), 2)
        #print(teams[0], ranking, weight)
        db.execute("UPDATE offensive SET ranking = ? WHERE team = ?", (new_ranking, teams[0], ))
        conn.commit()

def off_opp_home(team):
    home_score = []
    db.execute("SELECT score_one, team_two FROM scoreboard_1 where team_one = ?", (team[0],))
    check_list = db.fetchall()
    for check in check_list:
        points = int(check[0])
        db2.execute("SELECT ranking from defensive where team = ?", (check[1],))
        deff = db2.fetchone()
        if deff:
            deff_rank = deff[0]
            final = round(((points * (deff_rank / 2.5))/10), 2)
            home_score.append(final)
        else:
            final = round(((points * (5 / 2.5))/10), 2)
            home_score.append(final)
    return home_score

def off_opp_away(team):
    away_score = []
    db.execute("SELECT score_two, team_one FROM scoreboard_1 where team_two = ?", (team[0],))
    check_list = db.fetchall()
    for check in check_list:
        points = int(check[0])
        db2.execute("SELECT ranking from defensive where team = ?", (check[1],))
        deff = db2.fetchone()
        if deff:
            deff_rank = deff[0]
            final = round(((points * deff_rank)/25), 2)
            away_score.append(final)
        else:
            final = round(((points * 5)/25), 2)
            away_score.append(final)
    return away_score

def def_opp():
    teams_list = [] #Creating a list of all the teams
    db.execute("SELECT team FROM defensive")
    for row in db.fetchall():
        l = list(row)
        teams_list.append(l)
    for teams in (teams_list):  #Each team in the list
        home_score = off_opp_home(teams)
        away_score = off_opp_away(teams)
        home_score.extend(away_score)
        weight = 0
        for i in range(len(home_score)):
            weight = round((weight + home_score[i]), 2)
        new_weight = (weight/5)
        teams.append(new_weight)
        db.execute("SELECT ranking FROM defensive WHERE team = ?", (teams[0],))
        ranking = db.fetchone()
        new_ranking = round((((weight / 100) * ranking[0]) * 2.5), 2)
        #new_ranking = round(((ranking[0]/weight) * 2.5), 2)
        #print(teams[0], ranking, weight)
        db.execute("UPDATE defensive SET ranking = ? WHERE team = ?", (new_ranking, teams[0], ))
        conn.commit()

def def_opp_home(team):
    home_score = []
    db.execute("SELECT score_two, team_two FROM scoreboard_1 where team_one = ?", (team[0],))
    check_list = db.fetchall()
    for check in check_list:
        points = int(check[0])
        db2.execute("SELECT ranking from offensive where team = ?", (check[1],))
        deff = db2.fetchone()
        if deff:
            off_rank = deff[0]
            final = round((((points / 100)* (deff_rank))/10), 2)
            home_score.append(final)
        else:
            final = round((((points / 100 )* (5 ))/10), 2)
            home_score.append(final)
    return home_score

def def_opp_away(team):
    away_score = []
    db.execute("SELECT score_one, team_one FROM scoreboard_1 where team_two = ?", (team[0],))
    check_list = db.fetchall()
    for check in check_list:
        points = int(check[0])
        db2.execute("SELECT ranking from offensive where team = ?", (check[1],))
        deff = db2.fetchone()
        if deff:
            off_rank = deff[0]
            final = round((((points / 100)* (deff_rank))/10), 2)
            away_score.append(final)
        else:
            final = round((((points / 2.5 )* (5 ))/10), 2)
            away_score.append(final)
    return away_score

def main():
    database_create()
    #create_scores()
    #database_insert()
    off_ranking()
    def_ranking()
    off_def_sos()

if __name__ == '__main__':
    main()
