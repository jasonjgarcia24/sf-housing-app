import os
import json
import re
import calendar
import itertools

import pandas as pd

from dotenv   import load_dotenv
from requests import Session
from datetime import datetime
from pathlib  import Path

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


class MashvisorResponse():
    VERSION  = "v1.1"

    ARCHIVE_FILES = {
        "CITY-INVESTMENT-PERFORMANCE":         "city-investment-performance_data.csv",
        "LIST-NEIGHBORHOOD":                   "list-neighborhood_data.csv",
        "TOP-NEIGHBORHOOD":                    "top-neighborhood_data.csv",
        "OVERVIEW-NEIGHBORHOOD":               "overview-neighborhood_data.csv",
        "HISTORICAL-NEIGHBORHOOD-PERFORMANCE": "historical-neighborhood-performance_data.csv",
    }

    DOMAIN_SWITCH = {
        "CITY-INVESTMENT-PERFORMANCE":         lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/city/investment/{obj.state}/{obj.city}",
        "LIST-NEIGHBORHOOD":                   lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/city/neighborhoods/{obj.state}/{obj.city}",
        "TOP-NEIGHBORHOOD":                    lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/trends/neighborhoods",
        "OVERVIEW-NEIGHBORHOOD":               lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/neighborhood/{obj.id}/bar",
        "HISTORICAL-NEIGHBORHOOD-PERFORMANCE": lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/neighborhood/{obj.id}/historical/traditional",
        "DEBUG":                               lambda _:   os.path.join(os.getcwd(), "data"),
    }

    SAVE_CSV_OPTIONS = [None, "a", "w"]
    MONTH_OPTIONS    = [None] + list(itertools.chain.from_iterable(
        [{f"{m}", f"{m:02}", calendar.month_name[m], calendar.month_abbr[m]} for m in range(1, 13)]
    ))

    def __init__(self, run_type: str, state=None, city=None, id=None, page=1, items=10,
                 month=None, year=None, beds=None, save_csv=None, debug=False):

        self.__catch_value_error(run_type, "run_type", self.DOMAIN_SWITCH.keys())
        self.__catch_value_error(save_csv, "save_csv", self.SAVE_CSV_OPTIONS)
        self.__catch_value_error(month,    "month",    self.MONTH_OPTIONS)

        self.__run_type = run_type
        self.__state    = state
        self.__city     = city
        self.__id       = id
        self.__page     = page
        self.__items    = items
        self.__year     = year
        self.__month    = month
        self.__beds     = beds
        self.save_csv   = save_csv
        self.debug      = debug
        self.__request()

    @property
    def run_type(self):
        return self.__run_type.upper()

    @property
    def state(self):
        state = self.__state

        if len(state) == 2:
            return state.upper()
        elif len(state) > 2:
            return self.get_us_states_opts().get(state.lower())
        elif not state:
            return state

    @property
    def city(self):
        city = self.__city

        if city:
            return city.replace(" ", "%20")
        elif not city:
            return city

    @property
    def id(self):
        return str(self.__id)

    @property
    def page(self):
        return self.__page

    @property
    def items(self):
        return self.__items

    @property
    def date(self):
        year  = self.__year
        month = self.__month

        if year and len(str(year)) == 2:
            this_year = datetime.today().strftime("%y")
            year      = f"19{year}" if int(year) > int(this_year) else f"20{year}"

        if year and month:
            return f"{year}-{month}"
        elif year:
            return f"{year}-Jan"
        elif month:
            return f"1970-{month}"
        else:
            return None

    @property
    def month(self):
        if self.date and self.__month:
            return pd.to_datetime(self.date, infer_datetime_format=True).strftime("%m").lstrip("0")
        else:
            return None

    @property
    def year(self):
        if self.date and self.__year:
            return pd.to_datetime(self.date, infer_datetime_format=True).strftime("%Y")
        else:
            return None

    @property
    def beds(self):
        if self.__beds:
            return int(self.__beds)
        else:
            return None

    @property
    def url(self):
        if not self.debug:
            run_type = self.run_type
            domain   = self.DOMAIN_SWITCH.get(run_type)
        else:
            domain   = self.DOMAIN_SWITCH.get("DEBUG")
        
        return domain(self)

    @property
    def response(self):
        return self.__response

    @property
    def dataframe(self):
        if not self.response:
            return None
        else:
            return self.__dataframe
    
    def __request(self):
        # Using the Python requests library, make an API call to access Mashvisor
        # information.

        print(f"SOURCE   : {self.url}")
        print(f"RUN TYPE : {self.run_type}")
        print(f"DEBUG    : {self.debug}")

        endpoint_tag = self.run_type     

        # Get Mashvisor Response:
        if not self.debug:
            # Set request credentials and params
            load_dotenv()
            mashvisor_api_key = os.getenv("MASHVISOR_API_KEY")

            headers = {
                "x-api-key":  mashvisor_api_key,
            }

            parameters = {
                "state": self.state,
                "city":  self.city,
                "page":  self.page,
                "items": self.items,
                "month": self.month,
                "year":  self.year,
                "beds":  self.beds,
            }
            
            # Set url request
            params_switch = {
                "LIST-NEIGHBORHOOD":                   {},
                "TOP-NEIGHBORHOOD":                    {k: parameters[k] for k in ["state", "city", "page", "items"]},
                "OVERVIEW-NEIGHBORHOOD":               {k: parameters[k] for k in ["state",]},
                "HISTORICAL-NEIGHBORHOOD-PERFORMANCE": {k: parameters[k] for k in ["state", "month", "year", "beds"] if parameters[k]},
            }
            params  = params_switch.get(endpoint_tag)
            session = Session()
            session.headers.update(headers)

            try:
                response = session.get(self.url, params=params) if params else session.get(self.url)
                self.__response = json.loads(response.text)
            except (ConnectionError, Timeout, TooManyRedirects) as e:
                print(e)

            self.__dataframe = self.json_to_dataframe()
        
        # Get saved data:
        else:
            data_filename    = self.ARCHIVE_FILES[endpoint_tag]
            self.__response  = "DEBUG"
            self.__dataframe = pd.read_csv(Path(os.path.join(self.url, data_filename)))

        # Save dataframe to csv.
        if self.save_csv and isinstance(self.dataframe, pd.DataFrame):
            self.to_csv(mode=self.save_csv, suffix="auto")
        
    def json_to_dataframe(self):
        endpoint_tag = self.run_type
        response     = self.response

        if not isinstance(response["content"], (dict, list)):
            return None

        switch_set_df = {
            "LIST-NEIGHBORHOOD":                   lambda r: pd.DataFrame(r["content"]["results"]),
            "TOP-NEIGHBORHOOD":                    lambda r: pd.json_normalize(r["content"]["neighborhoods"]).drop(columns=["description"]),
            "OVERVIEW-NEIGHBORHOOD":               lambda r: pd.json_normalize(r["content"]).drop(columns=["description"]),
            "HISTORICAL-NEIGHBORHOOD-PERFORMANCE": lambda r: self.__parse_json_with_metadata(r["content"], "months", "averages"),
        }

        return switch_set_df.get(endpoint_tag)(response)

    @staticmethod
    def __parse_json_with_metadata(response, record: str, meta: str):
        df      = pd.json_normalize(response, record_path=record, meta=meta, record_prefix=f"{record}.")
        meta_df = pd.json_normalize(df[meta]).add_prefix(f"{meta}.")

        df.drop(columns=[meta,], inplace=True)

        return pd.concat([df, meta_df], axis=1)

    @staticmethod
    def __date_relative_to_explicit(date_str):
        if "last" in date_str:
            span  = re.match("last([0-9]+)days", date_str)
            span  = span.groups()[0]
            dates = list(pd.date_range(end=datetime.today(), periods=int(span)-1))
            dates = [d.strftime("%Y-%m-%d") for d in dates]
        elif re.fullmatch("[0-9]+-[0-9]+", str):
            s, e  = str.split("-")
            s = pd.to_datetime(s, format="%m%d%Y")
            e = pd.to_datetime(e, format="%m%d%Y")

            dates = pd.date_range(start=s, end=e, freq="D")
            dates = [d.strftime("%Y-%m-%d") for d in dates] 
        elif date_str == "today":
            dates = datetime.today().date().strftime("%Y-%m-%d")

        return dates

    def merge_df_responses(self, filename):
        df_new    = self.dataframe
        df_prev   = pd.read_csv(filename)
        df_merged = pd.concat([df_prev, df_new], axis=0)

        return df_merged

    def print_json_dump(self):
        if self.response != "DEBUG":
            print(json.dumps(self.response, indent=4, sort_keys=True))
        else:
            print("DEBUG")
    
    def to_csv(self, mode="a", suffix=""):
        if not isinstance(self.dataframe, pd.DataFrame):
            return

        self.__catch_value_error(mode, "mode", [opt for opt in self.SAVE_CSV_OPTIONS if opt])

        # Set to data archive domain: os.path.join(os.getcwd(), "data")
        endpoint_tag = self.run_type
        domain       = self.DOMAIN_SWITCH.get("DEBUG")(self)
        endpoint     = self.ARCHIVE_FILES[endpoint_tag]

        # Modify endpoints to include suffix and date if mode == "w".
        today         = "_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        endpoint, ext = os.path.splitext(endpoint)
        suffix        = "" if not suffix else "_" + suffix
        suffix        = suffix+today if mode=="w" else suffix
        endpoint      = endpoint + suffix + ext

        # Assign filename.
        filename = os.path.join(domain, endpoint)

        # If writing to file:
        # Write to file.
        if mode == "w" or not os.path.isfile(filename):
            self.dataframe.to_csv(filename, index=False)

        # If appending to file:
        # Read the existing file, concatenate with new data, and write to file.
        elif mode == "a":
            self.__dataframe = self.merge_df_responses(filename)
            self.__dataframe.to_csv(filename, index=False)
            
    @staticmethod
    def __catch_value_error(var, varname, opts):
        if var not in opts:
            raise ValueError(f"Variable '{varname}' must be one of the values in {opts}." +
                             f"'{var}' is not valid.")

    @staticmethod
    def config():
        outargs = {}

        outargs["us-states"] = {
            'alabama': 'AL',
            'alaska': 'AK',
            'american samoa': 'AS',
            'arizona': 'AZ',
            'arkansas': 'AR',
            'california': 'CA',
            'colorado': 'CO',
            'connecticut': 'CT',
            'delaware': 'DE',
            'district of columbia': 'DC',
            'florida': 'FL',
            'georgia': 'GA',
            'guam': 'GU',
            'hawaii': 'HI',
            'idaho': 'ID',
            'illinois': 'IL',
            'indiana': 'IN',
            'iowa': 'IA',
            'kansas': 'KS',
            'kentucky': 'KY',
            'louisiana': 'LA',
            'maine': 'ME',
            'maryland': 'MD',
            'massachusetts': 'MA',
            'michigan': 'MI',
            'minnesota': 'MN',
            'mississippi': 'MS',
            'missouri': 'MO',
            'montana': 'MT',
            'nebraska': 'NE',
            'nevada': 'NV',
            'new hampshire': 'NH',
            'new jersey': 'NJ',
            'new mexico': 'NM',
            'new york': 'NY',
            'north carolina': 'NC',
            'north dakota': 'ND',
            'northern mariana islands':'MP',
            'ohio': 'OH',
            'oklahoma': 'OK',
            'oregon': 'OR',
            'pennsylvania': 'PA',
            'puerto rico': 'PR',
            'rhode island': 'RI',
            'south carolina': 'SC',
            'south dakota': 'SD',
            'tennessee': 'TN',
            'texas': 'TX',
            'utah': 'UT',
            'vermont': 'VT',
            'virgin islands': 'VI',
            'virginia': 'VA',
            'washington': 'WA',
            'west virginia': 'WV',
            'wisconsin': 'WI',
            'wyoming': 'WY'
        }

        return outargs

    @staticmethod
    def get_us_states_opts():
        return MashvisorResponse.config()["us-states"]

