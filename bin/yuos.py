import argparse
import logging
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from yuos_query import YuosServer


def main(url, instrument, cache_filepath, proxies, update_interval=3200):
    while True:
        try:
            YuosServer.create(
                url, os.environ.get("YUOS_TOKEN"), instrument, cache_filepath, proxies
            ).update_cache()
            logging.info("updated cache")
            time.sleep(update_interval)
        except Exception as error:
            logging.error(f"failed to update cache: {error}")
            time.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-u",
        "--url",
        type=str,
        help="the URL for the proposal system",
        required=True,
    )

    required_args.add_argument(
        "-i", "--instrument", type=str, help="the instrument name", required=True
    )

    required_args.add_argument(
        "-c",
        "--cache-filepath",
        type=str,
        help="where to write the data",
        required=True,
    )

    parser.add_argument(
        "-hp",
        "--http-proxy",
        type=str,
        default="",
        help="the http proxy if required",
    )

    parser.add_argument(
        "-l",
        "--log-level",
        type=int,
        default=3,
        help="sets the logging level: debug=1, info=2, warning=3, error=4, critical=5.",
    )

    args = parser.parse_args()

    if 1 <= args.log_level <= 5:
        logging.basicConfig(
            format="%(asctime)s - %(message)s", level=args.log_level * 10
        )
    else:
        logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    proxies = {"https": args.http_proxy} if args.http_proxy else {}

    main(
        args.url,
        args.instrument,
        args.cache_filepath,
        proxies,
    )
