# import numpy as np
# import matplotlib.pyplot as plt

# # Constants
# m = -0.09210001871589
# c = np.log10(1304)
# threshold_cycles = 3823.79
# threshold_stress_mpa = 610
# threshold_stress_pa = threshold_stress_mpa # Convert MPa to Pa

# def calculate_range(life_cycles):
#     if life_cycles <= threshold_cycles:
#         return threshold_stress_mpa
#     else:
#         stress_pa = 10**(m * np.log10(life_cycles) + c)
#         return stress_pa  # Convert Pa to MPa

# def calculate_life_cycles(stress_value_mpa):
#     stress_pa = stress_value_mpa   # Convert MPa to Pa
#     if stress_value_mpa >= threshold_stress_mpa:
#         return threshold_cycles
#     else:
#         life_cycles = 10**((np.log10(stress_pa) - c) / m)
#         return life_cycles

# def plot_curve(user_x, user_y, user_value, is_life_cycles):
#     # Define the range for life cycles and corresponding stresses
#     life_cycles = np.logspace(1, 10, num=100)  # Generate 100 values from 10^1 to 10^8
#     stresses = np.array([calculate_range(lc) for lc in life_cycles])
    
#     # Plot the curve
#     plt.figure(figsize=(10, 6))
#     plt.loglog(life_cycles, stresses, label="Stress-Life Curve")

#     # Plot user input point
#     if is_life_cycles:
#         stress_value_mpa = calculate_range(user_value)
#         plt.plot(user_value, stress_value_mpa, 'ro', label=f'User Input: {user_value} life cycles')
#     else:
#         life_cycle_value = calculate_life_cycles(user_value)
#         plt.plot(life_cycle_value, user_value, 'bo', label=f'User Input: {user_value} MPa stress')

#     # Add axes intersections
#     plt.axhline(y=610, color='r', linestyle='--', label='Stress Threshold (610 MPa)')
#     plt.axvline(x=3823.79, color='b', linestyle='--', label='Life Cycle Threshold (3823.79)')
    
#     plt.xlabel("Life Cycles")
#     plt.ylabel("Stress Range (MPa)")
#     plt.title("Fatigue Curve")
#     plt.grid(True, which="both", ls="--")
#     plt.legend()
#     plt.show()

# # Input from user
# option = input("Do you want to enter life cycles or stress value? (x/y): ").strip().lower()

# if option == "x":
#     life_cycles = float(input("Enter the number of life cycles: "))
#     range_mpa = calculate_range(life_cycles)
#     print(f"Range (MPa) for {life_cycles} cycles: {range_mpa}")
#     plot_curve(life_cycles, range_mpa, life_cycles, is_life_cycles=True)
# elif option == "y":
#     stress_value = float(input("Enter the stress value (MPa): "))
#     life_cycles = calculate_life_cycles(stress_value)
#     if life_cycles>10E10:
#         print("Life cycles is too high, It have a infinite life cycles")
#     else:
#         print(f"Life cycles for {stress_value} MPa: {life_cycles}")
#         plot_curve(life_cycles, stress_value, stress_value, is_life_cycles=False)
# else:
#     print("Invalid option. Please enter 'x' or 'y'.")


# import numpy as np
# import matplotlib.pyplot as plt

# # Constants
# m = -0.09210001871589
# c = np.log10(1304/2)
# threshold_cycles =3823.79
# threshold_stress_mpa = 305
# threshold_stress_pa = threshold_stress_mpa  # Convert MPa to Pa

# def calculate_range(life_cycles):
#     if life_cycles <= threshold_cycles:
#         return threshold_stress_mpa
#     else:
#         stress_pa = 10**(m * np.log10(life_cycles) + c)
#         return stress_pa  # Convert Pa to MPa

# def calculate_life_cycles(stress_value_mpa):
#     stress_pa = stress_value_mpa   # Convert MPa to Pa
#     if stress_value_mpa > threshold_stress_mpa:
#         return threshold_cycles
#     else:
#         life_cycles = 10**((np.log10(stress_pa) - c) / m)
#         return life_cycles

# def plot_curve(user_x, user_y, user_value, is_life_cycles):
#     # Define the range for life cycles and corresponding stresses
#     life_cycles = np.logspace(1, 10, num=200) 
#     stresses = np.array([calculate_range(lc) for lc in life_cycles])   # Halve the y-values
    
#     # Plot the curve
#     plt.figure(figsize=(10, 6))
#     plt.loglog(life_cycles, stresses, label="Stress-Life Curve (Halved)")

#     # Plot user input point
#     if is_life_cycles:
#         stress_value_mpa = calculate_range(user_value)  # Halve the y-value
#         plt.plot(user_value, stress_value_mpa, 'ro', label=f'User Input: {user_value} life cycles')
#     else:
#         life_cycle_value = calculate_life_cycles(user_value)
#         plt.plot(life_cycle_value, user_value, 'bo', label=f'User Input: {user_value} MPa stress (Halved)')

