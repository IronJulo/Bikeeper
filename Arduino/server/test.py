
class PositionTarget:

    def __init__(self, message):
        self.message = message
        self.key = ""
        self.schema = ""
        self.long = 0
        self.lat = 0
        self.charge = False
        self.lvl = [0,0]
        self.speed = 0
        self.angles = [0,0]

    def get_message(self):
        return self.message

    def get_key(self):
        return self.key

    def get_schema(self):
        return self.schema

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
    
    def get_angles(self):
        return self.angles

    def set_message(self, message):
        self.message = message

    def set_key(self, key):
        self.key = key

    def set_schema(self, schema):
        self.schema = schema

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

    def set_angles(self,angles):
        self.angles = angles

    def auto_set(self):
        self.key = self.message[:4]
        self.schema = self.message[4]
        if self.message[5] == "-":
            self.long = -(int(self.message[6:-41])+int(self.message[10:-31])*0.000001)
        else:
            self.long = int(self.message[6:-41]) + (int(self.message[10:-31])*0.000001)

        if self.message[19] == "-":
            self.lat = -(int(self.message[20:-28])+(int(self.message[23:-19])*0.000001))
        else:
            self.lat = int(self.message[20:-28]) + (int(self.message[23:-19])*0.000001)
        if self.message[31] == "T":
            self.charge = True
        else:
            self.charge = False
        self.lvl[0] = self.message[33:-14]
        self.lvl[1] = self.message[36:-11]
        self.speed = self.message[38:-8]
        self.angles[0] = self.message[43:-4]
        if self.message[41] == "-":
            self.angles[0] = -self.angles[0]
        self.angles[1] = self.message[47:]
        if self.message[45] == "-":
            self.angles[1] = -self.angles[1]

def dict(protocol):
    d = {}
    protocol.auto_set()
    d["key"]=protocol.get_key()
    d["schema"]=protocol.get_schema()
    d["longitude"]=protocol.get_long()
    d["latitude"]=protocol.get_lat()
    d["charge"]=protocol.get_charge()
    d["level"]=protocol.get_lvl()
    d["speed"]=protocol.get_lvl()
    d["angles"]=protocol.get_angles()
    #for att in dir(protocol):
    #    if not att.startswith('__') and not callable(getattr(protocol, att)):
    #        d[str(att)] = protocol.att
    return d


test = "[bk]@+125,123456789-12,123456789T099069000+002+001"
protTest = PositionTarget(test)
dico = dict(protTest)
print(test)
print(dico)
