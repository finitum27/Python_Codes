import numpy as np

def calculate_range(life_cycles):
    m = -0.09210001871589  
    c = np.log10(1304) 

    range_mpa = 10**(m * np.log10(life_cycles) + c)
    
    return range_mpa

life_cycles = float(input("Enter the number of life cycles: "))
range_mpa = calculate_range(life_cycles)
print(f"Range (MPa) for {life_cycles} cycles: {range_mpa}")