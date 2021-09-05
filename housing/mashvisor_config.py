import re
import math
import numbers

import pandas as pd

from utils.string_ops import line_break_split


def us_states(state: str):
    switch_us_states = {
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

    return switch_us_states.get(state.lower())


def scale_definition(col: str):
    switch_scale_definition = {
        "year":                                               {"value": 1,          "text": ""},
        "month":                                              {"value": 1,          "text": ""},
        "zero_room_value":                                    {"value": 1 / 1000,   "text": "Thousands"},
        "one_room_value":                                     {"value": 1 / 1000,   "text": "Thousands"},
        "two_room_value":                                     {"value": 1 / 1000,   "text": "Thousands"},
        "three_room_value":                                   {"value": 1 / 1000,   "text": "Thousands"},
        "four_room_value":                                    {"value": 1 / 1000,   "text": "Thousands"},
        "averages.zero_room_value":                           {"value": 1 / 1000,   "text": "Thousands"},
        "averages.one_room_value":                            {"value": 1 / 1000,   "text": "Thousands"},
        "averages.two_room_value":                            {"value": 1 / 1000,   "text": "Thousands"},
        "averages.three_room_value":                          {"value": 1 / 1000,   "text": "Thousands"},
        "averages.four_room_value":                           {"value": 1 / 1000,   "text": "Thousands"},
        "id":                                                 {"value": 1,          "text": ""},
        "city":                                               {"value": 1,          "text": ""},
        "latitude":                                           {"value": 1,          "text": ""},
        "longitude":                                          {"value": 1,          "text": ""},
        "name":                                               {"value": 1,          "text": ""},
        "state":                                              {"value": 1,          "text": ""},
        "county":                                             {"value": 1,          "text": ""},
        "is_village":                                         {"value": 1,          "text": ""},
        "occupancy":                                          {"value": 1,          "text": ""},
        "total_listing":                                      {"value": 1,          "text": ""},
        "airbnb_listings":                                    {"value": 1,          "text": ""},
        "single_home_value":                                  {"value": 1 / 100000, "text": "Hundred-thousands"},
        "single_home_value_formatted":                        {"value": 1,          "text": ""},
        "mashMeter":                                          {"value": 1 / 10,     "text": "Tens"},
        "description":                                        {"value": 1,          "text": ""},
        "image":                                              {"value": 1,          "text": ""},
        "walkscore":                                          {"value": 1 / 100,    "text": "Hundreds - +Slide"},
        "num_of_properties":                                  {"value": 1 / 100,    "text": "Hundreds"},
        "num_of_airbnb_properties":                           {"value": 1 / 100,    "text": "Hundreds"},
        "num_of_traditional_properties":                      {"value": 1 / 100,    "text": "Hundreds"},
        "median_price":                                       {"value": 1 / 100000, "text": "Hundred-thousands"},
        "price_per_sqft":                                     {"value": 1 / 100,    "text": "Hundreds"},
        "mashMeterStars":                                     {"value": 1,          "text": ""},
        "avg_occupancy":                                      {"value": 1,          "text": ""},
        "strategy":                                           {"value": 1,          "text": ""},
        "airbnb_rental.roi":                                  {"value": 1,          "text": ""},
        "airbnb_rental.cap_rate":                             {"value": 1,          "text": ""},
        "airbnb_rental.rental_income":                        {"value": 1 / 1000,   "text": "Thousands"},
        "airbnb_rental.rental_income_change":                 {"value": 1,          "text": "Categorized"},
        "airbnb_rental.rental_income_change_percentage":      {"value": 1,          "text": "+Slide"},
        "airbnb_rental.night_price":                          {"value": 1 / 100,    "text": "Hundreds"},
        "airbnb_rental.occupancy":                            {"value": 1,          "text": ""},
        "airbnb_rental.occupancy_change":                     {"value": 1,          "text": "Categorized"},
        "airbnb_rental.occupancy_change_percentage":          {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.bedrooms.slope":              {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.bedrooms.RSquare":            {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.price.slope":                 {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.price.RSquare":               {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.stars_rate.slope":            {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.stars_rate.RSquare":          {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.bathrooms.slope":             {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.bathrooms.RSquare":           {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.beds.slope":                  {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.beds.RSquare":                {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.reviews_count.slope":         {"value": 1,          "text": "+Slide"},
        "airbnb_rental.insights.reviews_count.RSquare":       {"value": 1,          "text": "+Slide"},
        "traditional_rental.roi":                             {"value": 1,          "text": ""},
        "traditional_rental.cap_rate":                        {"value": 1,          "text": ""},
        "traditional_rental.rental_income":                   {"value": 1 / 1000,   "text": "Thousands"},
        "traditional_rental.rental_income_change":            {"value": 1,          "text": "Categorized"},
        "traditional_rental.rental_income_change_percentage": {"value": 1,          "text": "+Slide"},
        "traditional_rental.night_price":                     {"value": 1 / 100,    "text": "Hundreds"},
        "traditional_rental.occupancy":                       {"value": 1,          "text": ""},
        "traditional_rental.occupancy_change":                {"value": 1,          "text": "Categorized"},
    }

    return switch_scale_definition.get(col)


def normalize(ds: pd.Series):
    return (ds - ds.mean()) / ds.std() if ds.std() != 0.0 else ds


def pos_slide(ds: pd.Series):
    return ds + abs(ds) if (ds.min() < 0 or ds.std() != 0.0) and isinstance(ds[0], numbers.Number) else ds


def categorize(ds: pd.Series):
    return pd.Categorical(ds).codes


def scale_function(ds: pd.Series):
    switch_scale_function = {
        "year":                                               lambda ds: ds * scale_definition("year")["value"],
        "month":                                              lambda ds: ds * scale_definition("month")["value"],
        "zero_room_value":                                    lambda ds: ds * scale_definition("zero_room_value")["value"],
        "one_room_value":                                     lambda ds: ds * scale_definition("one_room_value")["value"],
        "two_room_value":                                     lambda ds: ds * scale_definition("two_room_value")["value"],
        "three_room_value":                                   lambda ds: ds * scale_definition("three_room_value")["value"],
        "four_room_value":                                    lambda ds: ds * scale_definition("four_room_value")["value"],
        "averages.zero_room_value":                           lambda ds: ds * scale_definition("averages.zero_room_value")["value"],
        "averages.one_room_value":                            lambda ds: ds * scale_definition("averages.one_room_value")["value"],
        "averages.two_room_value":                            lambda ds: ds * scale_definition("averages.two_room_value")["value"],
        "averages.three_room_value":                          lambda ds: ds * scale_definition("averages.three_room_value")["value"],
        "averages.four_room_value":                           lambda ds: ds * scale_definition("averages.four_room_value")["value"],
        "id":                                                 lambda ds: ds * scale_definition("id")["value"],
        "city":                                               lambda ds: ds * scale_definition("city")["value"],
        "latitude":                                           lambda ds: ds * scale_definition("latitude")["value"],
        "longitude":                                          lambda ds: ds * scale_definition("longitude")["value"],
        "name":                                               lambda ds: ds * scale_definition("name")["value"],
        "state":                                              lambda ds: ds * scale_definition("state")["value"],
        "county":                                             lambda ds: ds * scale_definition("county")["value"],
        "is_village":                                         lambda ds: ds * scale_definition("is_village")["value"],
        "occupancy":                                          lambda ds: ds * scale_definition("occupancy")["value"],
        "total_listing":                                      lambda ds: ds * scale_definition("total_listing")["value"],
        "airbnb_listings":                                    lambda ds: ds * scale_definition("airbnb_listings")["value"],
        "single_home_value":                                  lambda ds: ds * scale_definition("single_home_value")["value"],
        "single_home_value_formatted":                        lambda ds: ds * scale_definition("single_home_value_formatted")["value"],
        "mashMeter":                                          lambda ds: ds * scale_definition("mashMeter")["value"],
        "description":                                        lambda ds: ds * scale_definition("description")["value"],
        "image":                                              lambda ds: ds * scale_definition("image")["value"],
        "walkscore":                                          lambda ds: pos_slide(ds * scale_definition("walkscore")["value"]),
        "num_of_properties":                                  lambda ds: ds * scale_definition("num_of_properties")["value"],
        "num_of_airbnb_properties":                           lambda ds: ds * scale_definition("num_of_airbnb_properties")["value"],
        "num_of_traditional_properties":                      lambda ds: ds * scale_definition("num_of_traditional_properties")["value"],
        "median_price":                                       lambda ds: ds * scale_definition("median_price")["value"],
        "price_per_sqft":                                     lambda ds: ds * scale_definition("price_per_sqft")["value"],
        "mashMeterStars":                                     lambda ds: ds * scale_definition("mashMeterStars")["value"],
        "avg_occupancy":                                      lambda ds: ds * scale_definition("avg_occupancy")["value"],
        "strategy":                                           lambda ds: ds * scale_definition("strategy")["value"],
        "airbnb_rental.roi":                                  lambda ds: ds * scale_definition("airbnb_rental.roi")["value"],
        "airbnb_rental.cap_rate":                             lambda ds: ds * scale_definition("airbnb_rental.cap_rate")["value"],
        "airbnb_rental.rental_income":                        lambda ds: ds * scale_definition("airbnb_rental.rental_income")["value"],
        "airbnb_rental.rental_income_change":                 lambda ds: pos_slide(categorize(ds * scale_definition("airbnb_rental.rental_income_change")["value"])),
        "airbnb_rental.rental_income_change_percentage":      lambda ds: pos_slide(ds * scale_definition("airbnb_rental.rental_income_change_percentage")["value"]),
        "airbnb_rental.night_price":                          lambda ds: ds * scale_definition("airbnb_rental.night_price")["value"],
        "airbnb_rental.occupancy":                            lambda ds: ds * scale_definition("airbnb_rental.occupancy")["value"],
        "airbnb_rental.occupancy_change":                     lambda ds: pos_slide(categorize(ds * scale_definition("airbnb_rental.occupancy_change")["value"])),
        "airbnb_rental.occupancy_change_percentage":          lambda ds: pos_slide(ds * scale_definition("airbnb_rental.occupancy_change_percentage")["value"]),
        "airbnb_rental.insights.bedrooms.slope":              lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.bedrooms.slope")["value"]),
        "airbnb_rental.insights.bedrooms.RSquare":            lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.bedrooms.RSquare")["value"]),
        "airbnb_rental.insights.price.slope":                 lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.price.slope")["value"]),
        "airbnb_rental.insights.price.RSquare":               lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.price.RSquare")["value"]),
        "airbnb_rental.insights.stars_rate.slope":            lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.stars_rate.slope")["value"]),
        "airbnb_rental.insights.stars_rate.RSquare":          lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.stars_rate.RSquare")["value"]),
        "airbnb_rental.insights.bathrooms.slope":             lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.bathrooms.slope")["value"]),
        "airbnb_rental.insights.bathrooms.RSquare":           lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.bathrooms.RSquare")["value"]),
        "airbnb_rental.insights.beds.slope":                  lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.beds.slope")["value"]),
        "airbnb_rental.insights.beds.RSquare":                lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.beds.RSquare")["value"]),
        "airbnb_rental.insights.reviews_count.slope":         lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.reviews_count.slope")["value"]),
        "airbnb_rental.insights.reviews_count.RSquare":       lambda ds: pos_slide(ds * scale_definition("airbnb_rental.insights.reviews_count.RSquare")["value"]),
        "traditional_rental.roi":                             lambda ds: ds * scale_definition("traditional_rental.roi")["value"],
        "traditional_rental.cap_rate":                        lambda ds: ds * scale_definition("traditional_rental.cap_rate")["value"],
        "traditional_rental.rental_income":                   lambda ds: ds * scale_definition("traditional_rental.rental_income")["value"],
        "traditional_rental.rental_income_change":            lambda ds: pos_slide(categorize(ds * scale_definition("traditional_rental.rental_income_change")["value"])),
        "traditional_rental.rental_income_change_percentage": lambda ds: pos_slide(ds * scale_definition("traditional_rental.rental_income_change_percentage")["value"]),
        "traditional_rental.night_price":                     lambda ds: ds * scale_definition("traditional_rental.night_price")["value"],
        "traditional_rental.occupancy":                       lambda ds: ds * scale_definition("traditional_rental.occupancy")["value"],
        "traditional_rental.occupancy_change":                lambda ds: pos_slide(categorize(ds * scale_definition("traditional_rental.occupancy_change")["value"])),
    }

    return switch_scale_function.get(ds.name)(ds)


def set_acronym(label):
    acronym_dict = {
        "Avg":  "Average",
        "Id":   "ID",
        "Roi":  "ROI",
        "Sqft": "SqFt"
    }

    return " ".join([acronym_dict.get(s) if s in acronym_dict.keys() else s for s in label.split()])


def get_label(col: str, unit="", width=None, return_type="value"):
    UNIT_FUNC                  = lambda u:    line_break_split(f" ({u})" if u else "", width)
    SINGLE_WORD_FUNC           = lambda s, u: line_break_split(set_acronym(f"{s[0].upper()}{s[1:]}" + UNIT_FUNC(u)), width)
    MULTI_WORD_FUNC            = lambda s, u: line_break_split(set_acronym(" ".join([f"{x[0].upper()}{x[1:]}" for x in s.split("_")]) + UNIT_FUNC(u)), width)
    SINGLE_HDR_MULTI_WORD_FUNC = lambda s, u: line_break_split(set_acronym(" ".join([f"{x[0].upper()}{x[1:]}" for x in re.split("_{1}|\.{1}|_+", s)]) + UNIT_FUNC(u)), width)
    MULTI_HDR_MULTI_WORD_FUNC  = lambda s, u: line_break_split(set_acronym(" ".join([f"{x[0].upper()}{x[1:]}" for x in re.split("_{1}|\.{2}|_+|\.{1}", s)]) + UNIT_FUNC(u)), width)
    EXPLICIT_FUNC              = lambda s, u: line_break_split(s + UNIT_FUNC(u), width)

    switch_label = {
        "year":                                               lambda s, u: SINGLE_WORD_FUNC(s, u),
        "month":                                              lambda s, u: SINGLE_WORD_FUNC(s, u),
        "zero_room_value":                                    lambda s, u: MULTI_WORD_FUNC(s, u),
        "one_room_value":                                     lambda s, u: MULTI_WORD_FUNC(s, u),
        "two_room_value":                                     lambda s, u: MULTI_WORD_FUNC(s, u),
        "three_room_value":                                   lambda s, u: MULTI_WORD_FUNC(s, u),
        "four_room_value":                                    lambda s, u: MULTI_WORD_FUNC(s, u),
        "averages.zero_room_value":                           lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "averages.one_room_value":                            lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "averages.two_room_value":                            lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "averages.three_room_value":                          lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "averages.four_room_value":                           lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "id":                                                 lambda s, u: SINGLE_WORD_FUNC(s, u),
        "city":                                               lambda s, u: SINGLE_WORD_FUNC(s, u),
        "latitude":                                           lambda s, u: SINGLE_WORD_FUNC(s, u),
        "longitude":                                          lambda s, u: SINGLE_WORD_FUNC(s, u),
        "name":                                               lambda s, u: EXPLICIT_FUNC("Neighborhood", u),
        "state":                                              lambda s, u: SINGLE_WORD_FUNC(s, u),
        "county":                                             lambda s, u: SINGLE_WORD_FUNC(s, u),
        "is_village":                                         lambda s, u: MULTI_WORD_FUNC(s, u),
        "occupancy":                                          lambda s, u: SINGLE_WORD_FUNC(s, u),
        "total_listing":                                      lambda s, u: MULTI_WORD_FUNC(s, u),
        "airbnb_listings":                                    lambda s, u: MULTI_WORD_FUNC(s, u),
        "single_home_value":                                  lambda s, u: MULTI_WORD_FUNC(s, u),
        "single_home_value_formatted":                        lambda s, u: MULTI_WORD_FUNC(s, u),
        "mashMeter":                                          lambda _, u: EXPLICIT_FUNC("Mash Meter", u),
        "description":                                        lambda s, u: SINGLE_WORD_FUNC(s, u),
        "image":                                              lambda s, u: SINGLE_WORD_FUNC(s, u),
        "walkscore":                                          lambda _, u: EXPLICIT_FUNC("Walk Score", u),
        "num_of_properties":                                  lambda s, u: MULTI_WORD_FUNC(s, u),
        "num_of_airbnb_properties":                           lambda s, u: MULTI_WORD_FUNC(s, u),
        "num_of_traditional_properties":                      lambda s, u: MULTI_WORD_FUNC(s, u),
        "median_price":                                       lambda s, u: MULTI_WORD_FUNC(s, u),
        "price_per_sqft":                                     lambda s, u: MULTI_WORD_FUNC(s, u),
        "mashMeterStars":                                     lambda _, u: EXPLICIT_FUNC("Mash Meter Stars", u),
        "avg_occupancy":                                      lambda s, u: MULTI_WORD_FUNC(s, u),
        "strategy":                                           lambda s, u: SINGLE_WORD_FUNC(s, u),
        "airbnb_rental.roi":                                  lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.cap_rate":                             lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.rental_income":                        lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.rental_income_change":                 lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.rental_income_change_percentage":      lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.night_price":                          lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.occupancy":                            lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.occupancy_change":                     lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.occupancy_change_percentage":          lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.bedrooms.slope":              lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.bedrooms.RSquare":            lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.price.slope":                 lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.price.RSquare":               lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.stars_rate.slope":            lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.stars_rate.RSquare":          lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.bathrooms.slope":             lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.bathrooms.RSquare":           lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.beds.slope":                  lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.beds.RSquare":                lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.reviews_count.slope":         lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "airbnb_rental.insights.reviews_count.RSquare":       lambda s, u: MULTI_HDR_MULTI_WORD_FUNC(s, u),
        "traditional_rental.roi":                             lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "traditional_rental.cap_rate":                        lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "traditional_rental.rental_income":                   lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "traditional_rental.rental_income_change":            lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "traditional_rental.rental_income_change_percentage": lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "traditional_rental.night_price":                     lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "traditional_rental.occupancy":                       lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
        "traditional_rental.occupancy_change":                lambda s, u: SINGLE_HDR_MULTI_WORD_FUNC(s, u),
    }

    label = None

    if return_type == "value":
        label = switch_label.get(col)(col, unit)
    elif return_type == "key":
        for key, val in switch_label.items():
            label = key if val(key, "") == col else label

    return label


def base_scale(df: pd.DataFrame, col: str, base=11):
        data = df.index if col == df.index.name else df[col]
        
        if not isinstance(data[0], numbers.Number) or data.std() == 0.0:
            return data

        restored_data = data / scale_definition(col)["value"]
        scale         = 10 ** (int(math.log(restored_data.max(), base)) - 1)
        values        = restored_data / scale

        return values

