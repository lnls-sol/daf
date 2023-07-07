#!/usr/bin/env python3

import numpy as np
import pandas as pd

from daf.utils.decorators import cli_decorator
from daf.command_line.cli_base_utils import CLIBase
from daf.command_line.scan.daf_scan_utils import ScanBase


class FromFileScan(ScanBase):

    DESC = """Perform a scan from a csv file generated by daf.scan"""
    EPI = """
    Eg:
        daf.ffscan my_scan -t 0.01

        """

    def __init__(self):
        super().__init__(scan_type="list_scan")
        self.exp = self.build_exp()

    def parse_command_line(self):
        CLIBase.parse_command_line(self)
        self.parser.add_argument(
            "file_name",
            type=str,
            help="Perform a scan from the file generated by daf.scan",
        )
        self.common_cli_scan_arguments(step=False)
        args = self.parser.parse_args()
        return args

    def generate_data_for_scan(self, full_file_path: str) -> np.array:
        """Generate the scan path for scans"""
        scan_points = pd.read_csv(full_file_path)
        mu_points = [
            float(i) for i in scan_points["Mu"]
        ]  # Get only the points related to mu
        eta_points = [
            float(i) for i in scan_points["Eta"]
        ]  # Get only the points related to eta
        chi_points = [
            float(i) for i in scan_points["Chi"]
        ]  # Get only the points related to chi
        phi_points = [
            float(i) for i in scan_points["Phi"]
        ]  # Get only the points related to phi
        nu_points = [
            float(i) for i in scan_points["Nu"]
        ]  # Get only the points related to nu
        del_points = [
            float(i) for i in scan_points["Del"]
        ]  # Get only the points related to del

        data_for_scan = {
            "mu": [mu_points],
            "eta": [eta_points],
            "chi": [chi_points],
            "phi": [phi_points],
            "nu": [nu_points],
            "del": [del_points],
        }
        ordered_motors = [i for i in data_for_scan.keys()]

        return data_for_scan, ordered_motors

    def configure_scan_input(self):
        """Basically, a wrapper for configure_scan_inputs. It may differ from scan to scan"""
        data_for_scan, ordered_motors = self.generate_data_for_scan(
            self.parsed_args_dict["file_name"]
        )
        inputed_motors = [i for i in data_for_scan.keys()]
        return {
            "scan_data": data_for_scan,
            "inputed_motors": inputed_motors,
            "motors_data_dict": self.experiment_file_dict["motors"],
            "counters": self.get_counters(),
            "scan_type": self.scan_type,
            "steps": None,
            "acquisition_time": self.parsed_args_dict["time"],
            "output": self.parsed_args_dict["output"],
        }

    def run_cmd(self):
        """
        Method to be defined be each subclass, this is the method
        that should be run when calling the cli interface
        """
        self.run_scan()


@cli_decorator
def main() -> None:
    obj = FromFileScan()
    obj.run_cmd()


if __name__ == "__main__":
    main()