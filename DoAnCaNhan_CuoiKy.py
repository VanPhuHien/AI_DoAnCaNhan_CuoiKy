import pygame as pg
import time
from queue import Queue, LifoQueue, PriorityQueue
import heapq
import random
from copy import deepcopy
import math
from collections import defaultdict
import matplotlib.pyplot as plt

pg.init()

WIDTH, HEIGHT = 1050, 900
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("23110213_VanPhuHien")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GREEN = (0, 100, 0)

font = pg.font.Font(None, 48)
font_button = pg.font.Font(None, 40)
font_title = pg.font.Font(None, 50)

# Trạng thái ban đầu và mục tiêu
initial_start = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
start = [row[:] for row in initial_start]
goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
solution_steps = []

# Định nghĩa trong không gian niềm tin
current_mode = "default"  
nos_belief_states = set() 
nos_goal_states = set()    
pos_belief_states = set()  
pos_goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Định nghĩa các nhóm thuật toán
ALGORITHM_GROUPS = {
    "Uninformed": ["BFS", "DFS", "UCS", "IDS"],
    "Informed": ["Greedy", "A*", "IDA*"],
    "Local": ["SHC", "SAHC", "Stochastic", "SA", "BS", "GA"],
    "Nond": ["AOGS", "NOS", "POS"],
    "Constraint": ["BT", "AC-3"],
    "RL": ["Q-Learning"]
}

# Vị trí các nút
buttons = {
    "BFS": pg.Rect(50, 550, 150, 50),
    "DFS": pg.Rect(220, 550, 150, 50),
    "UCS": pg.Rect(390, 550, 150, 50),
    "IDS": pg.Rect(560, 550, 150, 50),
    "Greedy": pg.Rect(390, 620, 150, 50),
    "A*": pg.Rect(50, 620, 150, 50),
    "IDA*": pg.Rect(220, 620, 150, 50),
    "SHC": pg.Rect(220, 690, 150, 50),
    "SAHC": pg.Rect(390, 690, 150, 50),
    "Stochastic": pg.Rect(560, 690, 150, 50),
    "SA": pg.Rect(50, 690, 150, 50),
    "BS": pg.Rect(560, 620, 150, 50),
    "GA": pg.Rect(50, 760, 150, 50),
    "AOGS": pg.Rect(800, 690, 150, 50),
    "NOS": pg.Rect(800, 550, 150, 50),
    "POS": pg.Rect(800, 620, 150, 50),
    "BT": pg.Rect(220, 760, 150, 50),
    "AC-3": pg.Rect(390, 760, 150, 50),
    "Q-Learning": pg.Rect(560, 760, 150, 50),
    
    # Nút vẽ đồ thị
    "Uninformed": pg.Rect(10, 845, 160, 50),
    "Informed": pg.Rect(180, 845, 160, 50),
    "Local": pg.Rect(350, 845, 160, 50),
    "Nond": pg.Rect(520, 845, 160, 50),
    "Constraint": pg.Rect(690, 845, 160, 50),
    "RL": pg.Rect(860, 845, 160, 50),
    
    "Reset": pg.Rect(450, 300, 120, 50),                
    "Stop": pg.Rect(450, 380, 120, 50) 
}

