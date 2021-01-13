
class AlertSend:

    def __init__(self, message):
        self.message = message
        self.key = ""
        self.schema = ""
        self.type = ""
        self.long = 0
        self.lat = 0
        self.charge = False
        self.lvl = [0,0]

    def get_message(self):
        return self.message

    def get_key(self):
        return self.key

    def get_schema(self):
        return self.schema

    def get_type(self):
        return self.type

    def get_long(self):
        return self.long

    def get_lat(self):
        return self.lat

    def get_charge(self):
        return self.charge

    def get_lvl(self):
        return self.lvl

    def set_message(self, message):
        self.message = message

    def set_key(self, key):
        self.key = key

    def set_schema(self, schema):
        self.schema = schema

    def set_type(self, arert_type):
        self.type = alert_type

    def set_long(self, long):
        self.long = long

    def set_lat(self, lat):
        self.lat = lat

    def set_charge(self, charge):
        self.charge = charge

    def set_lvl(self, lvl):
        self.lvl = lvl

    def auto_set(self):
        self.key = self.message[:4]
        self.schema = self.message[4]
        self.type = self.message[5]
        if self.message[6] == "-":
            self.long = -(int(self.message[7:-30])+int(self.message[11:-20])*0.000001)
        else:
            self.long = int(self.message[7:-30]) + (int(self.message[11:-20])*0.000001)

        if self.message[20] == "-":
            self.lat = -(int(self.message[21:-17])+(int(self.message[24:-8])*0.000001))
        else:
            self.lat = int(self.message[21:-17]) + (int(self.message[24:-8])*0.000001)
        if self.message[32] == "T":
            self.charge = True
        else:
            self.charge = False
        self.lvl[0] = self.message[34:-3]
        self.lvl[1] = self.message[37:]


def dict(protocol):
    d = {}
    protocol.auto_set()
    d["key"]=protocol.get_key()
    d["schema"]=protocol.get_schema()
    d["type"]=protocol.get_type()
    d["longitude"]=protocol.get_long()
    d["latitude"]=protocol.get_lat()
    d["charge"]=protocol.get_charge()
    d["level"]=protocol.get_lvl()
    #for att in dir(protocol):
    #    if not att.startswith('__') and not callable(getattr(protocol, att)):
    #        d[str(att)] = protocol.att
    return d


test = "[bk]@V+125,123456789-12,123456789T099069"
protTest = AlertSend(test)
dico = dict(protTest)
print(test)
print(dico)
