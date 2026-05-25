import networkx as nx
import time
import urllib.request
import os
import gzip

# ==========================================
# 1. 資料集下載與載入
# ==========================================
url = "https://snap.stanford.edu/data/facebook_combined.txt.gz"
file_name = "facebook_combined.txt.gz"

if not os.path.exists(file_name):
    print("下載 SNAP Facebook 資料集中...")
    urllib.request.urlretrieve(url, file_name)

print("載入圖形資料...")
# SNAP 資料集格式為邊列表 (Edge list)，以空白分隔
with gzip.open(file_name, 'rt') as f:
    G = nx.read_edgelist(f, create_using=nx.Graph(), nodetype=int)

# ==========================================
# 2. 圖形基本統計資訊 (|V|, |E|, 平均 Degree)
# ==========================================
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
# 總 degree 除以節點數
avg_degree = sum(dict(G.degree()).values()) / num_nodes

print("-" * 40)
print(f"圖形基本資訊:")
print(f"節點數 |V|: {num_nodes}")
print(f"邊數   |E|: {num_edges}")
print(f"平均 Degree: {avg_degree:.2f}")
print("-" * 40)

# ==========================================
# 3. 執行 BFS 與 DFS 並量測時間
# ==========================================
# 隨機選擇第一個節點作為走訪起點
start_node = list(G.nodes())[0]

print(f"以節點 {start_node} 為起點開始走訪...")

# --- 量測 BFS ---
start_time_bfs = time.perf_counter()
# 使用 list() 強制消耗掉 generator，確保整個圖都被走訪完畢
list(nx.bfs_edges(G, source=start_node))
end_time_bfs = time.perf_counter()
bfs_duration = end_time_bfs - start_time_bfs

# --- 量測 DFS ---
start_time_dfs = time.perf_counter()
list(nx.dfs_edges(G, source=start_node))
end_time_dfs = time.perf_counter()
dfs_duration = end_time_dfs - start_time_dfs

# ==========================================
# 4. 輸出結果與時間差
# ==========================================
print(f"BFS 執行時間: {bfs_duration:.6f} 秒")
print(f"DFS 執行時間: {dfs_duration:.6f} 秒")
print("-" * 40)
print(f"時間差 (DFS時間 - BFS時間): {dfs_duration - bfs_duration:.6f} 秒")
print(f"效能比較: {'BFS' if bfs_duration < dfs_duration else 'DFS'} 較快")