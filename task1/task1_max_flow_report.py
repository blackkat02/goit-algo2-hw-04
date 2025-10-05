import os
import sys
import numpy as np
from collections import deque

# --- NODE CONSTANTS ---
S = 0    # Super-Source
T1 = 1   # Terminal 1
T2 = 2   # Terminal 2
W1 = 3   # Warehouse 1
W2 = 4   # Warehouse 2
W3 = 5   # Warehouse 3
W4 = 6   # Warehouse 4
T = 21   # Super-Sink
NUM_NODES = 22
INF = 1000 

# Node Names for output
NODE_NAMES = {
    0: 'S', 1: 'T1', 2: 'T2', 3: 'W1', 4: 'W2', 5: 'W3', 6: 'W4', 21: 'T',
    **{i: f'M{i-6}' for i in range(7, 21)} 
}

# --- CAPACITY MATRIX INITIALIZATION (Same logic, indices, and values) ---
capacity_matrix_np = np.zeros((NUM_NODES, NUM_NODES), dtype=int)
capacity_matrix_np[S, T1] = INF; capacity_matrix_np[S, T2] = INF
capacity_matrix_np[T1, W1] = 25; capacity_matrix_np[T1, W2] = 20; capacity_matrix_np[T1, W3] = 15
capacity_matrix_np[T2, W3] = 15; capacity_matrix_np[T2, W4] = 30; capacity_matrix_np[T2, W2] = 10
capacity_matrix_np[W1, 7] = 15; capacity_matrix_np[W1, 8] = 10; capacity_matrix_np[W1, 9] = 20
capacity_matrix_np[W2, 10] = 15; capacity_matrix_np[W2, 11] = 10; capacity_matrix_np[W2, 12] = 25
capacity_matrix_np[W3, 13] = 20; capacity_matrix_np[W3, 14] = 15; capacity_matrix_np[W3, 15] = 10
capacity_matrix_np[W4, 16] = 20; capacity_matrix_np[W4, 17] = 10; capacity_matrix_np[W4, 18] = 15; capacity_matrix_np[W4, 19] = 5; capacity_matrix_np[W4, 20] = 10
for i in range(7, 21): capacity_matrix_np[i, T] = INF
capacity_matrix = capacity_matrix_np.tolist() 

# --- EDMONDS-KARP ALGORITHM (Functions remain unchanged) ---
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True
    while queue:
        current_node = queue.popleft()
        for neighbor in range(len(capacity_matrix)):
            residual_capacity = capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor]
            if not visited[neighbor] and residual_capacity > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink: return True
                queue.append(neighbor)
    return False

def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = float('Inf')
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node
        max_flow += path_flow
    return max_flow, flow_matrix

