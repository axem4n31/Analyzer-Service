import pytest
from service import get_llm_prompt
from models.schema import SalesDataSchema, ProductSchema


@pytest.mark.asyncio
async def test_get_llm_prompt():
    data = SalesDataSchema(
        date="2024-11-19",
        products=[
            ProductSchema(
                id=1, name="Product 1", quantity=10, price=100.0, category="Category 1"
            ),
            ProductSchema(
                id=2, name="Product 2", quantity=5, price=200.0, category="Category 2"
            ),
        ],
    )
    prompt = await get_llm_prompt(data)
    assert "Проанализируй данные о продажах за 2024-11-19" in prompt
    assert "Общая выручка: 2000.0" in prompt
    assert "Топ-3 товара по продажам: ['Product 1', 'Product 2']" in prompt
