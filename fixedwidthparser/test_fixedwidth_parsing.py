import  pytest
from parser import create_fixed_length, create_fixed_width_parser


@pytest.fixture
def fixed_length_string():
    return "melbourne is a big city"


def test_fixed_length_greater_than_zero(fixed_length_string):
    print(fixed_length_string)
    word1=create_fixed_length(value=fixed_length_string, allowed_length=12)
    word2=create_fixed_length(value=fixed_length_string, allowed_length=10)
    assert word1=="melbourne is"
    assert word2=="melbourne "
   

def test_fixed_length_less_than_zero(fixed_length_string):
    word1=create_fixed_length(value=fixed_length_string, allowed_length=-1)
    assert word1==""


def test_fixed_width_parser(fixed_length_string):
    parser=create_fixed_width_parser(field_widths=[3,2,7])
    parse_line=parser(fixed_length_string)
    assert parse_line[0]=="mel"
    assert parse_line[1]=="bo"
    assert parse_line[2]=="urne is"
