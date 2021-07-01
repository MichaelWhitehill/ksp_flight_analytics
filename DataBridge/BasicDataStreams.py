from DataBridge.FuelConsumption import FuelConsumption


class EngineThrust:
    def __init__(self, konnection):
        self.open_cycle_streams = []
        self.closed_cycle_streams = []
        for engine in konnection.vessel.parts.engines:
            if 'IntakeAir' in engine. propellant_names:
                self.open_cycle_streams.append(create_attribute_stream(konnection, engine, 'thrust'))
            else:
                self.closed_cycle_streams.append(create_attribute_stream(konnection, engine, 'thrust'))

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


def create_attribute_stream(konnection, obj, attribute):
    return konnection.conn.add_stream(getattr, obj, attribute)


def get_intake_stream(konnection):
    intake_streams = []
    for intake in konnection.vessel.parts.intakes:
        intake_streams.append(create_attribute_stream(konnection, intake, 'flow'))

    def compute_flow():
        flow = 0
        for intake_s in intake_streams:
            flow += intake_s()
        return flow
    return compute_flow


def get_engine_info(konnection):
    engine = konnection.vessel.parts.engines[2]
    print(str(engine))

    def info():
        return "prop ratio" + str(engine.propellant_ratios) + " thrust: " + str(engine.thrust) + " isp: " +\
               str(engine.specific_impulse)
    return info


def get_angle_of_attack(konnection):
    reference_frame = konnection.conn.space_center.ReferenceFrame.create_hybrid(
        position=konnection.vessel.orbit.body.reference_frame, rotation=konnection.vessel.surface_reference_frame)
    flight = konnection.vessel.flight(reference_frame)
    aoa_stream = create_attribute_stream(konnection, flight, 'angle_of_attack')
    sideslip_stream = create_attribute_stream(konnection, flight, 'sideslip_angle')

    def compute_total_aoa():
        return aoa_stream() + sideslip_stream()
    return compute_total_aoa


def create_streams(konnection):
    flight = konnection.vessel.flight(konnection.vessel.surface_reference_frame)
    # noinspection PyDictCreation
    streams = {}
    streams['atmospheric density'] = create_attribute_stream(konnection, flight, 'atmosphere_density')
    streams['dyn. pressure'] = create_attribute_stream(konnection, flight, 'dynamic_pressure')
    streams['mach'] = create_attribute_stream(konnection, flight, 'mach')
    streams['G force'] = create_attribute_stream(konnection, flight, 'g_force')
    streams['alt(sea)'] = create_attribute_stream(konnection, flight, 'mean_altitude')
    streams['met'] = create_attribute_stream(konnection, konnection.vessel, 'met')

    # streams where we want the in game surface reference frame
    reference_frame = konnection.conn.space_center.ReferenceFrame.create_hybrid(
        position=konnection.vessel.orbit.body.reference_frame, rotation=konnection.vessel.surface_reference_frame)
    flight = konnection.vessel.flight(reference_frame)
    streams['vert. speed'] = create_attribute_stream(konnection, flight, 'vertical_speed')
    streams['ground speed'] = create_attribute_stream(konnection, flight, 'speed')
    streams['air speed'] = create_attribute_stream(konnection, flight, 'true_air_speed')
    streams['intake flow'] = get_intake_stream(konnection)
    streams['angle of attack(total)'] = get_angle_of_attack(konnection)

    streams['apoapsis alt.'] = create_attribute_stream(konnection, konnection.vessel.orbit, 'apoapsis_altitude')
    streams['apoapsis time'] = create_attribute_stream(konnection, konnection.vessel.orbit, 'time_to_apoapsis')

    streams['periapsis alt.'] = create_attribute_stream(konnection, konnection.vessel.orbit, 'periapsis_altitude')
    streams['periapsis time'] = create_attribute_stream(konnection, konnection.vessel.orbit, 'time_to_periapsis')

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
