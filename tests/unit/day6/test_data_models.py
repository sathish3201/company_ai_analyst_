from company_ai.data.models import (
    AnalysisRequest,
    ColumnMetadata,
    DataProfile,
    DataType,
    QueryRequest,
    QueryResult,
    TableMetadata,
)


def test_column_metadata():
    column = ColumnMetadata(
        name="revenue",
        data_type=DataType.FLOAT,
    )

    assert column.name == "revenue"
    assert column.data_type == DataType.FLOAT


def test_table_metadata():
    table = TableMetadata(
        name="sales",
        columns=[
            ColumnMetadata(
                name="amount",
                data_type=DataType.FLOAT,
            )
        ],
    )

    assert table.name == "sales"
    assert len(table.columns) == 1


def test_query_request_defaults():
    request = QueryRequest(
        query="SELECT * FROM sales"
    )

    assert request.max_rows == 10000
    assert request.parameters == {}


def test_query_result():
    result = QueryResult(
        columns=["id"],
        rows=[{"id": 1}],
        row_count=1,
    )

    assert result.row_count == 1


def test_data_profile():
    profile = DataProfile(
        row_count=10,
        column_count=3,
    )

    assert profile.row_count == 10


def test_analysis_request():
    request = AnalysisRequest(
        operation="head",
    )

    assert request.operation == "head"