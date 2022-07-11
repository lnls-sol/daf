#!/usr/bin/env python3

import os
from os import path

import argparse as ap
import numpy as np
import yaml

from daf.utils.log import daf_log
from daf.utils import dafutilities as du
from daf.utils import daf_paths as dp
from daf.command_line.experiment.experiment_utils import ExperimentBase


class ManageCounters(ExperimentBase):
    DESC = """Manage counter configuration files"""

    EPI = """
    Eg:
       daf.mc -s default
       daf.mc -n new_config
       daf.mc -lc new_config
       daf.mc -r my_setup1 my_setup2 my_setup3
       daf.mc -rc new_config counter1 
        """

    YAML_PREFIX = "config."
    YAML_SUFIX = ".yml"


    def __init__(self):
        super().__init__()
        self.parsed_args = self.parse_command_line()
        self.parsed_args_dict = vars(self.parsed_args)

    def parse_command_line(self):
        super().parse_command_line()
        self.parser.add_argument(
            "-s",
            "--set_default",
            metavar="config name",
            type=str,
            help="Set default counter file to be used in scans",
        )
        self.parser.add_argument(
            "-n", "--new", metavar="config name", type=str, help="Create a new setup"
        )
        self.parser.add_argument("-r", "--remove", metavar="file", nargs="*", help="Remove a setup")
        self.parser.add_argument(
            "-a",
            "--add_counter",
            metavar="counter",
            nargs="*",
            help="Add a counter to a config file",
        )
        self.parser.add_argument(
            "-rc",
            "--remove_counter",
            metavar="file",
            nargs="*",
            help="Remove counters from a config file",
        )
        self.parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            help="List all setups, showing in which one you are",
        )
        self.parser.add_argument(
            "-lc",
            "--list_counters",
            metavar="file",
            nargs="*",
            help="List counters in a specific file, more than one file can be passed",
        )
        self.parser.add_argument(
            "-lac",
            "--list_all_counters",
            action="store_true",
            help="List all counters available",
        )
        self.parser.add_argument(
            "-m",
            "--main-counter",
            metavar="counter",
            type=str,
            help="Set the main counter during a scan",
        )
        args = self.parser.parse_args()
        return args

    @staticmethod
    def read_yaml(file_path: str):
        with open(file_path) as file:
            data = yaml.safe_load(file)
            return data

    @staticmethod
    def write_yaml(list_: list, file_path: str):
        with open(file_path, "w") as file:
            yaml.dump(list_, file)

    def get_full_file_path(self, file_name: str) -> str:
        """Get full file path of a config file and return it"""
        yaml_file_name = self.YAML_PREFIX + file_name + self.YAML_SUFIX
        user_configs = os.listdir(dp.SCAN_UTILS_USER_PATH)
        sys_configs = os.listdir(dp.SCAN_UTILS_SYS_PATH)
        if yaml_file_name in user_configs:
            path_to_use = dp.SCAN_UTILS_USER_PATH
        elif yaml_file_name in sys_configs:
            path_to_use = dp.SCAN_UTILS_SYS_PATH
        full_file_path = path.join(path_to_use, yaml_file_name)
        return full_file_path

    @staticmethod
    def list_configuration_files():
        """List all configuration files, both user and system configuration."""
        user_configs = os.listdir(dp.SCAN_UTILS_USER_PATH)
        sys_configs = os.listdir(dp.SCAN_UTILS_SYS_PATH)
        all_configs = user_configs + sys_configs
        configs = [i for i in all_configs if len(i.split(".")) == 3 and i.endswith(".yml")]
        configs.sort()
        for i in configs:
            print(i.split(".")[1])

    @staticmethod
    def list_all_counters():
        """List all available counters for the current beamline"""
        with open(dp.DEFAULT_SCAN_UTILS_CONFIG) as conf:
            config_data = yaml.safe_load(conf)
        counters = config_data["counters"].keys()
        for i in counters:
            print(i)

    def set_default_counters(self, default_counter: str):
        """Set the file that should be used in the further scans"""
        self.experiment_file_dict["default_counters"] = self.YAML_PREFIX + default_counter + self.YAML_SUFIX
        du.write(self.experiment_file_dict)

    def create_new_configuration_file(self, file_name: str):
        """Create a new empty configuration counter file, counters should be added in advance."""
        yaml_file_name = self.YAML_PREFIX + file_name + self.YAML_SUFIX
        full_file_path = path.join(dp.SCAN_UTILS_USER_PATH, yaml_file_name)
        self.write_yaml([], full_file_path)

    def list_counter_in_a_configuration_file(self, file_name):
        """List all counters in a configuration file"""
        full_file_path = self.get_full_file_path(file_name)
        data = self.read_yaml(full_file_path)
        print("Counters in: {}".format(file_name))
        for counter in data:
            print(counter)

    def add_counters_to_a_file(self, file_name, counters):
        """Add counters to a config file"""
        full_file_path = self.get_full_file_path(file_name)
        data = self.read_yaml(full_file_path)
        if isinstance(data, list):
            for counter in counters:
                if counter not in data:
                    data.append(counter)
            self.write_yaml(data, full_file_path)
        else:
            list_ = []
            for counter in counters:
                if counter not in list_:
                    list_.append(counter)
            self.write_yaml(list_, full_file_path)

    def run_cmd(self, arguments: dict) -> None:
        """Method to be defined be each subclass, this is the method
        that should be run when calling the cli interface"""
        if arguments["list"]:
            self.list_configuration_files()

        if arguments["list_all_counters"]:
            self.list_all_counters()

        if arguments["set_default"]:
            self.set_default_counters(arguments["set_default"])

        if arguments["new"]:
            self.create_new_configuration_file(arguments["new"])

        if isinstance(arguments["list_counters"], list):
            for file in arguments["list_counters"]:
                self.list_counter_in_a_configuration_file(file)

        if arguments["add_counter"]:
            self.add_counters_to_a_file(arguments["add_counter"][0], arguments["add_counter"][1:])

        # if args.remove_counter:
        #     file_name = args.remove_counter[0]
        #     complete_file = prefix + file_name + sufix
        #     user_configs = os.listdir(path)
        #     sys_configs = os.listdir(sys_path)
        #     if complete_file in user_configs:
        #         path_to_use = path
        #     elif complete_file in sys_configs:
        #         path_to_use = sys_path

        #     data = read_yaml(filepath=path_to_use + complete_file)

        #     if isinstance(data, list):
        #         for counter in args.remove_counter[1:]:
        #             if counter in data:
        #                 data.remove(counter)

        #     write_yaml(data, filepath=path_to_use + complete_file)

        # if args.main_counter:
        #     dict_args["main_scan_counter"] = args.main_counter
        #     du.write(dict_args)


        # if args.remove:
        #     for file in args.remove:
        #         complete_file = prefix + file + sufix
        #         user_configs = os.listdir(path)
        #         sys_configs = os.listdir(sys_path)
        #         if complete_file in user_configs:
        #             path_to_use = path
        #         elif complete_file in sys_configs:
        #             path_to_use = sys_path
        #         os.system('rm -f "{}"'.format(path_to_use + complete_file))

@daf_log
def main() -> None:
    obj = ManageCounters()
    obj.run_cmd(obj.parsed_args_dict)


if __name__ == "__main__":
    main()







