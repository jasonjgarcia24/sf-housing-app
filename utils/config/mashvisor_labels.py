import re


UNIT_FUNC                  = lambda u:  (f" ({u})" if u else "")
SINGLE_WORD_FUNC           = lambda s, u: f"{s[0].upper()}{s[1:]}" + UNIT_FUNC(u)
MULTI_WORD_FUNC            = lambda s, u: " ".join([f"{x[0].upper()}{x[1:]}" for x in s.split("_")]) + UNIT_FUNC(u)
SINGLE_HDR_MULTI_WORD_FUNC = lambda s, u: " ".join([f"{x[0].upper()}{x[1:]}" for x in re.split("_{1}|\.{1}|_+", s)]) + UNIT_FUNC(u)
MULTI_HDR_MULTI_WORD_FUNC  = lambda s, u: " ".join([f"{x[0].upper()}{x[1:]}" for x in re.split("_{1}|\.{2}|_+|\.{1}", s)]) + UNIT_FUNC(u)
EXPLICIT_FUNC              = lambda s, u: s + UNIT_FUNC(u)


def get_label(col: str, unit=""):
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

    return switch_label.get(col)(col, unit)    

