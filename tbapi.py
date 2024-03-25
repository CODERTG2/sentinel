import tbapy

import constants

tba = tbapy.TBA(constants.blueAllianceToken)
print(tba.event_matches(event="2024wimi"))
