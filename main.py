import utilities
from collections import deque


class Street:
    def __init__(self, name, start, end, length):
        self.name = name
        self.start = start
        self.end = end
        self.length = length
        self.queue = deque()
    
    def add_to_queue(self, car):
        self.queue.append(car)
    
    def remove_from_queue(self):
        return self.queue.popleft()

    def is_green(self, timestep):
        return self.end.green_street(timestep) == self
    
    def __repr__(self):
        return self.name


class Intersection:
    def __init__(self, id):
        self.id = id
        self.incoming = set()
        self.outgoing = set()
        # schedule: [(street, green_phase_length), ...]
        self.schedule = []
        self.schedule_length = 0

    def add_incoming_street(self, street):
        self.incoming.add(street)

    def add_outgoing_street(self, street):
        self.outgoing.add(street)
    
    def set_schedule(self, schedule):
        self.schedule = schedule
        self.schedule_length = sum(s[1] for s in self.schedule)
        
    def green_street(self, timestep):
        if self.schedule_length == 0:
            return None
        timestep = timestep % self.schedule_length
        for street, phase_duration in self.schedule:
            timestep -= phase_duration
            if timestep < 0:
                return street
        

class Car:
    def __init__(self, start_street, route):
        self.start_street = start_street
        self.route = deque(route)
        self.current_street = self.route.popleft()
        self.pos_on_street = "queue"
    
    

def construct_submission(intersections):
    scheduled_inters = list(filter(lambda inters: inters.schedule_length > 0, intersections))
    out_lines = [len(scheduled_inters)]
    for inter in scheduled_inters:
        out_lines.append(inter.id)
        scheduled_streets = list(filter(lambda street_phase: street_phase[1] > 0, inter.schedule))
        out_lines.append(len(scheduled_streets))
        for street, phase in scheduled_streets:
            out_lines.append(" ".join((street.name, str(phase))))
    return "\n".join(map(str, out_lines))


# set every intersection to cycle through all lights, with a given length for each light
# order of streets? random or maybe ordered by length (longest streets first)
# strategy any of:
# random, shortest, longest
def make_baseline_schedule(intersections, green_phase_length, strategy="random"):
    for intersection in intersections:
        if strategy == "random":
            intersection.set_schedule([(street, green_phase_length) for street in intersection.incoming])
        elif strategy == "shortest":
            intersection.set_schedule([(street, green_phase_length) for street in sorted(intersection.incoming,key=lambda x: x.length)])
        elif strategy == "longest":
            intersection.set_schedule([(street, green_phase_length) for street in sorted(intersection.incoming,key=lambda x: x.length, reverse=True)])
    

def run_simulation(simulation_duration, cars, bonus_points):
    score = 0
    for timestep in range(simulation_duration):
        done_cars = []
        for i, car in enumerate(cars):
            #print([s.is_green(timestep) for s in streets.values()])
            #print(f"t={timestep}: car-{i}-{car.current_street.name}-{car.pos_on_street}")
            if car.pos_on_street == "queue":
                if len(car.current_street.queue) > 0 \
                and car.current_street.queue[0] == car \
                and car.current_street.is_green(timestep):
                    car.current_street.remove_from_queue()
                    car.pos_on_street = 0
                    car.current_street = car.route.popleft()
            if not car.pos_on_street == "queue":
                car.pos_on_street += 1
                if car.pos_on_street == car.current_street.length:
                    if len(car.route) == 0:
                        car.pos_on_street = "done"
                        done_cars.append(i)
                        continue
                    car.current_street.add_to_queue(car)
                    car.pos_on_street = "queue"
        for car_idx in reversed(done_cars):
            cars.pop(car_idx)
            score += bonus_points + simulation_duration - timestep
    return score


if __name__ == '__main__':
    problem_files = ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]
    #problem_files = ["a.txt"]
    for problem in problem_files:
        print(f"Running file {problem}")
        start_time = utilities.current_milli_time()


        #------- Loading problem -------

        path = f"qualification_round_2021.in/{problem}"
        metadata, problem_data = utilities.load_input_file(path)
        simulation_duration, intersections_count, streets_count, cars_count, bonus_points = map(int, metadata)
    
        streets_raw = problem_data[:streets_count]
    
        
        #------- Data structures construction -------

        intersections = {}
        streets = {}
    
        for street in streets_raw:
            start_inter, end_inter, name, duration_str = street
            start, end, duration = map(int, [start_inter, end_inter, duration_str])
            if start not in intersections:
                intersections[start] = Intersection(start)
            if end not in intersections:
                intersections[end] = Intersection(end)
            street = Street(name, intersections[start], intersections[end], duration)
            streets[name] = street
            intersections[start].add_outgoing_street(street)
            intersections[end].add_incoming_street(street)
            
        cars = [Car(streets[car_data[1]], map(lambda name: streets[name], car_data[1:]))
                    for car_data in problem_data[streets_count:]]
        for car in cars:
            car.current_street.add_to_queue(car)


        #------- Solution construction -------

        make_baseline_schedule(intersections.values(), 1, "shortest")

        #------- Simulating result -------

        score = run_simulation(simulation_duration, cars, bonus_points)
        
        print(f"Score: {score}")
        print(f"Number of cars not finished: {len(cars)}")
        
        #------- Saving solution -------

        submission = construct_submission(intersections.values())
        
        print(f"Time for everything: {round(utilities.current_milli_time() - start_time, 3)}")
        # print(submission)

        # write submission to file  
        with open(f"out/submission_{problem}_{utilities.get_current_time_for_filename()}.txt", "w+") as f:
            f.write(submission)
            



