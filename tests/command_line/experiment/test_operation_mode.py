import os
import sys

import pytest
import unittest
from unittest.mock import patch
import numpy as np

import daf.utils.dafutilities as du
from daf.command_line.experiment.operation_mode import OperationMode
import daf.utils.generate_daf_default as gdd
from daf.core.main import DAF


class TestDAF(unittest.TestCase):
    def setUp(self):
        data_sim = gdd.default
        data_sim["simulated"] = True
        data_sim["PV_energy"] = 10000.0
        gdd.generate_file(data=data_sim, file_name=".Experiment")

    def tearDown(self):
        os.system("rm .Experiment")

    @staticmethod
    def make_obj(command_line_args: list) -> OperationMode:
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init"]
        for arg in command_line_args:
            testargs.append(arg)
        with patch.object(sys, "argv", testargs):
            obj = OperationMode()
        return obj

    def test_GIVEN_cli_argument_WHEN_inputing_mode_215_THEN_check_parsed_args(
        self,
    ):
        obj = self.make_obj(["215"])
        assert obj.parsed_args_dict["Mode"] == "215"

    def test_GIVEN_cli_argument_WHEN_inputing_mode_2052_THEN_check_parsed_args(
        self,
    ):
        obj = self.make_obj(["2052"])
        assert obj.parsed_args_dict["Mode"] == "2052"

    def test_GIVEN_cli_argument_WHEN_inputing_mode_225_THEN_check_parsed_args(
        self,
    ):
        obj = self.make_obj(["225"])
        assert obj.parsed_args_dict["Mode"] == "225"

    def test_GIVEN_cli_argument_WHEN_inputing_mode_215_THEN_check_if_it_was_written_correctly(
        self,
    ):
        obj = self.make_obj(["215"])
        obj.run_cmd(obj.parsed_args_dict)
        dict_now = du.read()
        assert "215" == dict_now["Mode"]

    def test_GIVEN_cli_argument_WHEN_inputing_mode_2052_THEN_check_if_it_was_written_correctly(
        self,
    ):
        obj = self.make_obj(["2052"])
        obj.run_cmd(obj.parsed_args_dict)
        dict_now = du.read()
        assert "2052" == dict_now["Mode"]

    def test_GIVEN_cli_argument_WHEN_inputing_mode_225_THEN_check_if_it_was_written_correctly(
        self,
    ):
        obj = self.make_obj(["225"])
        obj.run_cmd(obj.parsed_args_dict)
        dict_now = du.read()
        assert "225" == dict_now["Mode"]