# Tìm vị trí ô trống
def find_null(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Lấy các trạng thái lân cận
def get_neighbors(state):
    neighbors = []
    x, y = find_null(state)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Duyệt qua từng hướng di chuyển và kiểm tra hợp lệ
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    
    return neighbors

# Heuristic: Tính khoảng cách Manhattan
def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                for gi in range(3):
                    for gj in range(3):
                        if goal[gi][gj] == value:
                            distance += abs(i - gi) + abs(j - gj)
                            break
    return distance



# Nhóm thuật toán tìm kiếm không có thông tin: BFS, DFS, UCS, IDS
# Breadth-First Search
def bfs(start_state):
    queue = Queue()
    queue.put((start_state, []))
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    
    while not queue.empty():
        state, path = queue.get()
        if state == goal:
            return path
        
        for neighbor in get_neighbors(state):
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                visited.add(state_tuple)
                queue.put((neighbor, path + [neighbor]))
    
    return []

# Depth-First Search
def dfs(start_state):
    stack = LifoQueue()
    stack.put((start_state, []))
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    
    while not stack.empty():
        state, path = stack.get()
        if state == goal:
            return path
        
        for neighbor in get_neighbors(state):
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                visited.add(state_tuple)
                stack.put((neighbor, path + [neighbor]))
    
    return []

# Uninformed Cost Search
def ucs(start_state):
    pq = PriorityQueue()
    pq.put((0, start_state, []))
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    
    while not pq.empty():
        cost, state, path = pq.get()
        if state == goal:
            return path
        
        for neighbor in get_neighbors(state):
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                visited.add(state_tuple)
                pq.put((cost + 1, neighbor, path + [neighbor]))
    
    return []

# Iterative Deepening Search
def ids(start_state):
    
    # Đệ quy tìm kiếm với giới hạn độ sâu
    def depth_limit_search(state, depth_limit, path, visited):
        if state == goal:
            return path
        if depth_limit <= 0:
            return None
        visited.add(tuple(map(tuple, state)))
        for neighbor in get_neighbors(state):
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                result = depth_limit_search(neighbor, depth_limit - 1, path + [neighbor], visited)
                if result:
                    return result
        visited.remove(tuple(map(tuple, state)))
        return None

    depth = 0
    while True:
        visited = set()
        result = depth_limit_search(start_state, depth, [], visited)
        if result:
            return result
        depth += 1



# Nhóm thuật toán tìm kiếm có thông tin: Greedy, A*, IDA*
# Greedy Best-First Search
def greedy(start_state):
    pq = []
    heapq.heappush(pq, (manhattan_distance(start_state), start_state, []))
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    
    while pq:
        _, state, path = heapq.heappop(pq)
        if state == goal:
            return path
        
        for neighbor in get_neighbors(state):
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                visited.add(state_tuple)
                heapq.heappush(pq, (manhattan_distance(neighbor), neighbor, path + [neighbor]))
    
    return []

# A*
def a_star(start_state):
    pq = []
    heapq.heappush(pq, (manhattan_distance(start_state), 0, start_state, []))
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    
    while pq:
        f, g, state, path = heapq.heappop(pq)
        if state == goal:
            return path
        
        for neighbor in get_neighbors(state):
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                visited.add(state_tuple)
                new_g = g + 1
                h = manhattan_distance(neighbor)
                f = new_g + h
                heapq.heappush(pq, (f, new_g, neighbor, path + [neighbor]))
    
    return []

# Iterative Deepening A*
def ida_star(start_state):
    if start_state == goal:
        return []

    def search(state, g, threshold, path, visited):
        h = manhattan_distance(state)
        f = g + h
        if f > threshold:
            return None, f
        if state == goal:
            return path, f 
        
        min_f = float('inf')
        for neighbor in get_neighbors(state):
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                visited.add(state_tuple)
                result, new_f = search(neighbor, g + 1, threshold, path + [neighbor], visited)
                visited.remove(state_tuple)
                if result is not None:
                    return result, new_f
                min_f = min(min_f, new_f)
        return None, min_f

    threshold = manhattan_distance(start_state)
    while True:
        visited = set()
        visited.add(tuple(map(tuple, start_state)))
        result, new_threshold = search(start_state, 0, threshold, [], visited)
        if result is not None:
            return result
        if new_threshold == float('inf'):
            return []
        threshold = new_threshold



# Nhóm thuật toán tìm kiếm cục bộ: SHC, SAHC, Stochastic, SA, BS, GA
# Simple Hill Climbing
def SHC(start_state):
    current_state = [row[:] for row in start_state]
    current_distance = manhattan_distance(current_state)
    path = [current_state]
    
    visited = set()
    visited.add(tuple(map(tuple, current_state)))
    
    while True:
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break
        
        best_neighbor = None
        best_distance = float('inf')
        for neighbor in neighbors:
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                distance = manhattan_distance(neighbor)
                if distance < best_distance:
                    best_distance = distance
                    best_neighbor = neighbor
        
        if best_neighbor is None or best_distance >= current_distance:
            break
        
        current_state = best_neighbor
        current_distance = best_distance
        visited.add(tuple(map(tuple, current_state)))
        path.append(current_state)
        
        if current_state == goal:
            return path
    
    return []

# Steepest-Ascent Hill Climbing
def SAHC(start_state):
    current_state = [row[:] for row in start_state]
    current_distance = manhattan_distance(current_state)
    path = [current_state]
    
    visited = set()
    visited.add(tuple(map(tuple, current_state)))
    
    n = 1000
    for _ in range(n):
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break
        
        best_neighbor = None
        best_distance = float('inf')
        for neighbor in neighbors:
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                distance = manhattan_distance(neighbor)
                if distance < best_distance:
                    best_distance = distance
                    best_neighbor = neighbor
        
        if best_neighbor is None or best_distance >= current_distance:
            break
        
        current_state = best_neighbor
        current_distance = best_distance
        visited.add(tuple(map(tuple, current_state)))
        path.append(current_state)
        
        if current_state == goal:
            return path
    
    return []

# Stochastic Hill Climbing
def Stochastic(start_state):
    current_state = [row[:] for row in start_state]
    current_distance = manhattan_distance(current_state)
    path = [current_state]
    
    max_iterations = 1000
    probability = 0.1
    
    for _ in range(max_iterations):
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break

        neighbor = random.choice(neighbors)
        neighbor_distance = manhattan_distance(neighbor)

        if neighbor_distance < current_distance:
            current_state = neighbor
            current_distance = neighbor_distance
            path.append(current_state)
        else:
            if random.random() < probability:
                current_state = neighbor
                current_distance = neighbor_distance
                path.append(current_state)

        if current_state == goal:
            return path
    
    return []


# Tính xác suất chấp nhận trạng thái mới
def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    delta_e = new_cost - old_cost
    return math.exp(-delta_e / temperature)

# Simulated Annealing
def SA(start_state):
    current_state = [row[:] for row in start_state]
    current_distance = manhattan_distance(current_state)
    path = [current_state]
    
    T = 1.0
    T_min = 0.00001
    alpha = 0.9
    
    while T > T_min:
        i = 1
        while i <= 100:
            neighbors = get_neighbors(current_state)
            if not neighbors:
                break
            new_state = random.choice(neighbors)
            new_distance = manhattan_distance(new_state)
            
            ap = acceptance_probability(current_distance, new_distance, T)
            if ap > random.random():
                current_state = new_state
                current_distance = new_distance
                path.append(current_state)
                
                if current_state == goal:
                    return path
            
            i += 1
        
        T *= alpha
    
    if current_state == goal:
        return path
    
    return []

# Beam Search
def BS(start_state):
    current_states = [(manhattan_distance(start_state), start_state, [start_state])]
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    
    n = 1000
    for _ in range(n):
        if not current_states:
            break
        
        new_states = []
        for _, state, path in current_states:
            if state == goal:
                return path
            
            neighbors = get_neighbors(state)
            for neighbor in neighbors:
                state_tuple = tuple(map(tuple, neighbor))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    distance = manhattan_distance(neighbor)
                    new_states.append((distance, neighbor, path + [neighbor]))
        
        new_states.sort(key=lambda x: x[0])
        current_states = new_states[:2]
    
    return []

# Genetic Algorithm
def GA(start_state):
    population_size = 100  # Kích thước quần thể
    generations = 1000    # Số thế hệ
    mutation_rate = 0.1   # Tỷ lệ đột biến
    tournament_size = 5   # Kích thước giải đấu chọn lọc

    # Hàm tạo trạng thái hợp lệ và có thể giải được
    def generate_valid_state():
        while True:
            flat_list = random.sample(range(9), 9)
            state = [
                [flat_list[0], flat_list[1], flat_list[2]],
                [flat_list[3], flat_list[4], flat_list[5]],
                [flat_list[6], flat_list[7], flat_list[8]]
            ]
            if is_solvable(state):
                return state

    # Khởi tạo quần thể
    population = [deepcopy(start_state)]
    for _ in range(population_size - 1):
        population.append(generate_valid_state())

    # Hàm lai ghép: Sinh trạng thái con bằng chuỗi di chuyển hợp lệ
    def crossover(parent1, parent2):
        # Chọn ngẫu nhiên một cha mẹ làm cơ sở
        parent = deepcopy(parent1) if random.random() < 0.5 else deepcopy(parent2)
        num_moves = random.randint(1, 5)  # Số di chuyển ngẫu nhiên
        
        # Áp dụng chuỗi di chuyển hợp lệ
        current_state = deepcopy(parent)
        for _ in range(num_moves):
            neighbors = get_neighbors(current_state)
            if neighbors:
                current_state = random.choice(neighbors)
        
        return current_state

    # Hàm đột biến: Thực hiện một di chuyển hợp lệ
    def mutate(state):
        neighbors = get_neighbors(state)
        if neighbors:
            return random.choice(neighbors)
        return deepcopy(state)

    # Hàm kiểm tra trạng thái có hợp lệ và khác trạng thái trước
    def is_valid_transition(prev_state, new_state):
        neighbors = get_neighbors(prev_state)
        return any(tuple(map(tuple, neighbor)) == tuple(map(tuple, new_state)) for neighbor in neighbors)

    best_path = [deepcopy(start_state)]  # Lưu đường đi tốt nhất, bắt đầu từ start_state
    best_fitness = manhattan_distance(start_state)  # Fitness ban đầu

    for generation in range(generations):
        # Sắp xếp quần thể theo fitness
        population.sort(key=lambda x: manhattan_distance(x))
        current_best = population[0]
        current_fitness = manhattan_distance(current_best)

        # Cập nhật đường đi nếu tìm thấy trạng thái tốt hơn
        if current_fitness < best_fitness:
            best_fitness = current_fitness
            # Chỉ thêm nếu là di chuyển hợp lệ từ trạng thái trước
            if not best_path or is_valid_transition(best_path[-1], current_best):
                if not best_path or best_path[-1] != current_best:
                    best_path.append(deepcopy(current_best))

        # Kiểm tra nếu đạt trạng thái mục tiêu
        if current_best == goal:
            return best_path

        # Chọn lọc giải đấu
        new_population = []
        for _ in range(population_size):
            tournament = random.sample(population, tournament_size)
            winner = min(tournament, key=lambda x: manhattan_distance(x))
            new_population.append(deepcopy(winner))

        # Lai ghép và đột biến
        next_generation = []
        for i in range(0, population_size, 2):
            parent1 = new_population[i]
            parent2 = new_population[min(i + 1, population_size - 1)]
            
            # Sinh hai trạng thái con
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            
            # Áp dụng đột biến
            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)
            
            next_generation.extend([child1, child2])

        population = next_generation[:population_size]

    return best_path if best_path else []



