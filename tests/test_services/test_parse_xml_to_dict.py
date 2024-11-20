import datetime

import pytest
from fastapi import UploadFile
from service import parse_xml_to_dict
from io import BytesIO
from models.schema import SalesDataSchema


@pytest.mark.asyncio
async def test_parse_xml_to_dict_valid_data():
    xml_content = """<root date="2024-11-19">
        <products>
            <product>
                <id>1</id>
                <name>Product 1</name>
                <quantity>10</quantity>
                <price>100.0</price>
                <category>Category 1</category>
            </product>
            <product>
                <id>2</id>
                <name>Product 2</name>
                <quantity>5</quantity>
                <price>200.0</price>
                <category>Category 2</category>
            </product>
        </products>
    </root>"""
    file = UploadFile(filename="test.xml", file=BytesIO(xml_content.encode()))
    sales_data = await parse_xml_to_dict(file)

    assert isinstance(sales_data, SalesDataSchema)
    assert sales_data.date == datetime.date(2024, 11, 19)
    assert len(sales_data.products) == 2
    assert sales_data.products[0].name == "Product 1"
    assert sales_data.products[0].price == 100.0


@pytest.mark.asyncio
async def test_parse_xml_to_dict_invalid_xml():
    invalid_xml_content = "<root><invalid></root>"
    file = UploadFile(filename="test.xml", file=BytesIO(invalid_xml_content.encode()))
    with pytest.raises(Exception) as excinfo:
        await parse_xml_to_dict(file)
    assert "Error parsing XML file" in str(excinfo.value)
