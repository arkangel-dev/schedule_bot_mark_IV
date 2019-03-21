import parse_data as p_data
import parse_dates as p_date
import parse_natural_language as parse_nl
import parse_cancelled_data as p_cancledd_d
from datetime import datetime

# print(pda.convertDateToDay(datetime.today()))
# print(p_data.parseSessionData(0, "wednesday"))
print(parse_nl.getFullTodayNL())

# print(p_cancledd_d.getCancelledSessions("wednesday"))