# Nhóm thuật toán tìm kiếm trong môi trường phức tạp: AOGS, NOS, POS
# OR Graph Search
def or_search(state, problem, visited, depth, max_depth):
    if depth > max_depth:
        return False

    if problem['goal_test'](state):
        return []
    
    # Kiểm tra trạng thái đã được thăm chưa
    state_tuple = tuple(map(tuple, state))
    if state_tuple in visited:
        return False
    
    visited.add(state_tuple)
    
    # Thử từng hành động (trạng thái lân cận)
    for action in problem['actions'](state):
        next_states = problem['result'](state, action)
        plan = and_search(next_states, problem, visited, depth + 1, max_depth)
        if plan is not False:
            visited.remove(state_tuple)
            return [action, plan]
    
    visited.remove(state_tuple)
    return False

# And Graph Search
def and_search(states, problem, visited, depth, max_depth):
    plans = []
    for s_i in states:
        plan_i = or_search(s_i, problem, visited, depth, max_depth)
        if plan_i is False:
            return False
        plans.append(plan_i)
    
    return plans

# AND-OR Graph Search
def AOGS(start_state):
    # Định nghĩa bài toán
    problem = {
        'initial_state': start_state,
        'goal_test': lambda state: state == goal,
        'actions': get_neighbors,
        'result': lambda state, action: [action]
    }
    
    # Gọi OR-SEARCH với tập visited và giới hạn độ sâu
    visited = set()
    max_depth = 100
    plan = or_search(start_state, problem, visited, 0, max_depth)
    
    if plan is False:
        return [] 
    
    path = [start_state]
    current_plan = plan
    
    # Duyệt qua kế hoạch để lấy các trạng thái
    while current_plan:
        action = current_plan[0]
        path.append(action)
        plans = current_plan[1]
        if not plans:
            break
        current_plan = plans[0] 
    
    return path
    
    
