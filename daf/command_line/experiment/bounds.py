#!/usr/bin/env python3

from daf.utils.log import daf_log
from daf.command_line.experiment.experiment_utils import ExperimentBase


class Bounds(ExperimentBase):
    DESC = """Sets the bounds of the diffractometer angles"""
    EPI = """
    Eg:
        daf.bounds -m -180 180 -n -180 180
        """

    DEFAULT_BOUNDS = {
        "mu": [-20.0, 160.0],
        "eta": [-20.0, 160.0],
        "chi": [-5.0, 95.0],
        "phi": [-400.0, 400.0],
        "nu": [-20.0, 160.0],
        "del": [-20.0, 160.0],
    }

    def __init__(self):
        super().__init__()
        self.parsed_args = self.parse_command_line()
        self.parsed_args_dict = vars(self.parsed_args)

    def parse_command_line(self):
        super().parse_command_line()
        self.parser.add_argument(
            "-m",
            "--mu",
            metavar=("min", "max"),
            type=float,
            nargs=2,
            help="Sets Mu bounds",
        )
        self.parser.add_argument(
            "-e",
            "--eta",
            metavar=("min", "max"),
            type=float,
            nargs=2,
            help="Sets Eta bounds",
        )
        self.parser.add_argument(
            "-c",
            "--chi",
            metavar=("min", "max"),
            type=float,
            nargs=2,
            help="Sets Chi bounds",
        )
        self.parser.add_argument(
            "-p",
            "--phi",
            metavar=("min", "max"),
            type=float,
            nargs=2,
            help="Sets Phi bounds",
        )
        self.parser.add_argument(
            "-n",
            "--nu",
            metavar=("min", "max"),
            type=float,
            nargs=2,
            help="Sets Nu bounds",
        )
        self.parser.add_argument(
            "-d",
            "--del",
            metavar=("min", "max"),
            type=float,
            nargs=2,
            help="Sets Del bounds",
        )
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List the current bounds"
        )
        self.parser.add_argument(
            "-r", "--reset", action="store_true", help="Reset all bounds to default"
        )

        args = self.parser.parse_args()
        return args

    def reset_bounds_to_default(self) -> None:
        """Reset all motor bounds to default. It writes directly to the .Experiment file"""
        self.write_to_experiment_file(self.DEFAULT_BOUNDS)

    def list_bounds(self) -> None:
        """Method to print the current bounds"""
        print("")
        print(
            "Mu    =    {}".format(self.experiment_file_dict["motors"]["mu"]["bounds"])
        )
        print(
            "Eta   =    {}".format(self.experiment_file_dict["motors"]["eta"]["bounds"])
        )
        print(
            "Chi   =    {}".format(self.experiment_file_dict["motors"]["chi"]["bounds"])
        )
        print(
            "Phi   =    {}".format(self.experiment_file_dict["motors"]["phi"]["bounds"])
        )
        print(
            "Nu    =    {}".format(self.experiment_file_dict["motors"]["nu"]["bounds"])
        )
        print(
            "Del   =    {}".format(self.experiment_file_dict["motors"]["del"]["bounds"])
        )
        print("")

    def check_if_bounds_bounds_should_be_written(self):
        """method to tell whether or not new bounds should be written, saving useless I/Os"""
        for value in self.parsed_args_dict.values():
            if value != None:
                self.write_flag = True

    def run_cmd(self) -> None:
        """Method to be defined be each subclass, this is the method
        that should be run when calling the cli interface"""
        self.check_if_bounds_bounds_should_be_written()
        if self.write_flag:
            self.write_to_experiment_file(self.parsed_args_dict)
        if self.parsed_args_dict["reset"]:
            self.reset_bounds_to_default()
        if self.parsed_args_dict["list"]:
            self.list_bounds()


@daf_log
def main() -> None:
    obj = Bounds()
    obj.run_cmd()


if __name__ == "__main__":
    main()