#     # Add axes intersections
#     plt.axhline(y=305, color='r', linestyle='--', label='Stress Threshold (305 MPa)')
#     plt.axvline(x=3823.79, color='b', linestyle='--', label='Life Cycle Threshold (3823.79)')
    
#     plt.xlabel("Life Cycles")
#     plt.ylabel("Stress Amplitude (MPa)")
#     plt.title("Fatigue Curve (Halved Stress Values)")
#     plt.grid(True, which="both", ls="--")
#     plt.legend()
#     plt.show()


# option = input("Do you want to enter life cycles or stress value? (x/y): ").strip().lower()

# if option == "x":
#     life_cycles = float(input("Enter the number of life cycles: "))
#     range_mpa = calculate_range(life_cycles) 
#     print(f"Range (MPa) for {life_cycles} cycles: {range_mpa}")
#     plot_curve(life_cycles, range_mpa, life_cycles, is_life_cycles=True)
# elif option == "y":
#     stress_value = float(input("Enter the stress value (MPa): "))
#     life_cycles = calculate_life_cycles(stress_value)
#     if life_cycles > 10E9:
#         print("Life cycles is too high, It have an infinite life cycles")
#     else:
#         print(f"Life cycles for {stress_value} MPa: {life_cycles}")
#         plot_curve(life_cycles, stress_value, stress_value, is_life_cycles=False)
# else:
#     print("Invalid option. Please enter 'x' or 'y'.")


import numpy as np
import matplotlib.pyplot as plt

# Constants
m = -0.09210001871589
c = np.log10(1304 / 2)
threshold_cycles = 3823.79
threshold_stress_mpa = 305
threshold_stress_pa = threshold_stress_mpa  # Convert MPa to Pa

def calculate_range(life_cycles):
    if life_cycles <= threshold_cycles:
        return threshold_stress_mpa
    else:
        stress_pa = 10**(m * np.log10(life_cycles) + c)
        return stress_pa  # Convert Pa to MPa

def calculate_life_cycles(stress_value_mpa):
    stress_pa = stress_value_mpa  # Convert MPa to Pa
    if stress_value_mpa > threshold_stress_mpa:
        return threshold_cycles
    else:
        life_cycles = 10**((np.log10(stress_pa) - c) / m)
        return life_cycles

def format_output(value):
    if value > 1000:
        return "{:.2E}".format(value)
    else:
        return str(value)

def plot_curve(user_x, user_y, user_value, is_life_cycles):
    # Define the range for life cycles and corresponding stresses
    life_cycles = np.logspace(1, 10, num=200)
    stresses = np.array([calculate_range(lc) for lc in life_cycles])
    
    # Plot the curve
    plt.figure(figsize=(10, 6))
    plt.loglog(life_cycles, stresses, label="Stress-Life Curve (Halved)")

    # Plot user input point
    if is_life_cycles:
        stress_value_mpa = calculate_range(user_value)
        plt.plot(user_value, stress_value_mpa, 'ro', label=f'User Input: {user_value} life cycles')
    else:
        life_cycle_value = calculate_life_cycles(user_value)
        plt.plot(life_cycle_value, user_value, 'bo', label=f'User Input: {user_value} MPa stress (Halved)')

    # Add axes intersections
    plt.axhline(y=305, color='r', linestyle='--', label='Stress Threshold (305 MPa)')
    plt.axvline(x=3823.79, color='b', linestyle='--', label='Life Cycle Threshold (3823.79)')
    
    plt.xlabel("Life Cycles")
    plt.ylabel("Stress Amplitude (MPa)")
    plt.title("Fatigue Curve (Halved Stress Values)")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.show()

option = input("Do you want to enter life cycles or stress value? (x/y): ").strip().lower()

if option == "x":
    life_cycles = float(input("Enter the number of life cycles: "))
    range_mpa = calculate_range(life_cycles)
    print(f"Range (MPa) for {format_output(life_cycles)} cycles: {format_output(range_mpa)}")
    plot_curve(life_cycles, range_mpa, life_cycles, is_life_cycles=True)
elif option == "y":
    stress_value = float(input("Enter the stress value (MPa): "))
    life_cycles = calculate_life_cycles(stress_value)
    if life_cycles > 10E9:
        print("Life cycles is too high, It has an infinite life cycles")
    else:
        print(f"Life cycles for {format_output(stress_value)} MPa: {format_output(life_cycles)}")
        plot_curve(life_cycles, stress_value, stress_value, is_life_cycles=False)
else:
    print("Invalid option. Please enter 'x' or 'y'.")