# Kiểm tra tính khả thi của trạng thái
def is_solvable(state):
    flat = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0

# Tìm đường đi dựa trên BFS
def find_path_to_goal(start_state, goal_state):
    queue = Queue()
    queue.put((start_state, []))
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    
    while not queue.empty():
        state, path = queue.get()
        if state == goal_state:
            return path
        
        for neighbor in get_neighbors(state):
            state_tuple = tuple(map(tuple, neighbor))
            if state_tuple not in visited:
                visited.add(state_tuple)
                queue.put((neighbor, path + [neighbor]))
    
    return []

# Tạo tập hợp trạng thái đầu ngẫu nhiên
def generate_random_states(num_states, exclude_states=None):
    all_numbers = list(range(9))
    states = set()
    exclude = set() if exclude_states is None else set(exclude_states)
    
    while len(states) < num_states:
        random.shuffle(all_numbers)
        state = [
            [all_numbers[0], all_numbers[1], all_numbers[2]],
            [all_numbers[3], all_numbers[4], all_numbers[5]],
            [all_numbers[6], all_numbers[7], all_numbers[8]]
        ]
        if is_solvable(state):  # Kiểm tra tính khả thi
            state_tuple = tuple(map(tuple, state))
            if state_tuple not in exclude:
                states.add(state_tuple)
    return states

# No Observable Search
def NOS():
    global nos_belief_states, nos_goal_states, solution_steps, found_goal_state
    
    nos_goal_states = generate_random_states(5)
    nos_belief_states = generate_random_states(10, exclude_states=nos_goal_states)
    initial_selected_state = random.choice(list(nos_belief_states))
    
    # Kiểm tra tính khả thi của initial_selected_state
    if not is_solvable(list(map(list, initial_selected_state))):
        # Nếu không khả thi, chọn lại trạng thái khác
        for state in nos_belief_states:
            if is_solvable(list(map(list, state))):
                initial_selected_state = state
                break
    
    def is_goal_belief(belief_state, goal_states):
        for state in belief_state:
            if state in goal_states:
                global found_goal_state
                found_goal_state = state
                return state, True
        return None, False
    
    def apply_action_to_belief(belief_state, action_func):
        new_belief_state = set()
        for state in belief_state:
            state_list = [list(row) for row in state]
            neighbors = action_func(state_list)
            for neighbor in neighbors:
                new_belief_state.add(tuple(map(tuple, neighbor)))
        return new_belief_state
    
    queue = Queue()
    queue.put((nos_belief_states, [], initial_selected_state))
    visited = set()
    
    moves = [
        ("Right", lambda state: [n for n in get_neighbors(state) if find_null(n)[1] > find_null(state)[1]]),
        ("Left", lambda state: [n for n in get_neighbors(state) if find_null(n)[1] < find_null(state)[1]]),
        ("Down", lambda state: [n for n in get_neighbors(state) if find_null(n)[0] > find_null(state)[0]]),
        ("Up", lambda state: [n for n in get_neighbors(state) if find_null(n)[0] < find_null(state)[0]])
    ]
    
    while not queue.empty():
        current_belief_state, path, current_state = queue.get()
        belief_tuple = frozenset(current_belief_state)
        if belief_tuple in visited:
            continue
        visited.add(belief_tuple)
        
        matched_state, is_goal = is_goal_belief(current_belief_state, nos_goal_states)
        if is_goal:
            # Tìm đường đi thực tế từ initial_selected_state đến matched_state
            initial_state_list = list(map(list, initial_selected_state))
            matched_state_list = list(map(list, matched_state))
            path_to_goal = find_path_to_goal(initial_state_list, matched_state_list)
            
            # Xây dựng result_path
            result_path = [initial_state_list] + path_to_goal
            if not path_to_goal:  # Nếu không tìm thấy đường đi
                print("Không thể tìm đường đi từ initial_selected_state đến matched_state")
                return []
            
            return result_path
        
        for action_name, action_func in moves:
            new_belief_state = apply_action_to_belief(current_belief_state, action_func)
            if new_belief_state:
                neighbors = action_func(list(map(list, current_state)))
                next_state = neighbors[0] if neighbors else current_state
                new_path = path + [(action_name, new_belief_state)]
                queue.put((new_belief_state, new_path, next_state))
    
    return []  # Không tìm thấy lời giải


# Hàm tạo trạng thái ngẫu nhiên với 3 ô đầu cố định là [1, 2, 3]
def generate_random_states_with_fixed_top_row(num_states, exclude_states=None):
    states = set()
    exclude = set() if exclude_states is None else set(exclude_states)
    
    while len(states) < num_states:
        remaining_numbers = [0, 4, 5, 6, 7, 8]
        random.shuffle(remaining_numbers)
        state = [
            [1, 2, 3],
            [remaining_numbers[0], remaining_numbers[1], remaining_numbers[2]],
            [remaining_numbers[3], remaining_numbers[4], remaining_numbers[5]]
        ]
        if is_solvable(state):  # Kiểm tra tính khả thi
            state_tuple = tuple(map(tuple, state))
            if state_tuple not in exclude:
                states.add(state_tuple)
    return states

