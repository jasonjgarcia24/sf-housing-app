from housing.mashvisor_client import MashvisorResponse

state = "Illinois"
city  = "Chicago"

top_neighborhood_data = MashvisorResponse(
    state=state,
    city=city,
    run_type="TOP-NEIGHBORHOOD",
    items=10,
    debug=True)

for id in top_neighborhood_data.dataframe["id"]:
    overview_neighborhood_data = MashvisorResponse(
        run_type="OVERVIEW-NEIGHBORHOOD",
        state=state,
        id=id,
        save_csv="a",
        debug=False)


breakpoint()