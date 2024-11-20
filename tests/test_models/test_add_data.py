import datetime

import pytest
from unittest.mock import AsyncMock, MagicMock
from models.schema import SalesDataSchema, ProductSchema
from models.model_service import add_data
from sqlalchemy.engine import Result


@pytest.mark.asyncio
async def test_add_data(mock_db):
    data = SalesDataSchema(
        date=datetime.date(2024, 11, 17),
        products=[
            ProductSchema(
                id=1, name="Product 1", quantity=10, price=100.0, category="Category 1"
            ),
            ProductSchema(
                id=2, name="Product 2", quantity=5, price=200.0, category="Category 2"
            ),
        ],
    )

    mock_result = MagicMock(spec=Result)
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    result = await add_data(data=data, db=mock_db)

    assert result is True
    mock_db.execute.assert_called()