# Partial Observable Search
def POS():
    global pos_belief_states, pos_goal_states, solution_steps, selected_goal_state
    
    # Tạo goal states với 3 ô đầu là [1, 2, 3]
    pos_goal_states = generate_random_states_with_fixed_top_row(5)
    selected_pos_goal = random.choice(list(pos_goal_states))
    
    # Tạo belief states, đảm bảo không trùng với goal states
    pos_belief_states = generate_random_states(10, exclude_states=pos_goal_states)
    
    # Chọn initial_selected_state có hàng đầu là [1, 2, 3] nếu có thể
    initial_selected_state = None
    for state in pos_belief_states:
        state_list = list(map(list, state))
        if state_list[0][0] == 1 and state_list[0][1] == 2 and state_list[0][2] == 3:
            initial_selected_state = state
            break
    if initial_selected_state is None:
        initial_selected_state = random.choice(list(pos_belief_states))
    
    # Kiểm tra tính khả thi của initial_selected_state
    if not is_solvable(list(map(list, initial_selected_state))):
        for state in pos_belief_states:
            if is_solvable(list(map(list, state))):
                initial_selected_state = state
                break
    
    def is_goal_belief(belief_state, goal_state):
        goal_tuple = tuple(map(tuple, goal_state))
        for state in belief_state:
            if state == goal_tuple:
                return state, True
        return None, False
    
    def filter_belief_state(belief_state):
        filtered = set()
        for state in belief_state:
            state_list = list(map(list, state))
            if state_list[0][0] == 1 and state_list[0][1] == 2 and state_list[0][2] == 3:
                filtered.add(state)
        return filtered
    
    def apply_action_to_belief(belief_state, action_func):
        new_belief_state = set()
        for state in belief_state:
            state_list = [list(row) for row in state]
            neighbors = action_func(state_list)
            for neighbor in neighbors:
                new_belief_state.add(tuple(map(tuple, neighbor)))
        return new_belief_state
    
    queue = Queue()
    queue.put((pos_belief_states, [], initial_selected_state))
    visited = set()
    
    moves = [
        ("Right", lambda state: [n for n in get_neighbors(state) if find_null(n)[1] > find_null(state)[1]]),
        ("Left", lambda state: [n for n in get_neighbors(state) if find_null(n)[1] < find_null(state)[1]]),
        ("Down", lambda state: [n for n in get_neighbors(state) if find_null(n)[0] > find_null(state)[0]]),
        ("Up", lambda state: [n for n in get_neighbors(state) if find_null(n)[0] < find_null(state)[0]])
    ]
    
    while not queue.empty():
        current_belief_state, path, current_state = queue.get()
        belief_tuple = frozenset(current_belief_state)
        if belief_tuple in visited:
            continue
        visited.add(belief_tuple)
        
        # Lọc belief state
        filtered_belief_state = filter_belief_state(current_belief_state)
        if not filtered_belief_state:
            continue
        
        # Kiểm tra mục tiêu
        matched_state, is_goal = is_goal_belief(filtered_belief_state, selected_pos_goal)
        if is_goal:
            # Lưu trạng thái mục tiêu được chọn
            selected_goal_state = matched_state
            # Tìm đường đi thực tế từ initial_selected_state đến matched_state
            initial_state_list = list(map(list, initial_selected_state))
            matched_state_list = list(map(list, matched_state))
            path_to_goal = find_path_to_goal(initial_state_list, matched_state_list)
            
            # Xây dựng result_path
            result_path = [initial_state_list] + path_to_goal
            if not path_to_goal:  # Nếu không tìm thấy đường đi
                print("Không thể tìm đường đi từ initial_selected_state đến matched_state")
                return []
            
            return result_path
        
        for action_name, action_func in moves:
            new_belief_state = apply_action_to_belief(filtered_belief_state, action_func)
            if new_belief_state:
                neighbors = action_func(list(map(list, current_state)))
                next_state = neighbors[0] if neighbors else current_state
                new_path = path + [(action_name, new_belief_state)]
                queue.put((new_belief_state, new_path, next_state))
    
    return []  # Không tìm thấy lời giải



# Nhóm thuật toán tìm kiếm có ràng buộc: BT, AC-3
# Backtracking
def BT(start_state):
    visited = set()
    
    # Hàm đệ quy với giới hạn độ sâu
    def backtrack(state, path, depth, max_depth):
        if state == goal:
            return path
        
        if depth > max_depth:
            return None
        
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            return None
        visited.add(state_tuple)
        
        # Duyệt qua các trạng thái lân cận
        for neighbor in get_neighbors(state):
            result = backtrack(neighbor, path + [neighbor], depth + 1, max_depth)
            if result is not None:
                return result
        visited.remove(state_tuple)
        return None
    
    max_depth = 50
    result = backtrack(start_state, [start_state], 0, max_depth)
    if result:
        return result
    else:
        return []

# Hàm định nghĩa CSP cho 8-Puzzle
def define_8puzzle_csp(state):
    variables = list(range(1, 10))
    
    # Miền giá trị 0 - 8
    domains = {var: set(range(9)) for var in variables}
    
    # Ràng buộc: "all different" giữa các ô
    constraints = []
    for i in range(1, 10):
        for j in range(i + 1, 10):
            constraints.append((i, j))  
    
    # Gán giá trị ban đầu dựa trên trạng thái
    for i in range(3):
        for j in range(3):
            var = i * 3 + j + 1
            value = state[i][j]
            domains[var] = {value}
    
    # Xây dựng danh sách hàng xóm cho từng biến
    neighbors = defaultdict(list)
    for var1, var2 in constraints:
        neighbors[var1].append(var2)
        neighbors[var2].append(var1)
    
    return variables, domains, constraints, neighbors

