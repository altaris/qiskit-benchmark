"""CLI module"""

import os
from pathlib import Path

import click
from loguru import logger as logging

from .logging import setup_logging


@click.command()
@click.option(
    "--logging-level",
    default=os.getenv("LOGGING_LEVEL", "info"),
    help=("Logging level, case insensitive"),
    type=click.Choice(
        ["critical", "debug", "error", "info", "warning"],
        case_sensitive=False,
    ),
)
@click.option(
    "-mq",
    "--min-qbits",
    default=1,
    help="Minimum number of qubits",
    type=int,
)
@click.option(
    "-Mq",
    "--max-qbits",
    default=10,
    help="Maximum number of qubits",
    type=int,
)
@click.option(
    "-md",
    "--min-depth",
    default=1,
    help="Minimum circuit depth",
    type=int,
)
@click.option(
    "-Md",
    "--max-depth",
    default=10,
    help="Maximum circuit depth",
    type=int,
)
@click.option(
    "-ns",
    "--n-shots",
    default=100,
    help="Maximum circuit depth",
    type=int,
)
@click.option(
    "-nc",
    "--n-circuits",
    default=10,
    help="Number of circuits to generate for a given number of qubits and depth",
    type=int,
)
@click.option(
    "-m",
    "--method",
    default="statevector",
    help=(
        "Simulator method, see "
        "https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html"
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
    help="Device to use for simulation",
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
    """Entrypoint"""
    # pylint: disable=import-outside-toplevel
    from .qiskit_benchmark import make_result_dataframe, plot_results, run

    setup_logging(logging_level)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    results = run(
        output_file=output_dir / "data" / "results.json",
        qbits_range=(min_qbits, max_qbits),
        depth_range=(min_depth, max_depth),
        n_shots=n_shots,
        n_circuits=n_circuits,
        method=method,
        device=device,
    )
    df = make_result_dataframe(results)
    df.to_csv(output_dir / "results.csv", index=False)
    plot_results(df, output_dir / "execution_time.png")


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
