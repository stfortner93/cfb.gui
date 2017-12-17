import requests
from bs4 import BeautifulSoup

scorelist1 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/01/"
scorelist2 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/02/"
scorelist3 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/03/"
scorelist4 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/04/"
scorelist5 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/05/"
scorelist6 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/06/"
scorelist7 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/07/"
scorelist8 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/08/"
scorelist9 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/09/"
scorelist10 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/10/"
scorelist11 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/11/"
scorelist12 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/12/"
scorelist13 = "https://www.cbssports.com/college-football/scoreboard/FBS/2017/regular/13/"


masterscorelist = [scorelist1, scorelist2, scorelist3, scorelist4, scorelist5, scorelist6, scorelist7, scorelist8, scorelist9, scorelist10, scorelist11, scorelist12, scorelist13]

#Total Offense -- tds[2] - tds [7]
url_OffTotal = 'http://www.ncaa.com/stats/football/fbs/current/team/21/p1'
url_OffTotal2 = 'http://www.ncaa.com/stats/football/fbs/current/team/21/p2'
url_OffTotal3 = 'http://www.ncaa.com/stats/football/fbs/current/team/21/p3'

#List for them all
urlOffTotalList = [url_OffTotal, url_OffTotal2, url_OffTotal3]

#Offensive Scoring----tds[7]--tds[9]. tds[10]
url_OffScor1 = 'http://www.ncaa.com/stats/football/fbs/current/team/27/p1'
url_OffScor2 = 'http://www.ncaa.com/stats/football/fbs/current/team/27/p2'
url_OffScor3 = 'http://www.ncaa.com/stats/football/fbs/current/team/27/p3'

#List for them all
urlOffScorList = [url_OffScor1, url_OffScor2, url_OffScor3]

urlOffList = [urlOffTotalList, urlOffScorList]

#Total Defensive -- tds[2] - tds [7]
url_DefTotal1 = 'http://www.ncaa.com/stats/football/fbs/current/team/22/p1'
url_DefTotal2 = 'http://www.ncaa.com/stats/football/fbs/current/team/22/p2'
url_DefTotal3 = 'http://www.ncaa.com/stats/football/fbs/current/team/22/p3'
urlDefTotalList = [url_DefTotal1, url_DefTotal2, url_DefTotal3]

#Defensive Scoring -- tds[7]--tds[9], tds[10]
url_DefScor1 = 'http://www.ncaa.com/stats/football/fbs/current/team/28/p1'
url_DefScor2 = 'http://www.ncaa.com/stats/football/fbs/current/team/28/p2'
url_DefScor3 = 'http://www.ncaa.com/stats/football/fbs/current/team/28/p3'
urlDefScorList = [url_DefScor1, url_DefScor2, url_DefScor3]

urlDefList = [urlDefTotalList, urlDefScorList]

#Winning Perc
url_Win1 = 'http://www.ncaa.com/stats/football/fbs/current/team/742/p1'
url_Win2 = 'http://www.ncaa.com/stats/football/fbs/current/team/742/p2'
url_Win3 = 'http://www.ncaa.com/stats/football/fbs/current/team/742/p3'
urlWinList = [url_Win1, url_Win2, url_Win3]


url_MasterList = [urlOffList, urlDefList, urlWinList]