def rm_inconsistent_values(xi, xj, domains, constraints):
    removed = False
    values_to_remove = set()
    
    # Duyệt qua từng giá trị z trong miền của Xi
    for z in domains[xi]:
        consistent = False
        for y in domains[xj]:
            if z != y:
                consistent = True
                break
        if not consistent:
            values_to_remove.add(z)
            removed = True
    
    # Xóa các giá trị không thỏa mãn khỏi miền của Xi
    domains[xi] -= values_to_remove
    return removed

# Hàm AC-3
def ac3(csp):
    from collections import defaultdict
    variables, domains, constraints, neighbors = csp
    queue = Queue()
    
    for xi, xj in constraints:
        queue.put((xi, xj))
    
    while not queue.empty():
        xi, xj = queue.get()
        if rm_inconsistent_values(xi, xj, domains, constraints):
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.put((xk, xi))
    
    return domains

# Hàm kiểm tra xem CSP có giải được không
def is_solvable_csp(domains):
    for var in domains:
        if not domains[var]:
            return False
    return True

# AC-3
def AC_3(start_state):
    global solution_steps
    
    # Kiểm tra tính khả thi của trạng thái ban đầu và mục tiêu
    if not is_solvable(start_state) or not is_solvable(goal):
        print("Trạng thái ban đầu hoặc mục tiêu không khả thi.")
        return []

    # Định nghĩa CSP
    variables, domains, constraints, neighbors = define_8puzzle_csp(start_state)
    csp = (variables, domains, constraints, neighbors)
    
    # Áp dụng AC-3 để giảm miền giá trị
    domains = ac3(csp)
    
    # Kiểm tra xem CSP có giải được không
    if not is_solvable_csp(domains):
        print("Không thể giải bài toán sau khi áp dụng AC-3: có miền rỗng.")
        return []
    
    # Dùng backtracking để tìm lời giải
    def backtrack(state, goal, depth, max_depth):
        if state == goal:
            return [state]
        
        if depth > max_depth:
            return None
        
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            return None
        
        visited.add(state_tuple)
        
        for neighbor in get_neighbors(state):
            result = backtrack(neighbor, goal, depth + 1, max_depth)
            if result is not None:
                return [state] + result
        visited.remove(state_tuple)
        return None
    
    max_depth = 50  # Giới hạn độ sâu tối đa
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    solution_steps = backtrack(start_state, goal, 0, max_depth)
    
    return solution_steps if solution_steps else []



# Nhóm thuật toán học củng cố: Q-learning
Q_TABLE = defaultdict(lambda: defaultdict(float))  
LEARNING_RATE = 0.1  
DISCOUNT_FACTOR = 0.9  
EPSILON = 0.3  
EPISODES = 5000 
MAX_STEPS_PER_EPISODE = 500

# Hàm tính phần thưởng
def get_reward(current_state, next_state):
    if next_state == goal:
        return 0 
    return -1  

# Hàm chuyển trạng thái để lưu vào Q-table
def state_to_tuple(state):
    return tuple(map(tuple, state))

# Q-Learning
def Q_learning(start_state, goal_state, episodes=EPISODES, max_steps=MAX_STEPS_PER_EPISODE):
    global Q_TABLE
    solution_steps = []

    for episode in range(episodes):
        current_state = [row[:] for row in start_state] 
        steps = 0
        
        while steps < max_steps:
            state_tuple = state_to_tuple(current_state)
            
            # epsilon-greedy chọn hành động
            if random.uniform(0, 1) < EPSILON:
                action = random.choice(get_neighbors(current_state))
            else:
                # Chọn hành động có Q-value cao nhất
                neighbors = get_neighbors(current_state)
                if not neighbors:
                    break
                max_q_value = float('-inf')
                best_action = neighbors[0]
                for neighbor in neighbors:
                    neighbor_tuple = state_to_tuple(neighbor)
                    q_value = Q_TABLE[state_tuple][neighbor_tuple]
                    if q_value > max_q_value:
                        max_q_value = q_value
                        best_action = neighbor
                action = best_action
            
            next_state = [row[:] for row in action]
            next_state_tuple = state_to_tuple(next_state)
            
            # Tính target để cập nhật Q-value
            reward = get_reward(current_state, next_state)
            max_future_q = max([Q_TABLE[state_to_tuple(neighbor)].get(state_to_tuple(neighbor), 0)
                               for neighbor in get_neighbors(next_state)], default=0)
            td_target = reward + DISCOUNT_FACTOR * max_future_q
            
            # Cập nhật Q-value 
            old_q = Q_TABLE[state_tuple][next_state_tuple]
            Q_TABLE[state_tuple][next_state_tuple] += LEARNING_RATE * (td_target - old_q)
 
            current_state = next_state
            solution_steps.append(current_state)
            
            if current_state == goal_state:
                break
            
            steps += 1
    
    return solution_steps


# Hàm vẽ trạng thái nhỏ (dùng để hiển thị nhiều trạng thái ngẫu nhiên)
def draw_small_state(state, x, y):
    for i in range(3):
        for j in range(3):
            pg.draw.rect(screen, GRAY, (j*40+x, i*40+y, 40, 40))
            value = state[i][j]
            if value != 0:
                text = pg.font.Font(None, 20).render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j*40+x+20, i*40+y+20))
                screen.blit(text, text_rect)

