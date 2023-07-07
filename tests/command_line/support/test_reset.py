import os
import sys

import pytest
import unittest
from unittest.mock import patch

import daf.utils.dafutilities as du
from daf.command_line.support.reset import Reset, main
import daf.utils.generate_daf_default as gdd
from daf.command_line.support.init import Init


class TestDAF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_sim = Init.build_current_file(Init, True)
        data_sim["simulated"] = True
        data_sim["PV_energy"] = 1
        gdd.generate_file(data=data_sim, file_name=".Experiment")

    @classmethod
    def tearDownClass(cls):
        os.remove(".Experiment")
        os.remove("Log")

    @staticmethod
    def make_obj(command_line_args: list) -> Reset:
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init"]
        for arg in command_line_args:
            testargs.append(arg)
        with patch.object(sys, "argv", testargs):
            obj = Reset()
        return obj

    def test_GIVEN_cli_argument_WHEN_inputing_hard_option_THEN_check_parsed_args(self):
        obj = self.make_obj(["--hard"])
        assert obj.parsed_args_dict["hard"] == True

    def test_GIVEN_cli_argument_WHEN_inputing_all_THEN_check_if_it_was_written_correctly(
        self,
    ):
        obj = self.make_obj([])
        obj.experiment_file_dict["Mode"] = "2023"
        obj.write_to_experiment_file({})
        dict_now = obj.io.read()
        assert obj.experiment_file_dict["Mode"] == "2023"
        obj = self.make_obj([])
        obj.run_cmd()
        dict_now = obj.io.read()
        assert dict_now["Mode"] == "2052"

    def test_GIVEN_cli_argument_WHEN_inputing_all_THEN_test_for_problems(
        self,
    ):
        obj = self.make_obj([])
        obj.experiment_file_dict["Mode"] = "2023"
        obj.write_to_experiment_file({})
        dict_now = obj.io.read()
        assert dict_now["Mode"] == "2023"
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init"]
        with patch.object(sys, "argv", testargs):
            main()
        dict_now = obj.io.read()
        assert dict_now["Mode"] == "2052"