from decimal import Decimal

class NormalSend:

    def __init__(self, data):
        self.data = data
        #self.key = ""
        #self.schema = ""
        self.long = 0
        self.lat = 0
        self.charge = False
        self.lvl = [0,0]

    def get_data(self):
        return self.data

    #def get_key(self):
    #    return self.key

    #def get_schema(self):
    #   return self.schema

    def get_long(self):
        return self.long

    def get_lat(self):
        return self.lat

    def get_charge(self):
        return self.charge

    def get_lvl(self):
        return self.lvl

    def set_data(self, data):
        self.data = data

    #def set_key(self, key):
    #    self.key = key

    #def set_schema(self, schema):
    #    self.schema = schema

    def set_long(self, long):
        self.long = long

    def set_lat(self, lat):
        self.lat = lat

    def set_charge(self, charge):
        self.charge = charge

    def set_lvl(self, lvl):
        self.lvl = lvl

    def auto_set(self):
        #self.key = self.data[:4]
        #self.schema = self.data[4]
        self.long = (Decimal(self.data[2])*1000).normalize()
        self.lat = (Decimal(self.data[3])*1000).normalize()
        if self.data[4] == "T":
            self.charge = True
        else:
            self.charge = False
        self.lvl[0] = int(self.data[5])
        self.lvl[1] = int(self.data[6])

    def to_dico(self):
        d = {}
        self.auto_set()
        d["longitude"]=float(self.get_long())
        d["latitude"]=float(self.get_lat())
        d["charge"]=self.get_charge()
        d["level"]=self.get_lvl()
        return d

