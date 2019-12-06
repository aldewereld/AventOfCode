from typing import List


class OrbitMap:
    def __init__(self, object_list: List[str]) -> None:
        self.map = {}
        for item in object_list:
            self.add_object(item)

    def add_object(self, description: str) -> None:
        o1, o2 = description.strip().split(")")
        self.map[o2] = o1

    def distance(self, object: str) -> int:
        if object == "COM":
            return 0
        elif self.map[object] == "COM":
            return 1
        else:
            return 1+self.distance(self.map[object])

    def get_total_orbits(self) -> int:
        total = 0
        for object in self.map.keys():
            total += self.distance(object)
        return total

    def get_distance_from_to(self, object1: str, object2: str) -> int:
        path_to_1 = self.get_path(object1)
        path_to_2 = self.get_path(object2)
        common_object = self.find_common_orbit(path_to_1, object2)
        distance_to_common1 = path_to_1.index(common_object) # jumps to common object
        distance_to_common2 = path_to_2.index(common_object)
        return distance_to_common1 + distance_to_common2

    def get_path(self, object: str) -> List[str]:
        if object == "COM":
            return ["COM"]
        else:
            return [object]+self.get_path(self.map[object])

    def find_common_orbit(self, path: List[str], object: str) -> str:
        if path[0] in self.get_path(object):
            return path[0]
        else:
            return self.find_common_orbit(path[1:], object)


objectList = "COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L".split(",")
map = OrbitMap(objectList)
print(map.distance("D"))
print(map.distance("L"))
print(map.distance("COM"))
print(map.get_total_orbits())

with open("input.txt") as file:
    olist = file.readlines()
    orbit_map = OrbitMap(olist)
    print(orbit_map.get_total_orbits())

    print("Distance from You to Santa: ", orbit_map.get_distance_from_to("SAN", "YOU")-2)

