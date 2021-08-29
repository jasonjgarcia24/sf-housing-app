import sys
sys.path.append(".")

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


ARCHIVE_PATH = os.path.join(os.getcwd(), "data")

ARCHIVE_FILES = {
    "CITY-INVESTMENT-PERFORMANCE":         "city-investment-performance_data.csv",
    "LIST-NEIGHBORHOOD":                   "list-neighborhood_data.csv",
    "TOP-NEIGHBORHOOD":                    "top-neighborhood_data.csv",
    "OVERVIEW-NEIGHBORHOOD":               "overview-neighborhood_data.csv",
    "HISTORICAL-NEIGHBORHOOD-PERFORMANCE": "historical-neighborhood-performance_data.csv",
}

def config():    
    normalize_func = lambda ds: (ds - ds.mean()) / ds.std()
    pos_slide_func = lambda ds: ds + abs(ds) if ds.min() < 0 or ds.std() != 0.0 else ds

    outargs = {}

    outargs["us-states"] = {
        "alabama": "AL",
        "alaska": "AK",
        "american samoa": "AS",
        "arizona": "AZ",
        "arkansas": "AR",
        "california": "CA",
        "colorado": "CO",
        "connecticut": "CT",
        "delaware": "DE",
        "district of columbia": "DC",
        "florida": "FL",
        "georgia": "GA",
        "guam": "GU",
        "hawaii": "HI",
        "idaho": "ID",
        "illinois": "IL",
        "indiana": "IN",
        "iowa": "IA",
        "kansas": "KS",
        "kentucky": "KY",
        "louisiana": "LA",
        "maine": "ME",
        "maryland": "MD",
        "massachusetts": "MA",
        "michigan": "MI",
        "minnesota": "MN",
        "mississippi": "MS",
        "missouri": "MO",
        "montana": "MT",
        "nebraska": "NE",
        "nevada": "NV",
        "new hampshire": "NH",
        "new jersey": "NJ",
        "new mexico": "NM",
        "new york": "NY",
        "north carolina": "NC",
        "north dakota": "ND",
        "northern mariana islands":"MP",
        "ohio": "OH",
        "oklahoma": "OK",
        "oregon": "OR",
        "pennsylvania": "PA",
        "puerto rico": "PR",
        "rhode island": "RI",
        "south carolina": "SC",
        "south dakota": "SD",
        "tennessee": "TN",
        "texas": "TX",
        "utah": "UT",
        "vermont": "VT",
        "virgin islands": "VI",
        "virginia": "VA",
        "washington": "WA",
        "west virginia": "WV",
        "wisconsin": "WI",
        "wyoming": "WY"
    }

    outargs["scale-definition"] = {
        "year":                                               None,
        "month":                                              None,
        "zero_room_value":                                    1 / 1000,
        "one_room_value":                                     1 / 1000,
        "two_room_value":                                     1 / 1000,
        "three_room_value":                                   1 / 1000,
        "four_room_value":                                    1 / 1000,
        "averages.zero_room_value":                           1 / 1000,
        "averages.one_room_value":                            1 / 1000,
        "averages.two_room_value":                            1 / 1000,
        "averages.three_room_value":                          1 / 1000,
        "averages.four_room_value":                           1 / 1000,
        "id":                                                 None,
        "city":                                               None,
        "latitude":                                           None,
        "longitude":                                          None,
        "name":                                               None,
        "state":                                              None,
        "county":                                             None,
        "is_village":                                         None,
        "occupancy":                                          None,
        "total_listing":                                      None,
        "airbnb_listings":                                    None,
        "single_home_value":                                  1 / 100000,
        "single_home_value_formatted":                        None,
        "mashMeter":                                          1 / 10,
        "description":                                        None,
        "image":                                              None,
        "walkscore":                                          1 / 100,
        "num_of_properties":                                  1 / 100,
        "num_of_airbnb_properties":                           1 / 100,
        "num_of_traditional_properties":                      1 / 100,
        "median_price":                                       1 / 100000,
        "price_per_sqft":                                     1 / 100,
        "mashMeterStars":                                     None,
        "avg_occupancy":                                      None,
        "strategy":                                           None,
        "airbnb_rental.roi":                                  None,
        "airbnb_rental.cap_rate":                             None,
        "airbnb_rental.rental_income":                        1 / 1000,
        "airbnb_rental.rental_income_change":                 None,
        "airbnb_rental.rental_income_change_percentage":      None,
        "airbnb_rental.night_price":                          1 / 100,
        "airbnb_rental.occupancy":                            None,
        "airbnb_rental.occupancy_change":                     None,
        "airbnb_rental.occupancy_change_percentage":          None,
        "airbnb_rental.insights.bedrooms.slope":              None,
        "airbnb_rental.insights.bedrooms.RSquare":            None,
        "airbnb_rental.insights.price.slope":                 None,
        "airbnb_rental.insights.price.RSquare":               None,
        "airbnb_rental.insights.stars_rate.slope":            None,
        "airbnb_rental.insights.stars_rate.RSquare":          None,
        "airbnb_rental.insights.bathrooms.slope":             None,
        "airbnb_rental.insights.bathrooms.RSquare":           None,
        "airbnb_rental.insights.beds.slope":                  None,
        "airbnb_rental.insights.beds.RSquare":                None,
        "airbnb_rental.insights.reviews_count.slope":         None,
        "airbnb_rental.insights.reviews_count.RSquare":       None,
        "traditional_rental.roi":                             None,
        "traditional_rental.cap_rate":                        None,
        "traditional_rental.rental_income":                   1 / 1000,
        "traditional_rental.rental_income_change":            None,
        "traditional_rental.rental_income_change_percentage": None,
        "traditional_rental.night_price":                     1 / 100,
        "traditional_rental.occupancy":                       None,
        "traditional_rental.occupancy_change":                None,
    }

    outargs["scale-function"] = {
        "year":                                               lambda ds: ds * outargs["scale-definition"]["year"],
        "month":                                              lambda ds: ds * outargs["scale-definition"]["month"],
        "zero_room_value":                                    lambda ds: ds * outargs["scale-definition"]["zero_room_value"],
        "one_room_value":                                     lambda ds: ds * outargs["scale-definition"]["one_room_value"],
        "two_room_value":                                     lambda ds: ds * outargs["scale-definition"]["two_room_value"],
        "three_room_value":                                   lambda ds: ds * outargs["scale-definition"]["three_room_value"],
        "four_room_value":                                    lambda ds: ds * outargs["scale-definition"]["four_room_value"],
        "averages.zero_room_value":                           lambda ds: ds * outargs["scale-definition"]["averages.zero_room_value"],
        "averages.one_room_value":                            lambda ds: ds * outargs["scale-definition"]["averages.one_room_value"],
        "averages.two_room_value":                            lambda ds: ds * outargs["scale-definition"]["averages.two_room_value"],
        "averages.three_room_value":                          lambda ds: ds * outargs["scale-definition"]["averages.three_room_value"],
        "averages.four_room_value":                           lambda ds: ds * outargs["scale-definition"]["averages.four_room_value"],
        "id":                                                 lambda ds: ds * outargs["scale-definition"]["id"],
        "city":                                               lambda ds: ds * outargs["scale-definition"]["city"],
        "latitude":                                           lambda ds: ds * outargs["scale-definition"]["latitude"],
        "longitude":                                          lambda ds: ds * outargs["scale-definition"]["longitude"],
        "name":                                               lambda ds: ds * outargs["scale-definition"]["name"],
        "state":                                              lambda ds: ds * outargs["scale-definition"]["state"],
        "county":                                             lambda ds: ds * outargs["scale-definition"]["county"],
        "is_village":                                         lambda ds: ds * outargs["scale-definition"]["is_village"],
        "occupancy":                                          lambda ds: ds * outargs["scale-definition"]["occupancy"],
        "total_listing":                                      lambda ds: ds * outargs["scale-definition"]["total_listing"],
        "airbnb_listings":                                    lambda ds: ds * outargs["scale-definition"]["airbnb_listings"],
        "single_home_value":                                  lambda ds: ds * outargs["scale-definition"]["single_home_value"],
        "single_home_value_formatted":                        lambda ds: ds * outargs["scale-definition"]["single_home_value_formatted"],
        "mashMeter":                                          lambda ds: ds * outargs["scale-definition"]["mashMeter"],
        "description":                                        lambda ds: ds * outargs["scale-definition"]["description"],
        "image":                                              lambda ds: ds * outargs["scale-definition"]["image"],
        "walkscore":                                          lambda ds: pos_slide_func(normalize_func(ds * outargs["scale-definition"]["walkscore"])),
        "num_of_properties":                                  lambda ds: ds * outargs["scale-definition"]["num_of_properties"],
        "num_of_airbnb_properties":                           lambda ds: ds * outargs["scale-definition"]["num_of_airbnb_properties"],
        "num_of_traditional_properties":                      lambda ds: ds * outargs["scale-definition"]["num_of_traditional_properties"],
        "median_price":                                       lambda ds: ds * outargs["scale-definition"]["median_price"],
        "price_per_sqft":                                     lambda ds: ds * outargs["scale-definition"]["price_per_sqft"],
        "mashMeterStars":                                     lambda ds: ds * outargs["scale-definition"]["mashMeterStars"],
        "avg_occupancy":                                      lambda ds: ds * outargs["scale-definition"]["avg_occupancy"],
        "strategy":                                           lambda ds: ds * outargs["scale-definition"]["strategy"],
        "airbnb_rental.roi":                                  lambda ds: ds * outargs["scale-definition"]["airbnb_rental.roi"],
        "airbnb_rental.cap_rate":                             lambda ds: ds * outargs["scale-definition"]["airbnb_rental.cap_rate"],
        "airbnb_rental.rental_income":                        lambda ds: ds * outargs["scale-definition"]["airbnb_rental.rental_income"],
        "airbnb_rental.rental_income_change":                 lambda ds: ds * outargs["scale-definition"]["airbnb_rental.rental_income_change"],
        "airbnb_rental.rental_income_change_percentage":      lambda ds: ds * outargs["scale-definition"]["airbnb_rental.rental_income_change_percentage"],
        "airbnb_rental.night_price":                          lambda ds: ds * outargs["scale-definition"]["airbnb_rental.night_price"],
        "airbnb_rental.occupancy":                            lambda ds: ds * outargs["scale-definition"]["airbnb_rental.occupancy"],
        "airbnb_rental.occupancy_change":                     lambda ds: ds * outargs["scale-definition"]["airbnb_rental.occupancy_change"],
        "airbnb_rental.occupancy_change_percentage":          lambda ds: ds * outargs["scale-definition"]["airbnb_rental.occupancy_change_percentage"],
        "airbnb_rental.insights.bedrooms.slope":              lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.bedrooms.slope"],
        "airbnb_rental.insights.bedrooms.RSquare":            lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.bedrooms.RSquare"],
        "airbnb_rental.insights.price.slope":                 lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.price.slope"],
        "airbnb_rental.insights.price.RSquare":               lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.price.RSquare"],
        "airbnb_rental.insights.stars_rate.slope":            lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.stars_rate.slope"],
        "airbnb_rental.insights.stars_rate.RSquare":          lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.stars_rate.RSquare"],
        "airbnb_rental.insights.bathrooms.slope":             lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.bathrooms.slope"],
        "airbnb_rental.insights.bathrooms.RSquare":           lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.bathrooms.RSquare"],
        "airbnb_rental.insights.beds.slope":                  lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.beds.slope"],
        "airbnb_rental.insights.beds.RSquare":                lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.beds.RSquare"],
        "airbnb_rental.insights.reviews_count.slope":         lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.reviews_count.slope"],
        "airbnb_rental.insights.reviews_count.RSquare":       lambda ds: ds * outargs["scale-definition"]["airbnb_rental.insights.reviews_count.RSquare"],
        "traditional_rental.roi":                             lambda ds: ds * outargs["scale-definition"]["traditional_rental.roi"],
        "traditional_rental.cap_rate":                        lambda ds: ds * outargs["scale-definition"]["traditional_rental.cap_rate"],
        "traditional_rental.rental_income":                   lambda ds: ds * outargs["scale-definition"]["traditional_rental.rental_income"],
        "traditional_rental.rental_income_change":            lambda ds: ds * outargs["scale-definition"]["traditional_rental.rental_income_change"],
        "traditional_rental.rental_income_change_percentage": lambda ds: ds * outargs["scale-definition"]["traditional_rental.rental_income_change_percentage"],
        "traditional_rental.night_price":                     lambda ds: ds * outargs["scale-definition"]["traditional_rental.night_price"],
        "traditional_rental.occupancy":                       lambda ds: ds * outargs["scale-definition"]["traditional_rental.occupancy"],
        "traditional_rental.occupancy_change":                lambda ds: ds * outargs["scale-definition"]["traditional_rental.occupancy_change"],
    }

    return outargs

