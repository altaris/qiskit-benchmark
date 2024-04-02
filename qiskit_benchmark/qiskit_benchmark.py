"""Main module"""

from datetime import datetime, timedelta
from itertools import product
from pathlib import Path
from typing import Any

import pandas as pd
import qiskit
import seaborn as sns
import turbo_broccoli as tb
from matplotlib.axes import Axes
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
    guard = tb.GuardedBlockHandler(
        output_file, artifact_path=output_file.parent / "data"
    )
    simulator = AerSimulator(method=method, device=device)
    for _, (n_qbits, depth, n) in guard(progress, result_type="list"):
        progress.set_postfix({"n_qbits": n_qbits, "depth": depth, "n": n})
        circuit = random_circuit(
            num_qubits=n_qbits, depth=depth, measure=True, conditional=True
        )
        start = datetime.now()
        circuit = qiskit.transpile(circuit, simulator)
        result = simulator.run(circuit, shots=n_shots).result()
        time_taken = (datetime.now() - start) / timedelta(seconds=1)
        guard.result.append(
            tb.EmbeddedDict(
                {
                    "circuit": qasm3.dumps(circuit),
                    "depth": depth,
                    "device": device,
                    "method": method,
                    "n_qbits": n_qbits,
                    "n_shots": n_shots,
                    "results": result.to_dict(),
                    "time_taken": time_taken,
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
            ]
        )
        for r in tqdm(results, desc="Post-processing"):
            df.loc[len(df)] = {k: r[k] for k in df.columns}
        guard.result = df
    return guard.result


def plot_results(df: pd.DataFrame, output_file: Path) -> Axes:
    """
    Plots the results. This method is guarded.

    Args:
        df (pd.DataFrame):
    """
    df = df.groupby(["n_qbits", "depth"]).mean().reset_index()
    df = df.pivot(index="n_qbits", columns="depth", values="time_taken")
    plot = sns.heatmap(df, annot=True, fmt=".2f")
    plot.set(title="Execution time (s)")
    plot.get_figure().savefig(str(output_file))
    return plot
