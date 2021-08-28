from housing.mashvisor_client import MashvisorResponse

state = "Illinois"
city  = "Chicago"

top_neighborhood_data = MashvisorResponse(
    run_type="TOP-NEIGHBORHOOD",
    state=state,
    city=city,
    page=1,
    items=10,
    debug=True,
)

for id in top_neighborhood_data.dataframe["id"]:
    historical_neighborhood_data = MashvisorResponse(
        run_type="HISTORICAL-NEIGHBORHOOD-PERFORMANCE",
        state=state,
        id=id,
        year=19,
        debug=False,
    )
    breakpoint()
    historical_neighborhood_data.dataframe["id"] = id
    historical_neighborhood_data.to_csv(mode="a", suffix="auto")

breakpoint()