# --- REPORT GENERATION FUNCTION (Translated to English) ---
def generate_report(max_flow_value, flow_matrix):
    report = []
    
    # Data for Question 1 (Terminals)
    terminal_flow_t1 = sum(flow_matrix[T1][w] for w in [W1, W2, W3])
    terminal_flow_t2 = sum(flow_matrix[T2][w] for w in [W2, W3, W4])
    
    # Data for Question 3 (Stores)
    store_flow = {}
    for i in range(7, 21): 
        store_flow[NODE_NAMES[i]] = flow_matrix[i][T]
    sorted_store_flow = sorted(store_flow.items(), key=lambda item: item[1])
    
    # Data for Question 2 & 4 (Bottlenecks)
    bottlenecks = []
    for u in range(NUM_NODES):
        for v in range(NUM_NODES):
            if capacity_matrix[u][v] > 0 and capacity_matrix[u][v] - flow_matrix[u][v] == 0:
                if u not in [S, T] and v not in [S, T] and capacity_matrix[u][v] < INF:
                    bottlenecks.append((NODE_NAMES.get(u), NODE_NAMES.get(v), capacity_matrix[u][v]))
    
    term_to_ware_bottlenecks = [b for b in bottlenecks if b[0].startswith('T') and b[1].startswith('W')]
    store_bottlenecks = [b for b in bottlenecks if b[0].startswith('W') and b[1].startswith('M')]

    # --- REPORT TEXT (ENGLISH) ---
    report.append("="*80)
    report.append(f"| MAXIMUM FLOW ANALYSIS OF LOGISTICS NETWORK (EDMONDS-KARP ALGORITHM) |")
    report.append("="*80)
    report.append(f"| OVERALL MAXIMUM FLOW: {max_flow_value} UNITS |")
    report.append("="*80)
    
    # --- 1. Terminal Flow ---
    report.append("\n## 1. Which terminals provide the greatest flow of goods?")
    report.append(f"-> Terminal 1 (T1) Flow: **{terminal_flow_t1} units** (Potential: {capacity_matrix_np[T1, W1] + capacity_matrix_np[T1, W2] + capacity_matrix_np[T1, W3]} units)")
    report.append(f"-> Terminal 2 (T2) Flow: **{terminal_flow_t2} units** (Potential: {capacity_matrix_np[T2, W2] + capacity_matrix_np[T2, W3] + capacity_matrix_np[T2, W4]} units)")
    report.append("\nCONCLUSION: **Terminal 1** contributes the highest flow. Both terminals are operating at **100% capacity** and are the primary constraint on the network's total throughput.")

    # --- 2 & 4. Bottlenecks and Optimization ---
    report.append("\n" + "-"*80)
    report.append("## 2 & 4. Bottlenecks (Min-Cut) and Optimization Paths")
    report.append(f"The **Minimum Cut** (the network's primary constraint) value is **{max_flow_value} units**.")
    
    report.append("\nA. Primary Bottlenecks (Limiting Overall Flow):")
    report.append("   These are the edges connecting Terminals to Warehouses. Their combined capacity limits the entire network.")
    for u_name, v_name, cap in term_to_ware_bottlenecks:
        report.append(f"      - {u_name} -> {v_name} ({cap} units)")
    
    report.append("\nACTION FOR EFFICIENCY IMPROVEMENT:")
    report.append("   To **increase OVERALL throughput** (>115 units), investment must target the capacity of **these six T -> W edges**. For instance, increasing T2 -> W4 from 30 to 40 would raise the Max Flow to 125 units.")
    
    report.append("\nB. Local Bottlenecks (Limiting Specific Stores):")
    for u_name, v_name, cap in store_bottlenecks:
        report.append(f"      - {u_name} -> {v_name} ({cap} units)")
    
    report.append("\nIMPACT ON OVERALL FLOW: These local constraints **do not affect** the total network capacity of 115, but they limit specific distribution points.")

    # --- 3. Store Supply ---
    report.append("\n" + "-"*80)
    report.append("## 3. Which stores received the least amount of goods?")
    report.append("Stores whose supply is limited by the smallest individual capacities:")
    
    for store, flow in sorted_store_flow:
        if flow <= 15:
            limiting_warehouse = next(u for u in [W1, W2, W3, W4] if capacity_matrix[u][next(i for i, name in NODE_NAMES.items() if name == store)] > 0)
            report.append(f"   - **{store}**: {flow} units (Limited by {NODE_NAMES[limiting_warehouse]} -> {store} with capacity {flow} units)")

    report.append("\nCAN SUPPLY BE INCREASED?: **Yes, locally.** Increasing the W4 -> M13 capacity from 5 to 15 will increase M13's local supply. However, this **will not increase the overall Max Flow of 115**.")
    report.append("="*80)

    return '\n'.join(report)

# --- EXECUTION ---
max_flow_value, flow_matrix = edmonds_karp(capacity_matrix, S, T)
final_report = generate_report(max_flow_value, flow_matrix)

# 1. Print to console (for immediate check)
print(final_report) 

# 2. Save to file (The robust solution for the mentor)
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
REPORT_FILENAME = os.path.join(SCRIPT_DIR, 'task1_analysis_report_EN.txt') 
try:
    with open(REPORT_FILENAME, 'w', encoding='utf-8') as f:
        f.write(final_report)
    print(f"\n Report successfully generated and saved to file: {REPORT_FILENAME}")
except Exception as e:
    # This prints any error during file writing (e.g., permission denied)
    print(f"Error writing file: {e}")