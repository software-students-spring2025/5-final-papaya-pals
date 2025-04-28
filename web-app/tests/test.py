""""""

import pytest
import streamlit as st


class Tests:

    # Test functions
    def test_sanity_check(self):
        """Basic test to ensure pytest runs properly"""
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True!"
