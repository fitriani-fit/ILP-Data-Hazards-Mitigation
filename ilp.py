# -*- coding: utf-8 -*-
"""
ILP Simulator - Mitigasi Data Hazards (RAW, WAR, & WAW) dengan Visualisasi Grafik
Kolaborasi: Della (RAW), Sinta (WAR), Fitri (WAW & Graph)
"""

from dataclasses import dataclass
import matplotlib.pyplot as plt
import networkx as nx


@dataclass
class Instruction:
    name: str
    destination: str
    sources: list


# -------------------------------------------------
# Sample Instruction Set
# -------------------------------------------------

instructions = [
    Instruction("I1", "R1", ["R2", "R3"]),
    Instruction("I2", "R4", ["R5", "R6"]),
    Instruction("I3", "R7", ["R1", "R4"]),
    Instruction("I4", "R8", ["R9", "R10"]),
    Instruction("I5", "R11", ["R7", "R8"]),
    Instruction("I6", "R12", ["R13", "R14"]),
]


# -------------------------------------------------
# Functions to check Data Hazards (RAW, WAR, WAW)
# -------------------------------------------------

def check_raw(inst1, inst2):
    return inst1.destination != "" and inst1.destination in inst2.sources

def check_war(inst1, inst2):
    return inst2.destination != "" and inst2.destination in inst1.sources

def check_waw(inst1, inst2):
    return inst1.destination != "" and inst2.destination != "" and inst1.destination == inst2.destination

def has_dependency(inst1, inst2):
    return check_raw(inst1, inst2) or check_war(inst1, inst2) or check_waw(inst1, inst2)


# -------------------------------------------------
# Dependency Analysis (Text Output)
# -------------------------------------------------

def show_dependencies(instructions):
    print("\n" + "=" * 50)
    print("DEPENDENCY ANALYSIS (RAW, WAR, WAW)")
    print("=" * 50)

    found = False

    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            i1, i2 = instructions[i], instructions[j]
            hazards = []

            if check_raw(i1, i2):
                hazards.append(f"RAW({i1.destination})")
            if check_war(i1, i2):
                hazards.append(f"WAR({i2.destination})")
            if check_waw(i1, i2):
                hazards.append(f"WAW({i1.destination})")

            if hazards:
                hazard_label = ", ".join(hazards)
                print(f"{i2.name} depends on {i1.name} [{hazard_label}]")
                found = True

    if not found:
        print("No dependencies found.")


# -------------------------------------------------
# Visualisasi Dependency Graph (NetworkX & Matplotlib)
# -------------------------------------------------

def plot_dependency_graph(instructions):
    """
    Membuat visualisasi Dependency Graph menggunakan NetworkX dan Matplotlib
    """
    G = nx.DiGraph()
    
    # 1. Tambahkan setiap instruksi sebagai node
    for inst in instructions:
        G.add_node(inst.name)
        
    # 2. Cek relasi hazard antar instruksi dan tambahkan sebagai edge (panah)
    for i in range(len(instructions)):
        for j in range(i + 1, len(instructions)):
            inst1 = instructions[i]
            inst2 = instructions[j]
            
            hazards = []
            if check_raw(inst1, inst2):
                hazards.append("RAW")
            if check_war(inst1, inst2):
                hazards.append("WAR")
            if check_waw(inst1, inst2):
                hazards.append("WAW")
                
            if hazards:
                # Jika ada hazard, buat panah dari inst1 ke inst2 dengan label jenis hazardnya
                hazard_label = "/".join(hazards)
                G.add_edge(inst1.name, inst2.name, label=hazard_label)

    # 3. Pengaturan Tampilan Grafik
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42) # Mengatur posisi node agar rapi
    
    # Gambar node, edge, dan teks label
    nx.draw_networkx_nodes(G, pos, node_color='#a1c4fd', node_size=2200)
    nx.draw_networkx_edges(G, pos, arrowsize=20, edge_color='#555555', width=2)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Menampilkan label jenis hazard (RAW/WAR/WAW) di atas garis panah
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_weight='bold')
    
    plt.title('Instruction Dependency Graph (ILP Hazards)', fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    print("\n[INFO] Membuka jendela visualisasi Dependency Graph...")
    plt.show()


# -------------------------------------------------
# Sequential Execution
# -------------------------------------------------

def sequential_execution(instructions):
    print("\n" + "=" * 50)
    print("SEQUENTIAL EXECUTION")
    print("=" * 50)

    cycle = 0
    for instruction in instructions:
        cycle += 1
        print(f"Cycle {cycle}: Executing {instruction.name} ({instruction.destination} = {' + '.join(instruction.sources)})")

    print(f"\nTotal Sequential Cycles: {cycle}")
    return cycle


# -------------------------------------------------
# ILP / Parallel Execution
# -------------------------------------------------

def parallel_execution(instructions):
    print("\n" + "=" * 50)
    print("INSTRUCTION-LEVEL PARALLEL EXECUTION")
    print("=" * 50)

    completed = set()
    remaining = instructions.copy()
    cycle = 0

    while remaining:
        cycle += 1
        current_cycle = []

        for instruction in remaining:
            dependencies_satisfied = True
            for previous in instructions:
                if previous.name == instruction.name:
                    break
                if has_dependency(previous, instruction):
                    if previous.name not in completed:
                        dependencies_satisfied = False
                        break

            if dependencies_satisfied:
                current_cycle.append(instruction)

        print(f"\nCycle {cycle}:")
        for instruction in current_cycle:
            print(f"    -> {instruction.name}: {instruction.destination} = {' + '.join(instruction.sources)}")

        for instruction in current_cycle:
            completed.add(instruction.name)
            remaining.remove(instruction)

    print(f"\nTotal ILP Cycles: {cycle}")
    return cycle


# -------------------------------------------------
# Main Program
# -------------------------------------------------

def main():
    print("\n")
    print("*" * 60)
    print("      INSTRUCTION-LEVEL PARALLELISM SIMULATOR")
    print("*" * 60)

    print("\nInstruction Set:")
    for instruction in instructions:
        print(f"{instruction.name}: {instruction.destination} = {' + '.join(instruction.sources)}")

    # Show dependencies text analysis
    show_dependencies(instructions)

    # Sequential execution
    sequential_cycles = sequential_execution(instructions)

    # Parallel execution
    parallel_cycles = parallel_execution(instructions)

    # Calculate speedup
    speedup = sequential_cycles / parallel_cycles
    efficiency = (speedup / len(instructions)) * 100

    print("\n" + "=" * 50)
    print("PERFORMANCE COMPARISON")
    print("=" * 50)

    print(f"Sequential Cycles : {sequential_cycles}")
    print(f"ILP Cycles        : {parallel_cycles}")
    print(f"Speedup           : {speedup:.2f}x")
    print(f"ILP Efficiency    : {efficiency:.2f}%")

    print("\nConclusion:")
    print("ILP reduces execution cycles by allowing independent instructions to execute in parallel.")

    # Render dan tampilkan grafik visual Dependency Graph
    plot_dependency_graph(instructions)


if __name__ == "__main__":
    main()
