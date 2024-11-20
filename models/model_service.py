from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from models.model import Category, Product, Sale, DailyReport
from models.schema import SalesDataSchema, ProductSchema
from datetime import date


async def add_data(data: SalesDataSchema, db: AsyncSession) -> bool:
    try:
        sales_date = data.date

        for product_data in data.products:
            result = await db.execute(
                select(Category).filter_by(name=product_data.category)
            )
            category = result.scalars().first()

            if not category:
                category = Category(name=product_data.category)
                db.add(category)
                await db.commit()

            result = await db.execute(
                select(Product)
                .options(joinedload(Product.category))
                .filter_by(id=product_data.id)
            )
            product = result.scalars().first()

            if not product:
                product = Product(
                    id=product_data.id,
                    categoryFK=category.id,
                    name=product_data.name,
                )
                db.add(product)
                await db.commit()
            sale_result = await db.execute(
                select(Sale).filter_by(productFK=product.id, date=sales_date)
            )
            sale = sale_result.scalars().first()

            if sale:
                sale.quantity = product_data.quantity
                sale.price = product_data.price
            else:
                sale = Sale(
                    productFK=product.id,
                    quantity=product_data.quantity,
                    price=product_data.price,
                    date=sales_date,
                )
                db.add(sale)

        await db.commit()
        return True

    except Exception as e:
        await db.rollback()
        raise e


async def add_report_by_date(date_report: date, text: str, db: AsyncSession):
    daily_report = await db.scalar(
        select(DailyReport).where(and_(DailyReport.date == date_report))
    )
    try:
        if daily_report:
            daily_report.report = text
        else:
            daily_report = DailyReport(
                date=date_report,
                report=text,
            )

        db.add(daily_report)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def get_report_by_date(date_report: date, db: AsyncSession) -> str | None:
    report = await db.scalar(
        select(DailyReport).where(and_(DailyReport.date == date_report))
    )
    if report:
        return report.report
    return


async def get_sales_data(date_sale: date, db: AsyncSession) -> SalesDataSchema | None:
    stmt = (
        select(Sale, Product.name, Category.name)
        .join(Product, Sale.productFK == Product.id)
        .join(Category, Product.categoryFK == Category.id)
        .where(Sale.date == date_sale)
    )
    result = await db.execute(stmt)
    try:
        data = result.all()
        products = []
        for sale, product_name, categories in data:
            products.append(
                ProductSchema(
                    id=sale.id,
                    name=product_name,
                    quantity=sale.quantity,
                    price=sale.price,
                    category=categories,
                )
            )
        if products:
            data = SalesDataSchema(date=date_sale, products=products)
            return data
        return
    except Exception as e:
        print(f"get_sales_data error : {e}")
