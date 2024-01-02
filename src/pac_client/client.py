import asyncio

from src.pac_client.series_dispatcher import SeriesDispatcher

if __name__ == "__main__":
    """
    Create a Series Dispatcher object and run it's infinite `main()` method in a event loop.
    """
    dispatcher = SeriesDispatcher()
    dispatcher.loop = asyncio.get_event_loop()
    dispatcher.loop.run_until_complete(dispatcher.main())
