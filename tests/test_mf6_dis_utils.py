import math

import pytest

from xmipy import XmiWrapper
from xmipy.errors import TimerError


def test_timing_initialize(flopy_dis, modflow_lib_path):
    mf6 = XmiWrapper(
        lib_path=modflow_lib_path, working_directory=flopy_dis.sim_path, timing=True
    )

    # Write output to screen:
    mf6.set_int("ISTDOUTTOFILE", 0)

    try:
        # Run initialize
        mf6.initialize()

        total = mf6.report_timing_totals()

        assert total > 0.0
    finally:
        mf6.finalize()


def test_timing_nothing(flopy_dis, modflow_lib_path):
    mf6 = XmiWrapper(
        lib_path=modflow_lib_path, working_directory=flopy_dis.sim_path, timing=True
    )

    # Write output to screen:
    mf6.set_int("ISTDOUTTOFILE", 0)

    totals = mf6.report_timing_totals()

    assert math.isclose(totals, 0.0)


def test_deactivated_timing(flopy_dis, modflow_lib_path):
    mf6 = XmiWrapper(
        lib_path=modflow_lib_path, working_directory=flopy_dis.sim_path, timing=False
    )

    # Write output to screen:
    mf6.set_int("ISTDOUTTOFILE", 0)

    try:
        # Run initialize
        mf6.initialize()

        with pytest.raises(TimerError):
            mf6.report_timing_totals()
    finally:
        mf6.finalize()


def test_dependencies(flopy_dis, modflow_lib_path):
    XmiWrapper(
        lib_path=modflow_lib_path,
        lib_dependency=modflow_lib_path,
        working_directory=flopy_dis.sim_path,
    )
