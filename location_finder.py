from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.reverse("12.959318,77.6455246")
print(location.address)
