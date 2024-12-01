import requests
import csv
from urllib.parse import urlencode
from dataclasses import dataclass, asdict

base_url = "https://clinicaltrials.gov/api/v2/studies"
query_params = {
    "query.cond": "diabetes",
    "filter.advanced": "AREA[StartDate]2019+"
}
encoded_params = urlencode(query_params, safe="[]+")
full_url = f"{base_url}?{encoded_params}"

@dataclass
class Location:
  studyId: str
  city: str
  state: str
  country: str
  startDate: str

def get_studies(url):
  response = requests.get(url)
  data = response.json()
  studies = data.get("studies", [])
  return studies

def get_locations(studies):
  
  locations_info=[]
  
  for study in studies:
    
    studyId=study.get("protocolSection",{}).get("identificationModule",{}).get("nctId")
    startDate=study.get("protocolSection",{}).get("statusModule",{}).get("startDateStruct",{}).get("date")
    locations=study.get("protocolSection",{}).get("contactsLocationsModule", {}).get("locations",[])
    
    for location in locations:
      city=location.get("city","")
      state=location.get("state","")
      country=location.get("country","")

      new_location = Location(
        studyId=studyId,
        startDate=startDate,
        city=city,
        state=state,
        country=country
      )
      locations_info.append(asdict(new_location))

  return locations_info

def save_to_csv(locations_info, file_name="locations.csv"):
    if locations_info:
        keys = locations_info[0].keys()  # Get headers from the first dictionary
        with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(locations_info)
        print(f"Data saved to {file_name}")
    else:
        print("No data to save.")

if __name__ == "__main__":
  studies = get_studies(full_url)
  locations_info = get_locations(studies)
  save_to_csv(locations_info)

