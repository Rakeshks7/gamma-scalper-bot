import asyncio
from ib_insync import *
from config import *
from logger import log
import math

class GammaScalper:
    def __init__(self):
        self.ib = IB()
        self.underlying_contract = None
        self.options_contracts = []
        self.is_running = False

    async def connect(self):
        try:
            log.info(f"Connecting to IBKR on {IB_HOST}:{IB_PORT}...")
            await self.ib.connectAsync(IB_HOST, IB_PORT, clientId=CLIENT_ID)
            log.info("Successfully connected to IBKR.")
        except Exception as e:
            log.critical(f"Connection failed: {e}")
            raise SystemExit

    async def setup_market_data(self):
        
        self.underlying_contract = Stock(SYMBOL, EXCHANGE, CURRENCY)
        await self.ib.qualifyContractsAsync(self.underlying_contract)
        self.ib.reqMktData(self.underlying_contract, '', False, False)
        log.info(f"Subscribed to Underlying: {self.underlying_contract.localSymbol}")

        call = Option(SYMBOL, EXPIRY, STRIKE, 'C', EXCHANGE, CURRENCY)
        put = Option(SYMBOL, EXPIRY, STRIKE, 'P', EXCHANGE, CURRENCY)
        
        self.options_contracts = [call, put]
        contracts = await self.ib.qualifyContractsAsync(*self.options_contracts)
        
        for c in contracts:
            self.ib.reqMktData(c, '100,101,104,106', False, False)
            log.info(f"Subscribed to Option: {c.localSymbol}")

    def get_net_delta(self):
        net_delta = 0.0
        
        positions = self.ib.positions()
        
        for pos in positions:
            contract = pos.contract
            
            if contract in self.options_contracts:
                ticker = self.ib.ticker(contract)
                if ticker.modelGreeks:
                    opt_delta = ticker.modelGreeks.delta
                    if opt_delta is not None:
                        contribution = opt_delta * 100 * pos.position
                        net_delta += contribution
                else:
                    log.warning(f"Greeks not ready for {contract.localSymbol}")

            elif contract.symbol == SYMBOL and contract.secType == 'STK':
                net_delta += pos.position  

        return net_delta

    async def execute_hedge(self, delta_exposure):
        
        hedge_qty = int(-delta_exposure)
        
        if abs(hedge_qty) < MIN_TRADE_SIZE:
            return

        action = 'BUY' if hedge_qty > 0 else 'SELL'
        quantity = abs(hedge_qty)

        current_stk_pos = 0
        for p in self.ib.positions():
            if p.contract.symbol == SYMBOL and p.contract.secType == 'STK':
                current_stk_pos = p.position
        
        if abs(current_stk_pos + hedge_qty) > MAX_POSITION:
            log.error(f"RISK HALT: Hedge would exceed max position limit of {MAX_POSITION}.")
            return

        order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(self.underlying_contract, order)
        
        log.info(f"HEDGING TRIGGERED: {action} {quantity} {SYMBOL} | Net Delta was: {delta_exposure:.2f}")
        
        while not trade.isDone():
            await asyncio.sleep(0.1)
        
        log.info(f"ORDER FILLED: {trade.orderStatus.avgFillPrice}")

    async def run_loop(self):
        self.is_running = True
        log.info("Bot logic started. Monitoring Delta...")

        while self.is_running:
            try:
                current_net_delta = self.get_net_delta()
                
                log.info(f"Heartbeat: Net Delta: {current_net_delta:.2f}")

                if abs(current_net_delta) > DELTA_THRESHOLD:
                    log.warning(f"Threshold Breached! Delta: {current_net_delta:.2f} > {DELTA_THRESHOLD}")
                    await self.execute_hedge(current_net_delta)

                await asyncio.sleep(SLEEP_INTERVAL)

            except Exception as e:
                log.error(f"Loop Error: {e}")
                await asyncio.sleep(5)

    def stop(self):
        self.is_running = False
        self.ib.disconnect()