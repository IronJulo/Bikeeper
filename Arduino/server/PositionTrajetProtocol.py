from decimal import Decimal

class PositionTrajet:

    def __init__(self, data):
        self.data = data
        self.long = 0
        self.lat = 0
        self.charge = False
        self.lvl = [0,0]
        self.speed = 0
        self.angle = 0

    def get_data(self):
       return self.data

    def get_long(self):
        return self.long

    def get_lat(self):
        return self.lat

    def get_charge(self):
        return self.charge

    def get_lvl(self):
        return self.lvl
    
    def get_speed(self):
        return self.speed
    
    def get_angle(self):
        return self.angle

    def set_data(self, data):
        self.data = data

    def set_long(self, long):
        self.long = long

    def set_lat(self, lat):
        self.lat = lat

    def set_charge(self, charge):
        self.charge = charge

    def set_lvl(self, lvl):
        self.lvl = lvl
    
    def set_speed(self,speed):
        self.speed = speed

    def set_angle(self,angle):
        self.angle = angle

    def auto_set(self):
        self.long = (Decimal(self.data[2])*1000).normalize()
        self.lat = (Decimal(self.data[3])*1000).normalize()
        self.charge = self.data[4]
        self.lvl[0] = int(self.data[5])
        self.lvl[1] = int(self.data[6])
        self.speed = int(self.data[7])
        self.angle = int(self.data[8])
    def to_dico(self):
        d = {}
        self.auto_set()
        d["longitude"]=float(self.get_long())
        d["latitude"]=float(self.get_lat())
        d["charge"]=self.get_charge()
        d["level"]=self.get_lvl()
        d["speed"]=self.get_speed()
        d["angle"]=self.get_angle()
        return d

