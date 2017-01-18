import readline, math

rho = 0.0765 #Density of air in lb/ft^3
g = 32.174 #Gravity in ft/s^2	
conversion = 32.174049 #conversion factor of ft-lbf to lbmft/s^2
y, n = True, False #For yes or no decisions (y/n)

def calculations():
	"""Main method for parachute calculations. 
	It assumes that the parachute is given enough distance to hit the ground at terminal velocity.
	Payload detaches, Booster and avionics bay comes down connected, but as separate sections."""
	
	payload, avionics, booster = weight_input()

	drogue_size, drogue_force = drogue_calc()
	main_size, main_force = main_calc(avionics, booster, drogue_force) #total mass, payload detaches

	print("Drogue is diameter is " + str(drogue_size) + " inches")
	print("Main is diameter is " + str(main_size) + " inches")
	
def weight_input():
	""" This method allows the user to input the weights.
	There are three components of the rocket (payload, avionics, and booster).
	Weights are in imperial units, pound-mass."""
	if bool(eval(input('Do you want to use different weights? (y/n) '))):
		return float(input('payload weight (lbm): ')), \
				float(input('avionics bay weight (lbm): ')), \
				float(input('booster weight (lbm): '))

	else:
		return 9.489, 4.083, 11.483 #2016-17 PDR Weights

def velocity_calc(mass, MoS):
	"""Returns the max velocity allowed that is withing the USLI regulation and MoS."""
	if bool(eval(input('Do you change the Kinetic Energy section? (y/n) '))):
		KEmax = float(input('Kenetic Energy Limit: '))
		safety_margin = float(input('Margin of Safety: '))
	else:
		KEmax = 75 #ft-lbf
		safety_margin = MoS

	KE_limit = KEmax / (safety_margin + 1)
	
	return math.sqrt((2*(KE_limit)*conversion)/mass)

def drogue_calc():
	"""Calculates the suggested size for the drogue.
	Requires user input on final drogue size."""
	if bool(eval(input('Do you change the drogue section? (y/n) '))):
		coeff_drag = float(input('Drogue Coefficient of Drag: '))
		max_velocity = float(input('Max Speed of Drogue (ft/s): '))

		area = (total * g) / (.5 * (max_velocity ** 2) * rho * coeff_drag)
		diameter = (math.sqrt(area/math.pi) * 2) * 12 #converted to inches

		print("Drogue is diameter should be at least " + str(diameter) + " inches")
		final_diameter = float(input('Please decide on final drogue parachute size (inches) :'))
	else:
		coeff_drag = 1.5
		final_diameter = 24.0  #2016-17 PDR Preset Value (inches)
	return final_diameter, coeff_drag * (math.pi * (final_diameter/2/12)**2) # Force of Drogue = Coeff of Drag * Area of Drogue 

def main_calc(avionics, booster, drogue_force):
	"""Calculates the suggested size for the drogue.
	Requires user input on final drogue size."""
	if bool(eval(input('Do you change the main section? (y/n) '))):
		coeff_drag = float(input('Drogue Coefficient of Drag: '))
		max_velocity = velocity_calc(max(avionics,booster), 0.5)	
	
		area = ((((avionics+booster) * g)/(.5 * (max_velocity ** 2) * rho)) - drogue_force) / coeff_drag
		radius = math.sqrt(area/math.pi) #ft
		diameter = radius * 2 * 12 #inches
		print("Main is diameter should be at least " + str(diameter) + " inches")
		final_diameter = float(input('Please decide on final main parachute size (inches) :'))
	else:
		coeff_drag = 2.2
		final_diameter = 72.0
	
	
	return final_diameter, coeff_drag * (math.pi * (final_diameter/2/12)**2) # Force of Drogue = Coeff of Drag * Area of Drogue 

calculations()
