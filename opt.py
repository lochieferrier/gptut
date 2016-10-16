from gpkit import Variable, Model, units

# Configuration
n_rotors = Variable('n_rotors',4,'-')
payload_mass = Variable('payload_mass',0.1,'kg')
structures_mass = Variable('structures_mass',0.2,'kg')

# Battery
battery_mass = Variable('battery_mass','kg')
battery_energy = Variable('battery_energy','J')
battery_specificEnergy = Variable('battery_specificEnergy',2.98e5,'J/kg')

# ESC
esc_mass = Variable('esc_mass','kg')
esc_power = Variable('esc_power','W')
esc_specificPower = Variable('esc_specificPower',500,'W/kg')

# Motor
motor_mass = Variable('motor_mass','kg')
motor_power = Variable('motor_power','W')
motor_specificPower = Variable('motor_specificPower',3007,'W/kg')

# Propeller
propeller_d = Variable('propeller_d',0.1,'m')
propeller_efficiency = Variable('propeller_efficiency',0.9,'-')

# Performance variables
t_hover = Variable('t_hover','s')
T_total = Variable('T_total','N')
P_total = Variable('P_total','W')
m_total = Variable('m_total','kg')

# Environment
rho = Variable('rho',1.225,'kg/m^3') 
g = Variable('g',9.8,'m/s/s')

# Constraints
constraints = [battery_energy <= battery_specificEnergy*battery_mass,
			   esc_power <= esc_specificPower*esc_mass,
			   motor_power <= motor_specificPower*motor_mass,
			   esc_power >= motor_power,
			   T_total <= 3.141/2 * rho* units('m^3/kg')* (propeller_efficiency*n_rotors*motor_power**(0.6)*propeller_d**(0.6)*units('(N/(W^0.6 * m^0.6))')),
			   m_total >= n_rotors*(esc_mass+motor_mass) + battery_mass+payload_mass+structures_mass,
			   P_total >= n_rotors*esc_power,
			   T_total >= m_total*g,
			   t_hover <= battery_energy/P_total,
			   t_hover >= Variable('t_hoverLimit',120,'s')]

# Objective (to minimize)
# objective = 1/t_hover
objective = (1/t_hover)**0.0001 * ((m_total*g)/T_total)**5

# Formulate the Model
m = Model(objective, constraints)
# Solve the Model
sol = m.solve(verbosity=1)

print '\nMax hover time is ' + str((sol(t_hover)*1/60).magnitude) + ' minutes'
print 'Thrust to weight ratio is ' + str(sol((T_total/(m_total*g))))