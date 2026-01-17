import asyncio
from gamma_scalper import GammaScalper
from logger import log

async def main():
    bot = GammaScalper()
    
    try:
        await bot.connect()
        await bot.setup_market_data()
        
        log.info("Warming up data streams (3s)...")
        await asyncio.sleep(3)
        
        await bot.run_loop()
        
    except KeyboardInterrupt:
        log.info("Manual Stop Requested.")
    finally:
        bot.stop()
        log.info("Bot Shutdown.")

if __name__ == '__main__':
    asyncio.run(main())