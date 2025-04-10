import pygame as pg
import time
from queue import Queue, LifoQueue, PriorityQueue
import heapq
import random
import math

pg.init()

WIDTH, HEIGHT = 1000, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("23110213_VanPhuHien")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

font = pg.font.Font(None, 48)
font_button = pg.font.Font(None, 40)
font_title = pg.font.Font(None, 50)

# Trạng thái ban đầu và mục tiêu
initial_start = [[2, 6, 5], [8, 7, 0], [4, 3, 1]]
start = [row[:] for row in initial_start]
goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
solution_steps = []

# Vị trí các nút
buttons = {
    "BFS": pg.Rect(50, 550, 150, 50),
    "DFS": pg.Rect(220, 550, 150, 50),
    "UCS": pg.Rect(390, 550, 150, 50),
    "IDS": pg.Rect(560, 550, 150, 50),
    "Greedy": pg.Rect(730, 550, 150, 50),
    "A*": pg.Rect(50, 620, 150, 50),
    "IDA*": pg.Rect(220, 620, 150, 50),
    "SHC": pg.Rect(390, 620, 150, 50),
    "SAHC": pg.Rect(560, 620, 150, 50),
    "Stochastic": pg.Rect(730, 620, 150, 50),
    "SA": pg.Rect(50, 690, 150, 50),
    "BS": pg.Rect(220, 690, 150, 50),
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
    
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    
    return neighbors

# Heuristic: Tính tổng khoảng cách Manhattan
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

# BFS
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

# DFS
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

# UCS
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

# IDS
def ids(start_state):
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

# IDA*
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
    
    # Các nút
    for name, rect in buttons.items():
        color = BLUE if name not in ["Reset", "Stop"] else RED
        pg.draw.rect(screen, color, rect)
        text = font_button.render(name, True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
    
    pg.display.flip()

# In các bước giải ra console
def print_path(steps):
    if not steps:
        print("Ko giai duoc")
        return
    print("Cac buoc giai:")
    for i, step in enumerate(steps):
        print(f"Buoc {i + 1}:")
        for row in step:
            print(row)
        print()

# Xử lý giải thuật khi nhấn nút
def solve(algo):
    global solution_steps
    solution_steps = []
    
    if algo == "BFS":
        solution_steps = bfs(start)
    elif algo == "DFS":
        solution_steps = dfs(start)
    elif algo == "UCS":
        solution_steps = ucs(start)
    elif algo == "IDS":
        solution_steps = ids(start)
    elif algo == "Greedy":
        solution_steps = greedy(start)
    elif algo == "A*":
        solution_steps = a_star(start)
    elif algo == "IDA*":
        solution_steps = ida_star(start)
    elif algo == "SHC":
        solution_steps = SHC(start)
    elif algo == "SAHC":
        solution_steps = SAHC(start)
    elif algo == "Stochastic":
        solution_steps = Stochastic(start)
    elif algo == "SA":
        solution_steps = SA(start)
    elif algo == "BS":
        solution_steps = BS(start)
    
    print(f"\nKet qua chay thuat toan {algo}:")
    print_path(solution_steps)

running = True
current_step = 0
is_playing = True  

while running:
    screen.fill(WHITE)
    
    if current_step >= len(solution_steps):
        draw_puzzle(start, goal, len(solution_steps) if solution_steps else None)
    else:
        draw_puzzle(solution_steps[current_step], goal, len(solution_steps))
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            for name, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    if name == "Reset":
                        start = [row[:] for row in initial_start]
                        current_step = 0
                        solution_steps = []
                        is_playing = True
                    elif name == "Stop":
                        is_playing = False
                        if solution_steps and current_step < len(solution_steps):
                            start = [row[:] for row in solution_steps[current_step]]
                    else:
                        solve(name)
                        current_step = 0
                        is_playing = True  
    
    if is_playing and solution_steps and current_step < len(solution_steps) - 1:
        current_step += 1
        time.sleep(0.1)
    
    pg.display.flip()

pg.quit()