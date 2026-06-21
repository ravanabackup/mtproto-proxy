import asyncio
import argparse
from src import storage, checker, generator, providers, logger
import logging


logger.setup_logger()
logger_ = logging.getLogger("System")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "MTProto Proxy Aggregation Tool\n\n"
            "This tool allows you to fetch, "
            "check and validate proxies"
        )
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-a",
        "--auto",
        action="store_true",
        help="Automatic mode fetches fresh proxies from providers and collect them"
    )

    group.add_argument(
        "-m",
        "--manual",
        action="store_true",
        help="Manual mode works with raw proxy file that prepared by you"
    )

    return parser.parse_args()


async def main():
    args = parse_arguments()

    if args.auto:
        logger_.info("Running in automatic mode...")
        await providers.aggregate_proxies()
    elif args.manual:
        logger_.info("Running in manual mode...")
    
    raw_proxies = storage.load_raw_proxies()
    if not raw_proxies:
        print("no raw proxies found")
        return
    
    alive_proxies = await checker.run_checker(raw_proxies)

    storage.save_results(alive_proxies)

    valid_data = storage.load_valid_json()
    stats = generator.calculate_metrics(len(raw_proxies), valid_data)

    generator.generate_readme(stats)
    generator.send_telegram_notification(stats)

if __name__ == "__main__":
    asyncio.run(main())