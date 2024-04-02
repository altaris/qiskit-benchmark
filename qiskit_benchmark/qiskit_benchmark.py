"""Main module"""

from itertools import product
from pathlib import Path
from typing import Any

import pandas as pd
import qiskit
import turbo_broccoli as tb
from qiskit import qasm3
from qiskit.circuit.random import random_circuit
from qiskit_aer import AerSimulator
from tqdm import tqdm


# pylint: disable=too-many-locals
def run(
    output_file: Path,
    qbits_range: tuple[int, int],
    depth_range: tuple[int, int],
    n_shots: int,
    n_circuits: int,
    method: str,
    device: str,
) -> list[dict[str, Any]]:
    """
    Runs the benchmark. Each iteration is guarded.

    Args:
        output_file (Path): Output JSON file path
        qbits_range (tuple[int, int]):
        depth_range (tuple[int, int]):
        n_shots (int):
        n_circuits (int):
        method (str):
        device (str):

    Returns:
        `list[dict[str, Any]]`
    """
    everything = list(
        product(
            range(qbits_range[0], qbits_range[1] + 1),
            range(depth_range[0], depth_range[1] + 1),
            range(1, n_circuits + 1),
        )
    )
    progress = tqdm(everything, desc="Benchmarking", total=len(everything))
    guard = tb.GuardedBlockHandler(output_file)
    simulator = AerSimulator(method=method, device=device)
    for _, (n_qbits, depth, n) in guard(progress, result_type="list"):
        progress.set_postfix({"n_qbits": n_qbits, "depth": depth, "n": n})
        circuit = random_circuit(
            num_qubits=n_qbits, depth=depth, measure=True, conditional=True
        )
        circuit = qiskit.transpile(circuit, simulator)
        result = simulator.run(circuit, shots=n_shots).result()
        guard.result.append(
            tb.EmbeddedDict(
                {
                    "n_qbits": n_qbits,
                    "depth": depth,
                    "time_taken": result.time_taken,
                    "max_memory_mb": result.metadata["max_memory_mb"],
                    "max_gpu_memory_mb": result.metadata["max_gpu_memory_mb"],
                    "circuit": qasm3.dumps(circuit),
                    "results": result.to_dict(),
                }
            )
        )
    return guard.result


def make_result_dataframe(
    output_file: Path, results: list[dict[str, Any]]
) -> pd.DataFrame:
    """
    Makes a dataframe out of the results provided by `run`. This method is
    guarded.

    Args:
        output_file (Path): Output CSV file path
        results (list[dict[str, Any]]):

    Returns:
        Pandas dataframe
    """
    guard = tb.GuardedBlockHandler(output_file)
    for _ in guard:
        df = pd.DataFrame(
            columns=[
                "n_qbits",
                "depth",
                "time_taken",
                "max_memory_mb",
                "max_gpu_memory_mb",
            ]
        )
        for r in tqdm(results, desc="Post-processing"):
            df.iloc[len(df)] = {k: r[k] for k in df.columns}
        guard.result = df
    return guard.result
