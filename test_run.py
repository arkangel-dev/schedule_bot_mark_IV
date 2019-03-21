import parse_data as pd
import parse_dates as pda
import parse_natural_language as parse_nl
from datetime import datetime
from send_the_message import sendMessage

# print(pda.convertDateToDay(datetime.today()))
# print(pd.parseSessionData(0, "wednesday"))

print(parse_nl.getFullTodayNL())