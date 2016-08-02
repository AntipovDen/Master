from random import randrange

STABLE_STATE = 0
UNSTABLE_STATE = 1
POTENTIALLY_UNSTABLE_STATE = 2
E = 20
run_number = 0


# function choose() takes map of functions and their probabilities and returns one of them with that probability
def choose(function_map):
    r = randrange(2 * E ** 2)
    for f, p in function_map.items():
        if r < p:
            return f
        r -= p
    return lambda: None


class State_exception(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Model:
    def __init__(self, unrelaxed_edge=0, free_distance=E - 1, state=STABLE_STATE):
        self.unrelaxed_edge = unrelaxed_edge
        self.free_distance = free_distance
        self.current_state = state
        self.end = False

    def free_distance_right(self):
        self.free_distance += 1
        if self.free_distance == self.unrelaxed_edge + 1:
            if self.current_state == UNSTABLE_STATE:
                self.end = True
            elif self.current_state == POTENTIALLY_UNSTABLE_STATE:
                self.current_state = UNSTABLE_STATE
    
    def free_distance_left(self):
        self.free_distance -= 1
        if self.free_distance == self.unrelaxed_edge and self.current_state == UNSTABLE_STATE:
            self.current_state = POTENTIALLY_UNSTABLE_STATE
    
    def unrelaxed_edge_right(self):
        self.unrelaxed_edge += 1
        self.current_state = UNSTABLE_STATE
    
    def to_unstable_state(self):
        self.current_state = UNSTABLE_STATE
        
    def to_stable_state(self):
        self.current_state = STABLE_STATE

    def to_potentially_stable_state(self):
        self.current_state = POTENTIALLY_UNSTABLE_STATE

    def unrelaxed_edge_left(self):
        if randrange(E + self.unrelaxed_edge - 1) > 0 or self.unrelaxed_edge == 1:
            self.current_state = STABLE_STATE
        self.unrelaxed_edge -= 1

    def end_run(self):
        self.end = True

    def swap_unrelaxed_edge_right(self):
        self.free_distance -= 1
        self.unrelaxed_edge += 1
        self.current_state = POTENTIALLY_UNSTABLE_STATE

    def swap_unrelaxed_edge_left(self):
        if randrange(E + self.unrelaxed_edge - 1) > 0 or self.unrelaxed_edge == 1:
            self.current_state = STABLE_STATE
        else:
            self.current_state = UNSTABLE_STATE
        self.free_distance += 1
        self.unrelaxed_edge -= 1

    def run(self):
        # global run_number
        # print('Run {}'.format(run_number))
        # run_number += 1
        iterations = 0
        while not self.end:
            iterations += 1
            function_map = {}
            if self.free_distance != E - 1:
                function_map[self.free_distance_right] = 1
            if self.free_distance != 0:
                function_map[self.free_distance_left] = 1
            if self.unrelaxed_edge != E - 1:
                function_map[self.unrelaxed_edge_right] = 1
            if self.unrelaxed_edge != 0:
                function_map[self.to_unstable_state] = 1
            if self.unrelaxed_edge > self.free_distance:
                function_map[self.to_potentially_stable_state] = 1
            if self.current_state != STABLE_STATE:
                function_map[self.to_stable_state] = E + self.unrelaxed_edge - 1
            if self.current_state == UNSTABLE_STATE:
                function_map[self.unrelaxed_edge_left] = E + self.unrelaxed_edge - 1
            if self.unrelaxed_edge == self.free_distance:
                function_map[self.end_run] = 1
            if self.free_distance == self.unrelaxed_edge + 1:
                function_map[self.swap_unrelaxed_edge_right] = 1
            if self.free_distance == self.unrelaxed_edge - 1 and self.current_state == POTENTIALLY_UNSTABLE_STATE:
                function_map[self.swap_unrelaxed_edge_left] = E + self.unrelaxed_edge - 1
            choose(function_map)()
        return iterations


class Real_model:
    def __init__(self):
        self.edges = list(reversed(range(E)))
        self.orientation = [0] * E

    # this function sets the initial state of the graph. It assumes that graph has all edges relaxed
    # i.e. edges[i] = E - i - 1 and orientation[i] = 0 for every i
    def reset(self, unrelaxed_edge=0, free_distance=E - 1, state=STABLE_STATE):
        # check for correctness
        if unrelaxed_edge == 0 and state == UNSTABLE_STATE:
            raise State_exception('Unstabel state is impossible when the first edge is unrelaxed')
        if unrelaxed_edge <= free_distance and state == POTENTIALLY_UNSTABLE_STATE:
            raise State_exception('PUS is impossible when the free distance is not on the left from the unrelaxed edge')

        for i in range(free_distance, unrelaxed_edge):
            self.edges[i] -= 1
        for i in range(unrelaxed_edge, free_distance):
            self.edges[i + 1] += 1

        if state == UNSTABLE_STATE:
            self.edges[unrelaxed_edge] = self.edges[unrelaxed_edge - 1]
        elif state == POTENTIALLY_UNSTABLE_STATE:
            self.edges[unrelaxed_edge] = self.edges[unrelaxed_edge - 1] + 1
        elif state == STABLE_STATE:
            self.orientation[unrelaxed_edge] = 1

    def count_unrelaxed(self):
        count = 0
        last_relaxed = -1
        # first edge
        if self.orientation[0] == 0:
            last_relaxed = 0
        else:
            count = 1

        # second edge
        if self.orientation[1] == 0:
            if last_relaxed == -1 or self.edges[1] < self.edges[0]:
                last_relaxed = 1
            else:
                count += 1
        else:
            count += 1

        if count == 2:
            return 2

        for i in range(2, E):
            if self.orientation[i] == 1 or self.edges[last_relaxed] <= self.edges[i]:
                count += 1
            else:
                last_relaxed = i
            if count == 2:
                return 2
        return count

    def run(self, unrelaxed_edge=0, free_distance=E - 1, state=STABLE_STATE):
        # global run_number
        # print('Run {}'.format(run_number))
        # run_number += 1
        self.reset(unrelaxed_edge, free_distance, state)
        iterations = 0
        while True:
            iterations += 1
            edge = randrange(E)
            old_length, old_orientation = self.edges[edge], self.orientation[edge]
            self.orientation[edge] = randrange(2)
            self.edges[edge] = randrange(E)
            unrelaxed = self.count_unrelaxed()
            if unrelaxed == 0:
                return iterations
            if unrelaxed >= 2:
                self.orientation[edge] = old_orientation
                self.edges[edge] = old_length

runs = 1000
for E in 20, 50, 100:
    print('E =', E)
    m = Real_model()
    for unrelaxed_edge in range(E):
        for free_distance in range(E):
            print('UE:', unrelaxed_edge, 'FD:', free_distance)
            my_model = sum([Model(unrelaxed_edge, free_distance).run() for _ in range(runs)]) / runs
            real_model = sum([m.run(unrelaxed_edge, free_distance) for _ in range(runs)]) / runs
            print('SSt:', my_model, real_model, abs(my_model - real_model) / max(my_model, real_model))
            if unrelaxed_edge != 0:
                my_model = sum([Model(unrelaxed_edge, free_distance, UNSTABLE_STATE).run() for _ in range(runs)]) / runs
                real_model = sum([m.run(unrelaxed_edge, free_distance, UNSTABLE_STATE) for _ in range(runs)]) / runs
                print('USS:', my_model, real_model, abs(my_model - real_model) / max(my_model, real_model))
            if unrelaxed_edge > free_distance:
                my_model = sum([Model(unrelaxed_edge, free_distance, POTENTIALLY_UNSTABLE_STATE).run() for _ in range(runs)]) / runs
                real_model = sum([m.run(unrelaxed_edge, free_distance, POTENTIALLY_UNSTABLE_STATE) for _ in range(runs)]) / runs
                print('PUS:', my_model, real_model, abs(my_model - real_model) / max(my_model, real_model))
