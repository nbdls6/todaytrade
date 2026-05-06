# backfill_events.py
import time
import pandas as pd
import moomoo as ft # pyright: ignore[reportMissingImports]
from datetime import timedelta
from todaytrade.clients.moomoo_client import MoomooQuoteClient
from todaytrade.global_configs import EVENT_DATA_LOG_FILE_PATH, KLINE_1M_DATA_DIR

KLINE_1M_DATA_DIR.mkdir(parents=True, exist_ok=True)

def backfill_events(client: MoomooQuoteClient) -> None:
    events = pd.read_csv(EVENT_DATA_LOG_FILE_PATH)
    events['event_date'] = pd.to_datetime(events['event_date'])

    unique_codes = events['code'].nunique()
    print(f"Total events : {len(events)}")
    print(f"Unique tickers: {unique_codes}")
    print()

    ret, quota = client.ctx.get_history_kl_quota(get_detail=True)
    if ret == ft.RET_OK:
        print(f"Quota info: {quota}\n")

    success, skipped, failed = 0, 0, 0

    for _, row in events.iterrows():
        code       = f"US.{row['code']}"
        event_date = row['event_date']
        out_file   = KLINE_1M_DATA_DIR / f"{code}_{event_date.date()}.parquet"

        if out_file.exists():
            skipped += 1
            continue

        start = (event_date - timedelta(days=5)).strftime("%Y-%m-%d")
        end   = (event_date + timedelta(days=1)).strftime("%Y-%m-%d")

        try:
            ret, df, _ = client.ctx.request_history_kline(
                code, start=start, end=end, ktype=ft.KLType.K_1M, extented_time=True
            )
            if ret != ft.RET_OK:
                raise RuntimeError(df)
            if df.empty:
                failed += 1
                print(f" {code}  {event_date.date()}  (no data)")
            else:
                df.to_parquet(out_file, index=False)
                success += 1
                print(f" {code}  {event_date.date()}  ({len(df)} bars)")
        except Exception as e:
            failed += 1
            print(f" {code}  {event_date.date()}  ERROR: {e}")

        time.sleep(0.6)  

    print(f"\n{'-'*40}")
    print(f"Done - success: {success}, skipped: {skipped}, failed: {failed}")


if __name__ == "__main__":
    with MoomooQuoteClient() as client:
        backfill_events(client)