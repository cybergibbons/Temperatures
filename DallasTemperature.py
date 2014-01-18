import os


class DS18B20(object):
    id = ''
    alias = ''
    temperature = None

    def __init__(self, id, alias='', temperature=None):
        self.id = id
        self.alias = alias
        self.temperature = temperature


class DallasTemperature(object):

    # Where will the OWFS filesystem reside
    base_dir = '/mnt/1wire'
    # default temperature resolution
    bit_resolution = 9
    # Chose between cached (quick to read, potentially old) and uncached (slow to read, more up to date)
    cached = True

    sensors = {}

    # OWFS filenames contain family code "28." and CRC "0000"
    # This pre/appends these parts to a short ID to get a long ID
    def short_to_long_id(self, id):
        if len(id) != 8:
            raise RuntimeError

        # CRC appears to be 0000 on OWFS
        return '28.'+str(id)+'0000'

    # OWFS filenames contain family code "28." and CRC "0000"
    # This trims these parts from a long ID to get a short ID
    def long_to_short_id(self, id):
        if len(id) != 15:
            raise RuntimeError

        return str(id)[3:11]

    def get_attribute(self, id, attribute):
        if self.cached:
            path = os.path.join(self.base_dir, self.short_to_long_id(id), attribute)
        else:
            path = os.path.join(self.base_dir, 'uncached', self.short_to_long_id(id), attribute)

        try:
            f = open(path)
            r = f.readline()
            f.close()
            return r

        except IOError:
            return None

    def get_type(self, id):
        return str(self.get_attribute(id=id, attribute='type')).strip()

    def get_temperature(self, id):
        return str(self.get_attribute(id, 'temperature'+str(self.bit_resolution))).strip()

    def is_connected(self, id):
        return self.get_attribute(id, 'scratchpad') is not None

    def scan_bus(self):
        self.sensors = {}

        for f in [name for name in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, name))
                # All DS18B20 have a class of 28
                  and name.startswith('28')]:

            id = self.long_to_short_id(f)
            type_sensor = self.get_type(id)

            if type_sensor is not None and type_sensor == 'DS18B20':
                if id not in self.sensors:
                    self.sensors[id] = DS18B20(id)

    def read_temperatures(self):
        for id in self.sensors:
            self.sensors[id].temperature = self.get_temperature(id)

    def set_alias(self, id, alias):
        if id in self.sensors:
            self.sensors[id].alias = alias

    def set_aliases(self, alias_dict):
        for id in alias_dict:
            self.set_alias(id, alias_dict[id])



sensor_map = {'33F74905': 'Flow',
              '3474A304': 'Return',
              'DB564A05': 'Ambient',
              'EDEE4905': 'Cylinder'}


bus = DallasTemperature()

bus.base_dir = '/Users/andrew/PycharmProjects/Temperatures/'

bus.scan_bus()

print len(bus.sensors)

bus.read_temperatures()

bus.set_aliases(sensor_map)

for id in bus.sensors:
    print bus.sensors[id].alias, bus.sensors[id].temperature

for id in sorted(bus.sensors):
    print id