# Vẽ giao diện cho NOS
def draw_nos(current_state, steps=None):
    screen.fill(WHITE)
    
    title = font_title.render("No Observable Search", True, BLACK)
    screen.blit(title, (50, 20))
    
    # Hiển thị trạng thái hiện tại
    start_title = font_title.render("Current State", True, BLACK)
    screen.blit(start_title, (50, 70))
    for i in range(3):
        for j in range(3):
            value = current_state[i][j]
            if value != 0:
                pg.draw.rect(screen, GRAY, (j*120+50, i*120+120, 120, 120))
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j*120+110, i*120+180))
                screen.blit(text, text_rect)
    
    # Hiển thị trạng thái mục tiêu
    goal_state = steps[-1] if steps else list(map(list, list(nos_goal_states)[0]))
    goal_title = font_title.render("Goal State", True, BLACK)
    screen.blit(goal_title, (600, 70))
    for i in range(3):
        for j in range(3):
            value = goal_state[i][j]
            if value != 0:
                pg.draw.rect(screen, GRAY, (j*120+600, i*120+120, 120, 120))
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j*120+660, i*120+180))
                screen.blit(text, text_rect)
    
    # Hiển thị số bước
    if steps is not None:
        step_count_text = font.render(f"So buoc: {len(steps) if steps else 0}", True, BLACK)
        screen.blit(step_count_text, (50, 500))
    
    # Hiển thị thời gian thực thi
    if "NOS" in execution_times:
        time_text = font.render(f"Thoi gian: {execution_times['NOS']:.4f}s", True, BLACK)
        screen.blit(time_text, (600, 500))
        
    # Hiển thị các trạng thái ban đầu ngẫu nhiên
    belief_title = font.render("Initial Belief States:", True, BLACK)
    screen.blit(belief_title, (50, 550))
    for idx, state in enumerate(nos_belief_states):
        if idx < 5:
            x = 50 + idx * 150
            y = 600
            draw_small_state(list(map(list, state)), x, y)
        else:
            x = 50 + (idx - 5) * 150
            y = 750
            draw_small_state(list(map(list, state)), x, y)
    
    goal_states_title = font.render("Goal States:", True, BLACK)
    screen.blit(goal_states_title, (50, 900))
    for idx, state in enumerate(nos_goal_states):
        x = 50 + idx * 150
        y = 950
        draw_small_state(list(map(list, state)), x, y)

# Vẽ giao diện cho POS
def draw_pos(current_state, steps=None):
    screen.fill(WHITE)
    
    # Tiêu đề
    title = font_title.render("Partial Observable Search", True, BLACK)
    screen.blit(title, (50, 20))
    
    # Hiển thị trạng thái hiện tại
    start_title = font_title.render("Current State", True, BLACK)
    screen.blit(start_title, (50, 70))
    for i in range(3):
        for j in range(3):
            value = current_state[i][j]
            if value != 0:
                pg.draw.rect(screen, GRAY, (j*120+50, i*120+120, 120, 120))
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j*120+110, i*120+180))
                screen.blit(text, text_rect)
    
    # Hiển thị trạng thái mục tiêu
    goal_title = font_title.render("Goal State", True, BLACK)
    screen.blit(goal_title, (600, 70))
    for i in range(3):
        for j in range(3):
            if i == 0 and j in [0, 1, 2]:
                value = 1 if j == 0 else 2 if j == 1 else 3
                pg.draw.rect(screen, GRAY, (j*120+600, i*120+120, 120, 120))
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j*120+660, i*120+180))
                screen.blit(text, text_rect)
            else:
                pg.draw.rect(screen, GRAY, (j*120+600, i*120+120, 120, 120))
                text = font.render("?", True, BLACK)
                text_rect = text.get_rect(center=(j*120+660, i*120+180))
                screen.blit(text, text_rect)
    
    # Hiển thị số bước
    if steps is not None:
        step_count_text = font.render(f"So buoc: {len(steps) if steps else 0}", True, BLACK)
        screen.blit(step_count_text, (50, 500))
        
    # Hiển thị thời gian thực thi
    if "POS" in execution_times:
        time_text = font.render(f"Thoi gian: {execution_times['POS']:.4f}s", True, BLACK)
        screen.blit(time_text, (600, 500))
    
    # Hiển thị các trạng thái ban đầu ngẫu nhiên
    belief_title = font.render("Initial Belief States:", True, BLACK)
    screen.blit(belief_title, (50, 550))
    for idx, state in enumerate(pos_belief_states):
        if idx < 5:
            x = 50 + idx * 150
            y = 600
            draw_small_state(list(map(list, state)), x, y)
        else:
            x = 50 + (idx - 5) * 150
            y = 750
            draw_small_state(list(map(list, state)), x, y)
    
    # Hiển thị các trạng thái mục tiêu
    goal_states_title = font.render("Goal States:", True, BLACK)
    screen.blit(goal_states_title, (50, 900))
    for idx, state in enumerate(pos_goal_states):
        x = 50 + idx * 150
        y = 950
        draw_small_state(list(map(list, state)), x, y)

execution_times = {}

# Vẽ puzzle (Start và Goal)
def draw_puzzle(start_state, goal_state, steps=None):
    screen.fill(WHITE)
    
    # Start State
    start_title = font_title.render("Start State", True, BLACK)
    screen.blit(start_title, (50, 20))
    for i in range(3):
        for j in range(3):
            value = start_state[i][j]
            if value != 0:
                pg.draw.rect(screen, GRAY, (j*120+50, i*120+70, 120, 120))
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j*120+110, i*120+130))
                screen.blit(text, text_rect)
    
    # Goal State
    goal_title = font_title.render("Goal State", True, BLACK)
    screen.blit(goal_title, (600, 20))
    for i in range(3):
        for j in range(3):
            value = goal_state[i][j]
            if value != 0:
                pg.draw.rect(screen, GRAY, (j*120+600, i*120+70, 120, 120))
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j*120+660, i*120+130))
                screen.blit(text, text_rect)
    
    # Hiển thị số bước
    if steps is not None:
        step_text = font.render(f"So buoc: {steps}", True, BLACK)
        screen.blit(step_text, (50, 480))

    # Hiển thị thời gian thực thi của thuật toán hiện tại
    current_algo = [algo for algo in execution_times if execution_times[algo] > 0]
    if current_algo:
        time_text = font.render(f"Thoi gian: {execution_times[current_algo[-1]]:.4f}s", True, BLACK)
        screen.blit(time_text, (600, 480))
                    

