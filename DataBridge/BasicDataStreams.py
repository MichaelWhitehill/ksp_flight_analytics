"""
This file creates data streams and performs minimal data manipulation on streams
"""

from DataBridge.FuelConsumption import FuelConsumption

class EngineThrust:
    def __init__(self, konnection):
        self.open_cycle_streams = []
        self.closed_cycle_streams = []
        # Build data stream of engine thrust depending on open or closed cycle (jet or rocket engine)
        for engine in konnection.vessel.parts.engines:
            if 'IntakeAir' in engine. propellant_names:
                self.open_cycle_streams.append(konnection.conn.add_stream(getattr, engine, 'thrust'))
            else:
                self.closed_cycle_streams.append(konnection.conn.add_stream(getattr, engine, 'thrust'))

    def get_closed_cycle_thrust(self):
        total = 0
        for engine in self.closed_cycle_streams:
            total += engine()
        return total

    def get_open_cycle_thrust(self):
        total = 0
        for engine in self.open_cycle_streams:
            total += engine()
        return total

# Creates streams for all air intake parts and returns lambda function that gets the total
def get_intake_stream(konnection):
    intake_streams = []
    for intake in konnection.vessel.parts.intakes:
        intake_streams.append(konnection.conn.add_stream(getattr, intake, 'flow'))

    def compute_flow():
        flow = 0
        for intake_s in intake_streams:
            flow += intake_s()
        return flow
    return compute_flow


def get_engine_info(konnection):
    engine = konnection.vessel.parts.engines[2]

    def info():
        return "prop ratio" + str(engine.propellant_ratios) + " thrust: " + str(engine.thrust) + " isp: " +\
               str(engine.specific_impulse)
    return info


# Opens streams for sideslip and angle of attack. Returns lambda that computes total.
def get_angle_of_attack(konnection):
    reference_frame = konnection.conn.space_center.ReferenceFrame.create_hybrid(
        position=konnection.vessel.orbit.body.reference_frame, rotation=konnection.vessel.surface_reference_frame)
    flight = konnection.vessel.flight(reference_frame)
    aoa_stream = konnection.conn.add_stream(getattr, flight, 'angle_of_attack')
    sideslip_stream = konnection.conn.add_stream(getattr, flight, 'sideslip_angle')

    def compute_total_aoa():
        return aoa_stream() + sideslip_stream()
    return compute_total_aoa

# Returns dictionary of attribute name to the stream for the attribute
# Streams are just functions so some attributes are lambda functions to access other streams
def create_streams(konnection):
    flight = konnection.vessel.flight(konnection.vessel.surface_reference_frame)
    # noinspection PyDictCreation
    streams = {}
    streams['atmospheric density'] = konnection.conn.add_stream(getattr, flight, 'atmosphere_density')
    streams['dyn. pressure'] = konnection.conn.add_stream(getattr, flight, 'dynamic_pressure')
    streams['mach'] = konnection.conn.add_stream(getattr, flight, 'mach')
    streams['G force'] = konnection.conn.add_stream(getattr, flight, 'g_force')
    streams['alt(sea)'] = konnection.conn.add_stream(getattr, flight, 'mean_altitude')
    streams['met'] = konnection.conn.add_stream(getattr, konnection.vessel, 'met')

    # streams where we want the in game surface reference frame
    reference_frame = konnection.conn.space_center.ReferenceFrame.create_hybrid(
        position=konnection.vessel.orbit.body.reference_frame, rotation=konnection.vessel.surface_reference_frame)
    flight = konnection.vessel.flight(reference_frame)
    streams['vert. speed'] = konnection.conn.add_stream(getattr, flight, 'vertical_speed')
    streams['ground speed'] = konnection.conn.add_stream(getattr, flight, 'speed')
    streams['air speed'] = konnection.conn.add_stream(getattr, flight, 'true_air_speed')
    streams['intake flow'] = get_intake_stream(konnection)
    streams['angle of attack(total)'] = get_angle_of_attack(konnection)

    streams['apoapsis alt.'] = konnection.conn.add_stream(getattr, konnection.vessel.orbit, 'apoapsis_altitude')
    streams['apoapsis time'] = konnection.conn.add_stream(getattr, konnection.vessel.orbit, 'time_to_apoapsis')

    streams['periapsis alt.'] = konnection.conn.add_stream(getattr, konnection.vessel.orbit, 'periapsis_altitude')
    streams['periapsis time'] = konnection.conn.add_stream(getattr, konnection.vessel.orbit, 'time_to_periapsis')

    # TODO Fix fuel consumption
    fc = FuelConsumption(konnection)
    streams['liquid fuel consumption'] = fc.compute_lf_consumption
    streams['oxidizer consumption'] = fc.compute_ox_consumption
    streams['Liquid Fuel'] = konnection.conn.add_stream(konnection.vessel.resources.amount, 'LiquidFuel')
    streams['Oxidizer'] = konnection.conn.add_stream(konnection.vessel.resources.amount, 'Oxidizer')

    engine_streams = EngineThrust(konnection)
    streams['open cycle thrust'] = engine_streams.get_open_cycle_thrust
    streams['closed cycle thrust'] = engine_streams.get_closed_cycle_thrust

    return streams
