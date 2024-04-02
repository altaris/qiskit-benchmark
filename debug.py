"""Debugging entrypoint"""

if __name__ == "__main__":
    from qiskit_benchmark.__main__ import main

    # CLI args and options as a list of str
    main(["--logging-level", "debug"])
