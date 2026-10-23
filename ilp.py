# -*- coding: utf-8 -*-
"""
ILP Simulator - Mitigasi Data Hazards (RAW, WAR, & WAW)
Kolaborasi: Della (RAW), Sinta (WAR), Fitri (WAW & Graph)
"""

from dataclasses import dataclass


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
    """RAW (Read-After-Write): inst2 membaca register yang ditulis oleh inst1"""
    return inst1.destination != "" and inst1.destination in inst2.sources


def check_war(inst1, inst2):
    """WAR (Write-After-Read): inst2 menulis ke register yang dibaca oleh inst1"""
    return inst2.destination != "" and inst2.destination in inst1.sources


def check_waw(inst1, inst2):
    """WAW (Write-After-Write): inst2 menulis ke register yang sama dengan tulisan inst1"""
    return inst1.destination != "" and inst2.destination != "" and inst1.destination == inst2.destination


def has_dependency(inst1, inst2):
    """Mengembalikan True jika terdapat dependensi RAW, WAR, atau WAW"""
    return check_raw(inst1, inst2) or check_war(inst1, inst2) or check_waw(inst1, inst2)


# -------------------------------------------------
# Dependency Analysis & Graph Logic
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
                hazards.append(f"RAW (Reg: {i1.destination})")
            if check_war(i1, i2):
                hazards.append(f"WAR (Reg: {i2.destination})")
            if check_waw(i1, i2):
                hazards.append(f"WAW (Reg: {i1.destination})")

            if hazards:
                print(
                    f"{i2.name} depends on {i1.name} "
                    f"[{', '.join(hazards)}]"
                )
                found = True

    if not found:
        print("No dependencies found.")


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
        print(
            f"Cycle {cycle}: Executing {instruction.name} "
            f"({instruction.destination} = "
            f"{' + '.join(instruction.sources)})"
        )

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
            print(
                f"  -> {instruction.name}: "
                f"{instruction.destination} = "
                f"{' + '.join(instruction.sources)}"
            )

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
        print(
            f"{instruction.name}: "
            f"{instruction.destination} = "
            f"{' + '.join(instruction.sources)}"
        )

    # Show dependencies
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
    print(
        "ILP reduces execution cycles by allowing "
        "independent instructions to execute in parallel."
    )


# -------------------------------------------------
# Run Program
# -------------------------------------------------

if __name__ == "__main__":
    main()
