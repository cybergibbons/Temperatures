from prettytable import PrettyTable


class Element(object):
    def __init__(self, name='', gross_area=0.0, openings=0.0, u_value=0.0):
        self.name = name
        self.gross_area = gross_area
        self.openings = openings
        self.u_value = u_value

    def net_area_get(self):
        return self.gross_area - self.openings
    net_area = property(fget=net_area_get)

    def heat_loss_WK_get(self):
        return self.net_area * self.u_value
    heat_loss_WK = property(fget=heat_loss_WK_get)


elements = [Element('Floor', 49, 0, 0.7),
            Element('Walls', 168, 12, 0.45),
            Element('Ceiling', 49, 0, 0.25),
            Element('Windows', 12, 0, 2)]

volume = 294
infiltration = 1.5  # Air changes per hour
infiltration_WK = 0.33 * infiltration * volume

internal_temp = 21
external_temp = 12

fabric_heat_loss_WK = 0

for element in elements:
    fabric_heat_loss_WK += element.heat_loss_WK

total_heat_loss_WK = fabric_heat_loss_WK + infiltration_WK
heat_loss = total_heat_loss_WK * (internal_temp - external_temp)

elements_table = PrettyTable(['Room', 'Gross Area', '-', 'Openings', '=', 'Net Area', '*', 'U value', ' =', 'W/K'])
elements_table.align = 'r'
elements_table.align['Room'] = 'l'


for element in elements:
    elements_table.add_row([
                           element.name, element.gross_area, '-', element.openings, '=', element.net_area,
                           '*', element.u_value, '=', element.heat_loss_WK
                           ])

elements_table.add_row(['','','','','','','','','',fabric_heat_loss_WK])
print elements_table

summary_table = PrettyTable(['Name', 'Value', 'Unit'])
summary_table.align = 'l'
summary_table.align['Value'] = 'r'

summary_table.add_row(['Fabric heat loss', fabric_heat_loss_WK, 'W/K'])
summary_table.add_row(['Infiltration heat loss', infiltration_WK, 'W/K'])
summary_table.add_row(['Total heat loss', total_heat_loss_WK, 'W/K'])
summary_table.add_row(['T diff', internal_temp - external_temp, 'C'])
summary_table.add_row(['Heat loss ('+str(total_heat_loss_WK)+'W/K * '+str(internal_temp - external_temp)+'C)',
                       heat_loss, 'W'])
summary_table.add_row(['Annual heating demand', heat_loss*0.024*365, 'kWh'])

print summary_table

