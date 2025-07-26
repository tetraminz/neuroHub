"""CLI entry point for running the P300 pipeline."""

from __future__ import annotations

import click

from neurohub import run_p300_pipeline


@click.command()
@click.option(
    "--data",
    "data_path",
    type=click.Path(exists=True),
    default=None,
    help="Path to raw data",
)
@click.option(
    "--out",
    "out_dir",
    type=click.Path(),
    default="results",
    show_default=True,
    help="Output directory",
)
def main(data_path: str | None, out_dir: str) -> None:
    """Run the full pipeline and print accuracy."""
    acc = run_p300_pipeline(data_path, out_dir)
    click.echo(f"Final accuracy: {acc:.3f}")


if __name__ == "__main__":
    main()