# In các bước giải ra console
def print_path(steps):
    if not steps:
        print("Khong giai duoc")
        return
    print("Cac buoc giai:")
    for i, step in enumerate(steps):
        print(f"Buoc {i + 1}:")
        for row in step:
            print(row)
        print()

# Hàm vẽ biểu đồ so sánh
def plot_comparison(group):
    algorithms = ALGORITHM_GROUPS[group]
    times = [execution_times.get(algo, 0) for algo in algorithms]
    
    plt.figure(figsize=(7, 5))
    plt.bar(algorithms, times, color='steelblue')
    plt.xlabel('Thuật toán')
    plt.ylabel('Thời gian thực thi (giây)')
    plt.title(f'So sánh thời gian thực thi - Nhóm {group}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    
# Xử lý giải thuật khi nhấn nút
def solve(algo):
    global solution_steps, current_mode, found_goal_state
    solution_steps = []
    found_goal_state = None
    
    start_time = time.time()
    
    if algo == "BFS":
        current_mode = "default"
        solution_steps = bfs(start)
    elif algo == "DFS":
        current_mode = "default"
        solution_steps = dfs(start)
    elif algo == "UCS":
        current_mode = "default"
        solution_steps = ucs(start)
    elif algo == "IDS":
        current_mode = "default"
        solution_steps = ids(start)
    elif algo == "Greedy":
        current_mode = "default"
        solution_steps = greedy(start)
    elif algo == "A*":
        current_mode = "default"
        solution_steps = a_star(start)
    elif algo == "IDA*":
        current_mode = "default"
        solution_steps = ida_star(start)
    elif algo == "SHC":
        current_mode = "default"
        solution_steps = SHC(start)
    elif algo == "SAHC":
        current_mode = "default"
        solution_steps = SAHC(start)
    elif algo == "Stochastic":
        current_mode = "default"
        solution_steps = Stochastic(start)
    elif algo == "SA":
        current_mode = "default"
        solution_steps = SA(start)
    elif algo == "BS":
        current_mode = "default"
        solution_steps = BS(start)
    elif algo == "GA":
        current_mode = "default"
        solution_steps = GA(start)
    elif algo == "AOGS":
        current_mode = "default"
        solution_steps = AOGS(start)
    elif algo == "NOS":
        current_mode = "NOS"
        solution_steps = NOS()
    elif algo == "POS":
        current_mode = "POS"
        solution_steps = POS()
    elif algo == "BT":
        current_mode = "default"
        solution_steps = BT(start)
    elif algo == "AC-3":
        current_mode = "default"
        solution_steps = AC_3(start)
    elif algo == "Q-learning":
        current_mode = "default"
        solution_steps = Q_learning(start, goal)
        
    end_time = time.time()  
    execution_times[algo] = end_time - start_time  
    
    print(f"\nKet qua chay thuat toan {algo}:")
    print_path(solution_steps)


running = True
current_step = 0
is_playing = True

while running:
    screen.fill(WHITE)
    
    if current_mode in ["NOS", "POS"]:
        visible_buttons = {name: rect for name, rect in buttons.items() if name in ["NOS", "POS", "Reset", "Stop"]}
    else:
        visible_buttons = buttons

    if current_mode == "default":
        if current_step >= len(solution_steps):
            draw_puzzle(start, goal, len(solution_steps) if solution_steps else None)
        else:
            draw_puzzle(solution_steps[current_step], goal, len(solution_steps))
    elif current_mode == "NOS":
        if current_step >= len(solution_steps):
            draw_nos(solution_steps[-1] if solution_steps else list(map(list, list(nos_belief_states)[0])), solution_steps)
        else:
            draw_nos(solution_steps[current_step], solution_steps)
    elif current_mode == "POS":
        if current_step >= len(solution_steps):
            draw_pos(solution_steps[-1] if solution_steps else list(map(list, list(pos_belief_states)[0])), solution_steps)
        else:
            draw_pos(solution_steps[current_step], solution_steps)

    for name, rect in visible_buttons.items():
        if name in ALGORITHM_GROUPS:
            color = DARK_GREEN
        else:
            color = BLUE if name not in ["Reset", "Stop"] else RED
        pg.draw.rect(screen, color, rect)
        text = font_button.render(name, True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            for name, rect in visible_buttons.items():
                if rect.collidepoint(event.pos):
                    if name == "Reset":
                        start = [row[:] for row in initial_start]
                        current_step = 0
                        solution_steps = []
                        current_mode = "default"
                        nos_belief_states = set()
                        nos_goal_states = set()
                        pos_belief_states = set()
                        pos_goal_states = set()
                        found_goal_state = None
                        selected_goal_state = None
                        is_playing = True
                    elif name == "Stop":
                        is_playing = False
                        if solution_steps and current_step < len(solution_steps):
                            start = [row[:] for row in solution_steps[current_step]]
                    elif name in ALGORITHM_GROUPS:
                        plot_comparison(name)
                    else:
                        solve(name)
                        current_step = 0
                        is_playing = True
    
    if is_playing and solution_steps and current_step < len(solution_steps) - 1:
        current_step += 1
        time.sleep(0.1)

pg.quit()
