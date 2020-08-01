import urllib3
import json
import folium
from folium import plugins as plg

if __name__ == "__main__":
	# create a pool manager 
	http_req = urllib3.PoolManager(num_pools=10)
	# url to get the json file
	url_json = "http://api.open-notify.org/iss-now.json"
	# sending a GET request 
	resp = http_req.request('GET', url_json)
	# store the result as dict object
	loc_dic = json.loads(resp.data.decode('utf8'));
	# print the result
	print("[*] Responce message : ",loc_dic)
	# get the long iis position
	iss_long = float(loc_dic['iss_position']['longitude'])
	print("[*] Longitude : {:.2f}".format(iss_long))
	# get the lat iis position
	iss_lat = float(loc_dic['iss_position']['latitude'])
	print("[*] Latitude : {:.2f}".format(iss_lat))
	# plot on a folium map
	# create a folium map object
	world_map = folium.Map(min_zoom=1.5, max_bounds=True, tiles='cartodbpositron')

	# add tiles to map
	folium.raster_layers.TileLayer('Open Street Map').add_to(world_map)
	folium.raster_layers.TileLayer('Stamen Terrain').add_to(world_map)
	folium.raster_layers.TileLayer('Stamen Toner').add_to(world_map)
	folium.raster_layers.TileLayer('Stamen Watercolor').add_to(world_map)
	folium.raster_layers.TileLayer('CartoDB Positron').add_to(world_map)
	folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(world_map)

	# add layer control
	folium.LayerControl().add_to(world_map)

	# mini map, scroll zoom toggle button, full screen
	# plugin for mini map
	minimap = plg.MiniMap(toggle_display=True)

	# add minimap to map
	world_map.add_child(minimap)

	# add scroll zoom toggler to map
	plg.ScrollZoomToggler().add_to(world_map)

	# add full screen button to map
	plg.Fullscreen(position='topright').add_to(world_map)

	# draw the position of the space station as a red circle
	folium.Circle(
		location=[iss_lat,iss_long],
		popup='IIS position:'+ '\nlongitude = ' + str(iss_long) + '\nlatitude = ' + str(iss_lat),
		radius=1000,
		color='red',
		fill=True,
		fill_color='crimson'
		).add_to(world_map)

	# save the map as html file to open it in a browser
	world_map.save('world_map.html')