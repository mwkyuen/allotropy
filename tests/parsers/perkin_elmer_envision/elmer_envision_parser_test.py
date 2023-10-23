import pytest

from allotropy.allotrope.allotrope import AllotropeConversionError
from allotropy.parser_factory import Vendor
from allotropy.parsers.perkin_elmer_envision.elmer_envision_parser import (
    ElmerEnvisionParser,
)
from allotropy.parsers.utils.timestamp_parser import TimestampParser
from tests.parsers.perkin_elmer_envision.elmer_envision_data import get_data, get_model
from tests.parsers.test_utils import from_file, validate_contents, validate_schema

output_files = (
    "PE_Envision_fluorescence_example01",
    "PE_Envision_fluorescence_example02",
    "PE_Envision_fluorescence_example03",
)

VENDOR_TYPE = Vendor.PERKIN_ELMER_ENVISION


@pytest.mark.parametrize("output_file", output_files)
def test_parse_elmer_envision_to_asm(output_file: str) -> None:
    test_filepath = f"tests/parsers/perkin_elmer_envision/testdata/{output_file}.csv"
    expected_filepath = (
        f"tests/parsers/perkin_elmer_envision/testdata/{output_file}.json"
    )
    allotrope_dict = from_file(test_filepath, VENDOR_TYPE)
    validate_schema(allotrope_dict, "fluorescence/BENCHLING/2023/09/fluorescence.json")
    validate_contents(allotrope_dict, expected_filepath)


@pytest.mark.short
def test_get_model() -> None:
    parser = ElmerEnvisionParser(TimestampParser())
    model = parser._get_model(get_data())

    if model.measurement_aggregate_document:
        model.measurement_aggregate_document.measurement_identifier = ""

    assert model == get_model()


@pytest.mark.parametrize("output_file", output_files)
def test_parse_missing_file(output_file: str) -> None:
    test_filepath = f"tests/parsers/perkin_elmer_envision/testdata/{output_file}.tsv"
    with pytest.raises(FileNotFoundError):
        from_file(test_filepath, VENDOR_TYPE)


@pytest.mark.parametrize("output_file", output_files)
def test_parse_incorrect_vendor(output_file: str) -> None:
    test_filepath = f"tests/parsers/perkin_elmer_envision/testdata/{output_file}.csv"
    with pytest.raises(AllotropeConversionError):
        from_file(test_filepath, Vendor.AGILENT_GEN5)


def test_parse_file_missing_headers() -> None:
    test_filepath = (
        "tests/parsers/perkin_elmer_envision/testdata/example01_missing_header.csv"
    )
    with pytest.raises(AllotropeConversionError):
        from_file(test_filepath, VENDOR_TYPE)
