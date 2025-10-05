import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Зв'язки Термінал -> Склад
edges_terminal_to_warehouse = [
    ("Термінал 1", "Склад 1", 25), 
    ("Термінал 1", "Склад 2", 20), 
    ("Термінал 1", "Склад 3", 15), 
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
]

# Зв'язки Склад -> Магазин
edges_warehouse_to_store = [
    ("Склад 1", "Магазин 1", 15), 
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

G.add_weighted_edges_from(edges_terminal_to_warehouse, weight='capacity')
G.add_weighted_edges_from(edges_warehouse_to_store, weight='capacity')

pos = {
    # Термінали (Джерело)
    "Термінал 1": (1, 2.5),
    "Термінал 2": (5, 2.5),
    
    # Склади (Проміжні вузли)
    "Склад 1": (2, 4),
    "Склад 2": (4.5, 3.5), 
    "Склад 3": (2.5, 1.5), 
    "Склад 4": (4, 1),
  
    # Магазини Складу 1
    "Магазин 1": (1, 5),
    "Магазин 2": (2, 5),
    "Магазин 3": (3, 5),
    
    # Магазини Складу 2
    "Магазин 4": (4, 5),
    "Магазин 5": (5, 5),
    "Магазин 6": (6, 5),
    
    # Магазини Складу 3
    "Магазин 7": (1.5, 0),
    "Магазин 8": (2.5, 0),
    "Магазин 9": (3.5, 0),
    
    # Магазини Складу 4
    "Магазин 10": (4.5, 0),
    "Магазин 11": (5.5, 0),
    "Магазин 12": (6.5, 0),
    "Магазин 13": (7.5, 0),
    "Магазин 14": (8.5, 0),
}


plt.figure(figsize=(16, 9))

node_colors = {}
for node in G.nodes():
    if "Термінал" in node:
        node_colors[node] = "lightcoral"  # Червоний для джерела
    elif "Склад" in node:
        node_colors[node] = "skyblue"    # Синій для проміжних
    elif "Магазин" in node:
        node_colors[node] = "lightgreen" # Зелений для стоку

color_list = [node_colors[node] for node in G.nodes()]

nx.draw(
    G, 
    pos, 
    with_labels=True, 
    node_size=1500, 
    node_color=color_list, 
    font_size=10, 
    font_weight="bold", 
    arrows=True,
    edge_color='gray'
)

labels = nx.get_edge_attributes(G, 'capacity')

nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red', font_size=8)

plt.title("Повна Логістична Мережа та Пропускна Здатність", size=15)
plt.axis('off')
plt.show()

