import os
import pandas as pd
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger("parquet_sink")


def _make_dir(path):
    """create directories if missing."""
    os.makedirs(path, exist_ok=True)


def write_to_parquet(events, topic_name, base_path="data/bronze"):
    """
    write list of events to parquet file partitioned by topic + date.
    """
    if not events:
        return

    try:
        # define target path
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        dir_path = os.path.join(base_path, topic_name, f"date={date_str}")
        _make_dir(dir_path)

        # create dataframe and write
        df = pd.DataFrame(events)
        timestamp = datetime.utcnow().strftime("%H%M%S")
        file_path = os.path.join(dir_path, f"batch_{timestamp}.parquet")
        df.to_parquet(file_path, index=False)

        logger.info(f"wrote {len(df)} events to {file_path}")
    except Exception as e:
        logger.error(f"failed to write events for {topic_name}: {e}")
