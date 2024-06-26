"""CLI module"""

# pylint: disable=import-outside-toplevel

import os
from pathlib import Path

import click
from loguru import logger as logging

from .logging import setup_logging


@click.command()
@click.option(
    "--logging-level",
    default=os.getenv("LOGGING_LEVEL", "info"),
    help=(
        "Logging level, case insensitive. Defaults to 'info'. Can also be set "
        "using the LOGGING_LEVEL environment variable."
    ),
    type=click.Choice(
        ["critical", "debug", "error", "info", "warning"],
        case_sensitive=False,
    ),
)
@click.option(
    "-mq",
    "--min-qbits",
    default=1,
    help="Minimum number of qubits. Defaults to 1.",
    type=int,
)
@click.option(
    "-Mq",
    "--max-qbits",
    default=10,
    help="Maximum number of qubits. Defaults to 10.",
    type=int,
)
@click.option(
    "-md",
    "--min-depth",
    default=1,
    help="Minimum circuit depth. Defaults to 1.",
    type=int,
)
@click.option(
    "-Md",
    "--max-depth",
    default=10,
    help="Maximum circuit depth. Defaults to 10.",
    type=int,
)
@click.option(
    "-ns",
    "--n-shots",
    default=100,
    help="Number of times a given circuit is to be run. Defaults to 100.",
    type=int,
)
@click.option(
    "-nc",
    "--n-circuits",
    default=10,
    help=(
        "Number of circuits to generate for a given number of qubits and "
        "depth. Defaults to 10."
    ),
    type=int,
)
@click.option(
    "-m",
    "--method",
    default="statevector",
    help=(
        "Simulator method, see "
        "https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html"
        " . Defaults to 'statevector'."
    ),
    type=click.Choice(
        [
            "automatic",
            "statevector",
            "density_matrix",
            "stabilizer",
            "matrix_product_state",
            "extended_stabilizer",
            "unitary",
            "superop",
            "tensor_network",
        ],
    ),
)
@click.option(
    "-d",
    "--device",
    default="CPU",
    help="Device to use for simulation. Defaults to 'CPU'.",
    type=str,
)
@click.argument(
    "OUTPUT_DIR",
    type=click.Path(  # type: ignore
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@logging.catch
def main(
    output_dir: Path,
    logging_level: str,
    min_qbits: int,
    max_qbits: int,
    min_depth: int,
    max_depth: int,
    n_shots: int,
    n_circuits: int,
    method: str,
    device: str,
):
    """Simple qiskit benchmarking utility"""
    from .qiskit_benchmark import (
        generate_random_circuits,
        make_result_dataframe,
        plot_results,
        run,
    )

    setup_logging(logging_level)

    logging.info("Generating circuits")
    (output_dir / "circuits").mkdir(parents=True, exist_ok=True)
    generate_random_circuits(
        output_dir=output_dir / "circuits",
        qbits_range=(min_qbits, max_qbits),
        depth_range=(min_depth, max_depth),
        n_circuits=n_circuits,
    )

    logging.info("Running circuits")
    (output_dir / "data").mkdir(parents=True, exist_ok=True)
    results = run(
        output_file=output_dir / "data" / "results.json",
        circuits_dir=output_dir / "circuits",
        qbits_range=(min_qbits, max_qbits),
        depth_range=(min_depth, max_depth),
        n_shots=n_shots,
        n_circuits=n_circuits,
        method=method,
        device=device,
    )

    logging.info("Post-processing & plotting")
    df = make_result_dataframe(results)
    df.to_csv(output_dir / "results.csv", index=False)
    plot_results(df, output_dir)


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
