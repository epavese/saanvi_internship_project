class Map:
    def __init__(self, name):
        self.name = name
        self.locations={}

    def add_location(self, location):
        self.locations[location] = []

    def display_locations(self): 
        if not self.locations:
            print(f"No locations found for {self.name}")
        else:
            for location in self.locations:
                print(location)

class Location:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.lat = latitude
        self.long = longitude

    def __str__(self):
        return f"the following location is: {self.name} and the latitude is {self.lat} and the longitude is {self.long}."
    



def Sample_Data():
    countries = {}  
    france = Map("France")
    france.add_location(Location("Paris", 48.8566, 2.3522))
    france.add_location(Location("Lyon", 45.7640, 4.8357))
    countries["france"] = france
    japan = Map("Japan")
    japan.add_location(Location("Tokyo", 35.6762, 139.6503))
    japan.add_location(Location("Kyoto", 35.0116, 135.7681))
    countries["japan"] = japan
    for k,v in countries.items():
        v.display_locations()
    return countries

if __name__ == "__main__":
    data= Sample_Data()
    #print(data)

neighbours = {
    Paris:[Lyon,Bordeaux,Marseille,Nice],
    Lyon:[Paris,Bordeux,Marseille,Nice],
    Marseille:[Paris,Lyon,Bordeux,Nice],
    Bordeux:[Paris,Lyon,Marseille,Nice],
    Nice:[Paris,Lyon,Marseille,Bordeux]
}