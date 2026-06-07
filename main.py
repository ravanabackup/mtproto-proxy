import asyncio
from src import storage, checker, generator


async def main():
    raw_proxies = storage.load_raw_proxies()
    if not raw_proxies:
        print("no raw proxies found")
        return
    
    print(f"Testing... (found {len(raw_proxies)} unique proxies)")
    alive_proxies = await checker.run_checker(raw_proxies)

    storage.save_results(alive_proxies)

    valid_data = storage.load_valid_json()
    stats = generator.calculate_metrics(len(raw_proxies), valid_data)

    print("Generating README...")
    generator.generate_readme(stats)


if __name__ == "__main__":
    asyncio.run(main())