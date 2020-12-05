import rom as rom

from ortools.constraint_solver import pywrapcp, routing_enums_pb2

mymatrix = [
    [0, 1000, 10000, 10000],
    [1, 0, 1, 1],
    [1, 10000, 0, 10000],
    [1, 1, 10000, 0],
]

class Solver():

    def create_data_model(basematrix):
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = basematrix
        data['num_vehicles'] = 1
        data['depot'] = 0
        return data


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    def distance_counter(routing, solution):
        route_distance = 0
        index = routing.Start(0)

        while not routing.IsEnd(index):
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        return route_distance

    def print_solution(manager, routing, solution):
        """Prints solution on console."""
        print('Objective: {} miles'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Route:\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(manager.IndexToNode(index))
        print(plan_output)
        plan_output += 'Route distance: {}miles\n'.format(route_distance)

    def calculate_max_distance(matrix):
        return (len(matrix)*(len(matrix)-1))/2

if __name__ == '__main__':
    data = Solver.create_data_model(mymatrix)
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    transit_callback_index = routing.RegisterTransitCallback(Solver.distance_callback)

    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)

    maxdistance = Solver.calculate_max_distance(mymatrix)
    print(solution)
    if solution and Solver.distance_counter(routing, solution) < maxdistance:
        Solver.print_solution(manager, routing, solution)