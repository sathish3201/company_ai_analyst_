import pytest

from company_ai.data.access.query_validator import (
    ReadOnlyQueryValidator,
)
from company_ai.data.exceptions import (
    QueryValidationError,
)


def test_select_query_is_allowed():

    validator = ReadOnlyQueryValidator()

    result = validator.validate(
        "SELECT * FROM employees"
    )

    assert result == "SELECT * FROM employees"


def test_with_query_is_allowed():

    validator = ReadOnlyQueryValidator()

    result = validator.validate(
        "WITH data AS "
        "(SELECT * FROM employees) "
        "SELECT * FROM data"
    )

    assert result.startswith("WITH")


@pytest.mark.parametrize(
    "query",
    [
        "DELETE FROM employees",
        "UPDATE employees SET salary = 0",
        "INSERT INTO employees VALUES (1)",
        "DROP TABLE employees",
        "TRUNCATE TABLE employees",
        "ALTER TABLE employees ADD test INT",
        "CREATE TABLE test(id INT)",
    ],
)
def test_write_queries_are_rejected(query):

    validator = ReadOnlyQueryValidator()

    with pytest.raises(QueryValidationError):
        validator.validate(query)


def test_empty_query_is_rejected():

    validator = ReadOnlyQueryValidator()

    with pytest.raises(QueryValidationError):
        validator.validate("")