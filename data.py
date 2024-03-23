import pandas as pd
from bs4 import BeautifulSoup
import requests
import tbapy
import bot

blueAllianceToken = "PiqFQSWcSw9DgmNEhNDviFRxzfTOa8Bp2l3g5nX42ngqqi9zlaLnzizwt2gtDQQQ"


stemURL = "https://www.thebluealliance.com/event/"
compCode = bot.compCode
pitURL = stemURL + compCode + "#teams"
matchURL = stemURL + compCode
rankingsURL = stemURL + compCode + "#rankings"

pitResponse = requests.get(pitURL, headers={"X-TBA-Auth-Key": blueAllianceToken})
pitSoup = BeautifulSoup(pitResponse.text, "html.parser")

matchResponse = requests.get(matchURL, headers={"X-TBA-Auth-Key": blueAllianceToken})
matchSoup = BeautifulSoup(matchResponse.text, "html.parser")

rankingsResponse = requests.get(rankingsURL, headers={"X-TBA-Auth-Key": blueAllianceToken})
rankingsSoup = BeautifulSoup(rankingsResponse.text, "html.parser")

# print(response.text)


'''
d = {
    "Teams":
}
'''