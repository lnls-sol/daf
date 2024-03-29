import os
import sys

import pytest
import unittest
from unittest.mock import patch

from daf.command_line.query.status import Status, main
import daf.utils.generate_daf_default as gdd
from daf.command_line.support.init import Init
from daf.core.main import DAF


class TestDAF(unittest.TestCase):
    def setUp(self):
        data_sim = Init.build_current_file(Init, True)
        data_sim["simulated"] = True
        gdd.generate_file(data=data_sim, file_name=".Experiment")

    def tearDown(self):
        os.system("rm .Experiment")

    @staticmethod
    def make_obj(command_line_args: list) -> Status:
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init"]
        for arg in command_line_args:
            testargs.append(arg)
        with patch.object(sys, "argv", testargs):
            obj = Status()
        return obj

    def test_GIVEN_cli_argument_WHEN_passing_mode_option_THEN_check_parsed_args(self):
        obj = self.make_obj(["--mode"])
        assert obj.parsed_args_dict["mode"] == True

    def test_GIVEN_cli_argument_WHEN_passing_experiment_option_THEN_check_parsed_args(
        self,
    ):
        obj = self.make_obj(["--experiment"])
        assert obj.parsed_args_dict["experiment"] == True

    def test_GIVEN_cli_argument_WHEN_passing_sample_option_THEN_check_parsed_args(self):
        obj = self.make_obj(["--sample"])
        assert obj.parsed_args_dict["sample"] == True

    def test_GIVEN_cli_argument_WHEN_passing_umatrix_option_THEN_check_parsed_args(
        self,
    ):
        obj = self.make_obj(["--umatrix"])
        assert obj.parsed_args_dict["umatrix"] == True

    def test_GIVEN_cli_argument_WHEN_passing_bounds_option_THEN_check_parsed_args(self):
        obj = self.make_obj(["--bounds"])
        assert obj.parsed_args_dict["bounds"] == True

    def test_GIVEN_cli_argument_WHEN_passing_all_option_THEN_check_parsed_args(self):
        obj = self.make_obj(["--all"])
        assert obj.parsed_args_dict["all"] == True

    def test_experiment_obj(self):
        obj = self.make_obj(["--all"])
        assert isinstance(obj.exp, DAF)

    def test_GIVEN_cli_argument_WHEN_inputing_mode_THEN_test_for_problems(
        self,
    ):
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init", "-m"]
        with patch.object(sys, "argv", testargs):
            main()

    def test_GIVEN_cli_argument_WHEN_inputing_experiment_THEN_test_for_problems(
        self,
    ):
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init", "-e"]
        with patch.object(sys, "argv", testargs):
            main()

    def test_GIVEN_cli_argument_WHEN_inputing_sample_THEN_test_for_problems(
        self,
    ):
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init", "-s"]
        with patch.object(sys, "argv", testargs):
            main()

    def test_GIVEN_cli_argument_WHEN_inputing_umatrix_THEN_test_for_problems(
        self,
    ):
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init", "-u"]
        with patch.object(sys, "argv", testargs):
            main()

    def test_GIVEN_cli_argument_WHEN_inputing_bounds_THEN_test_for_problems(
        self,
    ):
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init", "-b"]
        with patch.object(sys, "argv", testargs):
            main()

    def test_GIVEN_cli_argument_WHEN_inputing_bounds_THEN_test_for_problems(
        self,
    ):
        testargs = ["/home/hugo/work/SOL/tmp/daf/command_line/daf.init", "-a"]
        with patch.object(sys, "argv", testargs):
            main()
