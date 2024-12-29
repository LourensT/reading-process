import argparse
import os

from .plotter import Plotter


def save_plot(figure, output_dir, filename):
    figure.savefig(os.path.join(output_dir, filename))
    print(f"Figure saved as '{filename}'")


def main():
    parser = argparse.ArgumentParser(description="Reading Process CLI")

    parser.add_argument("input_dir", type=str, help="Path to the input directory.")
    parser.add_argument("output_dir", type=str, help="Path to the output directory.")

    parser.add_argument(
        "--grouped",
        action="store_true",
        help="Figures comparing logs in subdirectories of input_dir",
    )

    parser.add_argument(
        "--period_name",
        type=str,
        help="Optional name for the processing period (e.g., 'Q1', '2024', etc.).",
    )

    args = parser.parse_args()

    # Ensure input_dir exists
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        exit(1)

    # Ensure output_dir exists or create it
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Output directory '{args.output_dir}' created.")

    # If no period name, set it to the input directory name
    if args.period_name is None:
        args.period_name = os.path.basename(args.input_dir)

    if args.grouped:
        print("creating grouped-by figure")
        raise NotImplementedError
    else:
        # load data
        plotter = Plotter(args.input_dir, args.period_name)
        # timeline
        timeline_figure = plotter.plot_timeline()
        save_plot(timeline_figure, args.output_dir, "timeline.png")

        # trajectories
        trajectories_figure = plotter.plot_trajectories()
        save_plot(trajectories_figure, args.output_dir, "trajectories.png")

        # average trajectories
        average_trajectories_figure = plotter.plot_average_trajectories()
        save_plot(
            average_trajectories_figure, args.output_dir, "average_trajectories.png"
        )

        print(f"Processing files from '{args.input_dir}' to '{args.output_dir}'")


if __name__ == "__main__":
    main()
