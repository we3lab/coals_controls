def electricity_conversion(coal_combusted, heat, heat_rate):
    lb_to_kg = 2.20462 #pounds in a kilogram
    heat_consumed = coal_combusted * heat * lb_to_kg #Btu
    electricity_generated = heat_consumed / heat_rate
    return electricity_generated

def coal_combustion(electricity_generated, heat, heat_rate):
    kg_to_lb = 0.453592 #kilograms in a pound
    MWh_to_kWh = 1000 #kWh in a MWh
    heat_converted = electricity_generated * MWh_to_kWh * heat_rate #Btu/hr of heat combusted in the plant
    coal_combusted = (heat_converted * kg_to_lb) / heat #kg/hr of coal combusted in the plant
    return coal_combusted