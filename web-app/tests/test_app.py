"""This is the module to test the streamlit app functionality"""

import pytest  # pylint: disable=unused-import
import streamlit as st  # pylint: disable=unused-import


# Test functions
def test_sanity_check():
    """Basic test to ensure pytest runs properly"""
    expected = True
    actual = True
    assert actual == expected, "Expected True to be equal to True!"
