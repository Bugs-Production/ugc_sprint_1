import asyncio
import json
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.clickhouse import initialize_clickhouse
from etl_modules.brokers import KafkaBroker
from etl_modules.extractors import KafkaExtractor
from etl_modules.loaders import loader
from etl_modules.transformers import event_transformer
from logger import setup_logger
from pydantic_core._pydantic_core import ValidationError
from settings.config import BATCH_SIZE, settings

logger = logging.getLogger("etl")


async def main():
    async with KafkaBroker() as broker:
        batch = []
        extractor = KafkaExtractor(broker)
        async for event in extractor.extract():
            try:
                event_data = json.loads(event.decode("utf-8"))
                batch.append(event_transformer.transform(event_data))
                if len(batch) == BATCH_SIZE:
                    loader.load(batch)
                    batch.clear()
            except json.JSONDecodeError as e:
                logger.error(e)
            except ValidationError as e:
                logger.error(e)
        if batch:
            loader.load(batch)


if __name__ == "__main__":
    setup_logger()
    initialize_clickhouse()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, "interval", seconds=settings.scheduler_interval_seconds)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
    asyncio.run(main())
