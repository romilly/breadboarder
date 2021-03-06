import re
from decimal import Decimal

res_reg = re.compile('([0-9][0-9]?0?)([R|k|M])$|([0-9][0-9]?)(R|k|M)([0-9])$')

multipliers = {'R' : 1,
               'k' : 1000,
               'M' : 1000000,
               }

colors = ('black','brown','red','orange','yellow','blue','green','violet','grey','white')
multiplier_color = {}
for (index, color) in enumerate(colors):
    multiplier_color[index] = color
multiplier_color[-1] = 'gold'
multiplier_color[-2] = 'silver'
tolerance_bands = {
    '1%' : 'brown',
    '5%' : 'gold',
    '10%': 'silver'
}

class ColorCode:
    @staticmethod
    def parse(text):
        i = res_reg.match(text)
        if i is None:
            raise Exception('I only understand resistance values in standard form - e.g. 2R2, 220k, 1M2')
        if i.group(1):
            return Decimal(i.group(1))*multipliers[i.group(2)]
        else:
            return (Decimal(i.group(3)+i.group(5))*multipliers[i.group(4)])/Decimal(10)

    def bands_for(self, decimal_value):
        digits, exponent = decimal_value.as_tuple()[1:] # don't care about sign
        zeros = sum([(0 == digit) for digit in digits])
        significant_digits = [digit for digit in digits if digit != 0]
        start = ([0]+significant_digits)[-2:]
        multiplier = zeros + exponent
        return list(colors[digit] for digit in start)+[multiplier_color[multiplier]]

    def tolerance_band(self, tolerance):
        if tolerance not in tolerance_bands:
            raise ValueError('Tolerance must be 1%, 5% or 10%')
        return tolerance_bands[tolerance]
