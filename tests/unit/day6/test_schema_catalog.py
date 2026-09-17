from company_ai.data.models import (
    ColumnMetadata,
    DataType,
    SchemaMetadata,
    TableMetadata,
)
from company_ai.data.schema.catalog import (
    SchemaCatalog,
)


def create_catalog():

    metadata = SchemaMetadata(
        source_name="company_db",
        tables=[
            TableMetadata(
                name="employees",
                columns=[
                    ColumnMetadata(
                        name="employee_id",
                        data_type=DataType.INTEGER,
                    ),
                    ColumnMetadata(
                        name="salary",
                        data_type=DataType.FLOAT,
                    ),
                ],
            )
        ],
    )

    return SchemaCatalog(metadata)


def test_catalog_finds_table():

    catalog = create_catalog()

    assert catalog.has_table("employees")


def test_catalog_is_case_insensitive():

    catalog = create_catalog()

    assert catalog.has_table("EMPLOYEES")


def test_catalog_returns_columns():

    catalog = create_catalog()

    assert catalog.columns("employees") == (
        "employee_id",
        "salary",
    )


def test_catalog_unknown_table():

    catalog = create_catalog()

    assert catalog.get_table("unknown") is None