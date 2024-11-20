from fastapi import UploadFile, File, HTTPException
import xml.etree.ElementTree as ET
import heapq
from models.schema import SalesDataSchema


async def parse_xml_to_dict(file: UploadFile = File(...)) -> SalesDataSchema:
    try:
        contents = await file.read()
        root = ET.fromstring(contents)

        date = root.attrib.get("date")
        if not date:
            raise HTTPException(
                status_code=400, detail="Date attribute is missing in XML."
            )

        products_data = []
        for product in root.find("products"):
            product_data = {
                "id": int(product.find("id").text),
                "name": product.find("name").text,
                "quantity": int(product.find("quantity").text),
                "price": float(product.find("price").text),
                "category": product.find("category").text,
            }
            products_data.append(product_data)

        sales_data = SalesDataSchema(date=date, products=products_data)

        return sales_data

    except ET.ParseError:
        raise HTTPException(status_code=400, detail="Error parsing XML file.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")


async def get_llm_prompt(data: SalesDataSchema) -> str:
    products = {}
    total_revenue = 0
    categories = set()
    for product in data.products:
        total_revenue += product.quantity * product.price
        products[product.name] = product.quantity
        if product.category not in categories:
            categories.add(product.category)

    top_products = heapq.nlargest(3, products, key=products.get)

    prompt = (
        f"Проанализируй данные о продажах за {data.date}:"
        f"1. Общая выручка: {total_revenue}"
        f"2. Топ-3 товара по продажам: {top_products}"
        f"3. Распределение по категориям: {categories}"
        f"Составь краткий аналитический отчет с выводами и рекомендациями."
    )
    return prompt
