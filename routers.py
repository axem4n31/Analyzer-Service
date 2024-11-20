import json
import redis.asyncio as redis
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from models.model_service import (
    add_data,
    add_report_by_date,
    get_report_by_date,
    get_sales_data,
)
from models.model_settings import db_helper, get_redis
from sberai_settings import ai_client
from service import parse_xml_to_dict, get_llm_prompt
from settings import get_logger

api_router = APIRouter(prefix="/api", tags=["API"])


@api_router.post("/upload-xml/", status_code=status.HTTP_200_OK)
async def upload_xml(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    redis: redis.Redis = Depends(get_redis),
):
    logger = get_logger("upload_xml")
    try:
        logger.info(f"Started processing file upload: {file.filename}")
        data = await parse_xml_to_dict(file=file)
        await redis.set(str(data.date), data.json(), ex=timedelta(days=1))
        logger.info(f"Data for date {data.date} cached in Redis")

        if await add_data(data=data, db=db):
            logger.info(f"Data added to the database for {data.date}")
            prompt = await get_llm_prompt(data=data)
            ai_text = await ai_client.ask_a_question(prompt)
            await add_report_by_date(date_report=data.date, text=ai_text, db=db)
            logger.info(f"Report for {data.date} added successfully")
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@api_router.get("/get-daily-report/", status_code=status.HTTP_200_OK)
async def get_daily_report(
    date_report: date,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    redis: redis.Redis = Depends(get_redis),
) -> str:
    logger = get_logger("get_daily_report")  # Get logger instance

    logger.info(f"Fetching daily report for {date_report}")
    report = await redis.get(str(f"report-{date_report}"))
    if report:
        logger.info(f"Report for {date_report} found in Redis")
        return report

    logger.info(f"Report for {date_report} not found in Redis, fetching from DB")
    report = await get_report_by_date(date_report=date_report, db=db)

    if report:
        await redis.set(str(f"report-{date_report}"), report, ex=timedelta(days=1))
        logger.info(f"Report for {date_report} saved to Redis")
        return report

    logger.warning(f"Report for {date_report} not found")
    raise HTTPException(status_code=404, detail="Report not found")


@api_router.get("/get_daily-sales", status_code=status.HTTP_200_OK)
async def get_daily_sales(
    date_sale: date,
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    redis: redis.Redis = Depends(get_redis),
):
    logger = get_logger("get_daily_sales")
    logger.info(f"Fetching sales data for {date_sale}")
    data = await redis.get(str(date_sale))
    if data:
        data = json.loads(data)
        logger.info(f"Sales data for {date_sale} found in Redis")
        return data

    logger.info(f"Sales data for {date_sale} not found in Redis, fetching from DB")
    data = await get_sales_data(date_sale=date_sale, db=db)
    if data:
        await redis.set(str(date_sale), data.json(), ex=timedelta(days=1))
        logger.info(f"Sales data for {date_sale} saved to Redis")
        return data

    logger.warning(f"Sales data for {date_sale} not found")
    raise HTTPException(status_code=404, detail="Data sales not found")
