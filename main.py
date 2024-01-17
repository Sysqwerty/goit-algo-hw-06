import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Завдання 1: Створення та візуалізація графа

# Створення графа
G = nx.Graph()

# Додавання вершин (наприклад, вулиць міста Києва)
streets = ["Khreschatyk", "Independence Ave", "Bessarabska Square", "Maidan Nezalezhnosti", "Andriyivsky Descent"]
G.add_nodes_from(streets)

# Додавання ребер (зв'язків між вулицями)
connections = [("Khreschatyk", "Independence Ave"),
               ("Khreschatyk", "Maidan Nezalezhnosti"),
               ("Independence Ave", "Bessarabska Square"),
               ("Bessarabska Square", "Maidan Nezalezhnosti"),
               ("Maidan Nezalezhnosti", "Andriyivsky Descent")]

G.add_edges_from(connections)

# Візуалізація графа
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, node_color='skyblue', font_size=10,
        edge_color='gray')
plt.title("Мережа вулиць міста Києва")
plt.show()

# Аналіз основних характеристик графа
print(f"Cписок усіх вузлів графа: {G.nodes()}")
print(f"Cписок усіх ребер графа: {G.edges()}")
print(f"Кількість вершин: {G.number_of_nodes()}")
print(f"Кількість ребер: {G.number_of_edges()}")
print(f"Ступінь вершин: {dict(G.degree())}")
print(f"Граф є зв'язним: {nx.is_connected(G)}")
print(f"Ступінь центральності (Degree Centrality): {nx.degree_centrality(G)}")
print(f"Близькість вузла (Closeness Centrality): {nx.closeness_centrality(G)}")
print(f"Посередництво вузла (Betweenness Centrality): {nx.betweenness_centrality(G)}")


# Завдання 2: DFS і BFS алгоритми для знаходження шляхів

def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next_node in set(graph[start]) - set(path):
        yield from dfs_paths(graph, next_node, goal, path + [next_node])


def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (node, path) = queue.pop(0)
        for next_node in set(graph[node]) - set(path):
            if next_node == goal:
                yield path + [next_node]
            else:
                queue.append((next_node, path + [next_node]))


# Використання DFS/BFS для створеного графа G
start_node = "Khreschatyk"
goal_node = "Andriyivsky Descent"

dfs_result = list(dfs_paths(G, start_node, goal_node))
bfs_result = list(bfs_paths(G, start_node, goal_node))

print("DFS шляхи:", dfs_result)
print("BFS шляхи:", bfs_result)


# Завдання 3: Алгоритм Дейкстри для знаходження найкоротшого шляху

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph[current_node]:
            distance = current_distance + graph[current_node][neighbor]['weight']
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


# Додавання ваги до ребер графа G (відстань між вулицями)
edge_weights = {("Khreschatyk", "Independence Ave"): 2,
                ("Khreschatyk", "Maidan Nezalezhnosti"): 1,
                ("Independence Ave", "Bessarabska Square"): 3,
                ("Bessarabska Square", "Maidan Nezalezhnosti"): 2,
                ("Maidan Nezalezhnosti", "Andriyivsky Descent"): 4}

G_with_weights = G.copy()
nx.set_edge_attributes(G_with_weights, edge_weights, 'weight')

# Використання алгоритму Дейкстри для знаходження найкоротших шляхів
start_node_dijkstra = "Khreschatyk"
shortest_paths = {node: dijkstra(G_with_weights, node) for node in G_with_weights}

print("Найкоротші шляхи за алгоритмом Дейкстри:")
for node in G_with_weights:
    print(f"Від {start_node_dijkstra} до {node}: {shortest_paths[start_node_dijkstra][node]}")

# Візуалізація графа з вагами
pos2 = nx.spring_layout(G_with_weights)

# Визначення ваги ребер
edge_labels = {(node1, node2): attr['weight'] for node1, node2, attr in G_with_weights.edges(data=True)}

nx.draw(G_with_weights, pos2, with_labels=True, font_weight='bold', node_size=1000, node_color='skyblue', font_size=10,
        edge_color='gray')
nx.draw_networkx_edge_labels(G_with_weights, pos2, edge_labels=edge_labels)

plt.title("Мережа міста Києва з вагами")
plt.show()
