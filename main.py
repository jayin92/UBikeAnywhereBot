import get_data
import google_map_api
import time


cord = google_map_api.google_map_api("桃園市八德區介壽路一段936號")

all_station_info = []
all_station_availability = []


start = time.time()
get_data.get_all_station_availability(all_station_availability)
get_data.get_all_station_info(all_station_info)
print(time.time()-start)
start = time.time()

print(get_data.search(all_station_availability, all_station_info, cord, 0))

print(time.time()-start)
