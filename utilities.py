import time


def current_milli_time():
    return round(time.perf_counter() * 1000)


def get_current_time_for_filename():
    return time.strftime("%Y-%m-%d_%H-%M-%S")


def load_input_file(filepath):
    with open(filepath, "r") as f:
        metadata = f.readline().split()
        problem_data = [line.split() for line in f]
    return metadata, problem_data


def save_solution_file(solution, filepath):
    with open(filepath, "w") as f:
        f.write(solution)