class MashvisorResponse():
    VERSION  = "v1.1"

    DOMAIN_SWITCH = {
        "CITY-INVESTMENT-PERFORMANCE":         lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/city/investment/{obj.state}/{obj.city}",
        "LIST-NEIGHBORHOOD":                   lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/city/neighborhoods/{obj.state}/{obj.city}",
        "TOP-NEIGHBORHOOD":                    lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/trends/neighborhoods",
        "OVERVIEW-NEIGHBORHOOD":               lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/neighborhood/{obj.id}/bar",
        "HISTORICAL-NEIGHBORHOOD-PERFORMANCE": lambda obj: f"https://api.mashvisor.com/{obj.VERSION}/client/neighborhood/{obj.id}/historical/traditional",
        "DEBUG":                               lambda _:   ARCHIVE_PATH,
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
                "ds-api-key":  mashvisor_api_key,
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
            data_filename    = ARCHIVE_FILES[endpoint_tag]
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
        endpoint     = ARCHIVE_FILES[endpoint_tag]

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
    def get_us_states_opts():
        return config()["us-states"].keys()

class MashvisorNeighborhoodParser():
    FIND_COLS_FUNC = lambda obj, sub:   [col for col in obj.__columns if sub in col]

    def __init__(self):
        self.df        = self.__get_df()
        self.__columns = self.df.columns.to_list()
        
        self.__drop_columns()
        self.__clean_column_names()
        self.__scale_columns()
        self.__set_neighborhood_df()

    @property
    def dropped_columns(self):
        duplicate_cols = [self.FIND_COLS_FUNC(sub) for sub in [".list_neighborhood", ".top_neighborhood", ".overview_neighborhood"]]
        duplicate_cols = [col for sub in duplicate_cols for col in sub]

        cols_to_remove = [
            "investment_rentals.airbnb_rental.roi",
            "investment_rentals.airbnb_rental.cap_rate",
            "investment_rentals.airbnb_rental.rental_income",
            "investment_rentals.traditional_rental.roi",
            "investment_rentals.traditional_rental.cap_rate",
            "investment_rentals.traditional_rental.rental_income",
            "single_home_value_formatted",
        ]

        return duplicate_cols + cols_to_remove

    @property
    def cleaned_column_dict(self):
        months_cols        = self.FIND_COLS_FUNC("months")
        cleaned_month_cols = {col: col.replace("months.", "") for col in months_cols}

        return cleaned_month_cols

    def __get_df(self):
        historical_neighborhood_df = pd.read_csv(os.path.join(ARCHIVE_PATH, ARCHIVE_FILES["HISTORICAL-NEIGHBORHOOD-PERFORMANCE"]))
        list_neighborhood_df       = pd.read_csv(os.path.join(ARCHIVE_PATH, ARCHIVE_FILES["LIST-NEIGHBORHOOD"]))
        top_neighborhood_df        = pd.read_csv(os.path.join(ARCHIVE_PATH, ARCHIVE_FILES["TOP-NEIGHBORHOOD"]))
        overview_neighborhood_df   = pd.read_csv(os.path.join(ARCHIVE_PATH, ARCHIVE_FILES["OVERVIEW-NEIGHBORHOOD"]))

        df = historical_neighborhood_df.join(
            list_neighborhood_df.set_index("id"),
            on="id",
            how="left",
            rsuffix=".list_neighborhood"
        )

        df = df.join(
            top_neighborhood_df.set_index("id"),
            on="id",
            how="left",
            rsuffix=".top_neighborhood"
        )

        df = df.join(
            overview_neighborhood_df.set_index("id"),
            on="id",
            how="left",
            rsuffix=".overview_neighborhood"
        )

        return df

    def __drop_columns(self):
        self.df.drop(columns=self.dropped_columns, inplace=True)

    def __clean_column_names(self):
        self.df.rename(columns=self.cleaned_column_dict, inplace=True)

    def __scale_columns(self):
        for col in self.df.columns:
            if config()["scale-definition"][col]:
                self.df[col] = config()["scale-function"][col](self.df[col])

    def __set_neighborhood_df(self):
        self.df = self.df.groupby("name").mean()

