import challonge
import sys
import re
import datetime

username = sys.argv[1]
api_key = sys.argv[2]
url = sys.argv[3]
subdomain = None
try:
    subdomain = sys.argv[4]
    fullurl = f"{subdomain}-{url}"
except:
    subdomain = None 
    fullurl = url

challonge.set_credentials(username, api_key)
print("Fetching current tournament...")
current = challonge.tournaments.show(fullurl)
print("Found!")
print(current["start_at"])
currentNr = -1;
print("Checking if the name has a number in it...")
format = re.match("^([^0-9]*)([1-9][0-9]+)([^0-9]*)$", current["name"]).groups()
date = current["start_at"] + datetime.timedelta(days=7)
try:
    print(f"Number found: {format[0]}({format[1]}){format[2]}")
    currentNr = int(format[1])
except:
    print("No number in name found to base format on. Please input a numbered tournament series with no other numbers anywhere else")
if currentNr != -1:
    challonge.tournaments.update(fullurl, url=f"{url}{currentNr}")
    challonge.tournaments.create(url=url, name=f"{format[0]}{currentNr + 1}{format[2]}", subdomain=subdomain, tournament_type=current["tournament_type"], description=current["description"], start_at=date)
print(f"Executed! Created {format[0]}{currentNr + 1}{format[2]} and updated {format[0]}{currentNr}{format[2]}!")