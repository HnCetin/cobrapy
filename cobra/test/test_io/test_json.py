# -*- coding: utf-8 -*-

"""Test functionalities of json.py"""

from __future__ import absolute_import

import json
from os.path import join

import pytest

import cobra.io as cio
from cobra.test.test_io.conftest import compare_models


@pytest.mark.xfail(reason="schema outdated")
def test_validate_json(data_directory):
    """Validate file according to JSON-schema."""
    jsonschema = pytest.importorskip("jsonschema")
    with open(join(data_directory, "mini.json"),
              "r", encoding="utf-8") as infile:
        loaded = json.load(infile)
    assert jsonschema.validate(loaded, cio.json.json_schema)


def test_load_json_model(data_directory, mini_model):
    """Test the reading of JSON model."""
    json_model = cio.load_json_model(join(data_directory, "mini.json"))
    assert compare_models(mini_model, json_model) is None


@pytest.mark.xfail(reason="schema outdated")
def test_save_json_model(tmpdir, mini_model):
    """Test the writing of JSON model."""
    jsonschema = pytest.importorskip("jsonschema")
    output_file = tmpdir.join("mini.json")
    cio.save_json_model(mini_model, output_file.strpath, pretty=True)
    # validate against JSONSchema
    with open(output_file, "r") as infile:
        loaded = json.load(infile)
    assert jsonschema.validate(loaded, cio.json.json_schema)


def test_reaction_bounds_json(data_directory, tmp_path):
    """Test reading and writing of model with inf bounds in json"""

    """Path to XML file with INF bounds"""
    path_to_xml_inf_file = join(data_directory, "fbc_ex1.xml")
    model_xml_inf = cio.read_sbml_model(path_to_xml_inf_file)
    path_to_output = join(str(tmp_path), 'fbc_ex1_json.json')

    """Saving model with inf bounds in json form without error"""
    cio.save_json_model(model_xml_inf, path_to_output)

    """Path to JSON file with INF bounds"""
    path_to_JSON_inf_file = join(data_directory, "JSON_with_inf_bounds.json")
    model_json_inf = cio.load_json_model(path_to_JSON_inf_file)
    assert model_json_inf.reactions[0].upper_bound == float('inf')
