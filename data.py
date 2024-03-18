import pandas as pd
from bs4 import BeautifulSoup
import requests
import tbapy
from docx import Document

document = Document()


blueAllianceToken = "PiqFQSWcSw9DgmNEhNDviFRxzfTOa8Bp2l3g5nX42ngqqi9zlaLnzizwt2gtDQQQ"


stemURL = "https://www.thebluealliance.com/event/"
compCode = "2024wimi"
finalURL = stemURL + compCode

response = requests.get(finalURL, headers={"X-TBA-Auth-Key": blueAllianceToken})
document.add_paragraph(response.text)

document.save('parseBlueAlliance.docx')
soup = BeautifulSoup(response.text, "html.parser")
# print(response.text)


'''
d = {
    "Teams":
}
'''