class Map:
    def __init__(self, name):
        self.name = name
        self.locations={}
        self.neighbours= {}
    def add_location(self, location):
        if isinstance(location,Location):
            self.locations[location] = location
            self.neighbours[location] = [] 

    def display_locations(self,location): 
        if not self.locations:
            print(f"No locations found for {self.name}")
        else:
            for location in self.locations:
                print(location)
#Class invariants need to be added
    def add_neighbours(self,  location1, location2):
        if isinstance(location1, Location) and isinstance(location2, Location):
            return
        else:
             print("No neighburs for this location")

    def display_neighbours(self, location):
        if location not in Neighbours.neighbours.keys():
            print(f"There is no neighbouring location for {location}")
            return
        else:
            print(f"Neighbours: {self.neighbours}")




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
    france.add_location(Location("Marseille", 43.2965, 5.3698))
    france.display_neighbours()
    countries["France"] = france
    japan = Map("Japan")
    japan.add_location(Location("Tokyo", 35.6762, 139.6503))
    japan.add_location(Location("Kyoto", 35.0116, 135.7681))
    japan.add_location(Location("Satiama",35.8857, 139.6682))
    japan.display_neighbours()
    countries["Japan"] = japan
    usa = Map("USA")
    usa.add_location(Location("Seattle", 47.6062, 122.3321))
    usa.add_location(Location("Portland",45.5152, 122.6748))
    usa.add_location(Location("San Francisco",37.7749, 122.4194))
    usa.display_neighbours()
    countries["USA"] = usa
    for k,v in countries.items():
        v.display_locations()
    return countries

if __name__ == "__main__":
    data = Sample_Data() 

    #print(data)
class Neighbours:
    neighbours={
    "Paris":["Lyon", "Marseille"],
    "Lyon":["Paris","Marseille"],
    "Marseille":["Paris","Lyon"],

    "Tokyo":["Satiama","Kyoto"],
    "Satiama":["Tokyo","Kyoto"],
    "Kyoto":["Satiama","Tokyo"],

    "Seattle":["Portland","San Franscisco"], # pyright: ignore[reportUndefinedVariable]
    "Portland":["Seattle", "San Francisco"],
    "San Francisco":["Seattle", "Portland"]
}
    def __init__(self,location1, location2):
        
        self.__location1 = location1
        self.__location2 = location2

    def get_location1(self):
        return self.__location1
    
    def get_location2(self):
        return self.__location2
    
    def __str__(self):
       return f"Neighbours:{self.__location1}and{self.__location2}."