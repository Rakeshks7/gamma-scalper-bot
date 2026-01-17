# Gamma Scalper: Dynamic Delta Hedging Bot

[![Language](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Broker-Interactive%20Brokers-red?style=for-the-badge&logo=interactive-brokers&logoColor=white)](https://www.interactivebrokers.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

---

##  Overview

**Gamma Scalper** is a production-grade volatility trading engine designed for the Interactive Brokers (IBKR) TWS API. 

It automates the process of **Delta Neutral Market Making**. By continuously monitoring the Greeks of an options portfolio (specifically Long Straddles or Strangles), the bot algorithmically trades the underlying asset to re-hedge the position, effectively "scalping" profits from market oscillations while neutralizing directional risk.

> **Read the Theory:** [Understanding the Math & Strategy](STRATEGY.md)

##  Key Features

* **Real-Time Greek Monitoring:** Streams live Delta data directly from IBKR's risk navigator engine.
* **Dynamic Thresholding:** User-defined Delta limits (e.g., hedge only when Delta drifts > 50).
* **Asynchronous Core:** Built on `asyncio` and `ib_insync` for non-blocking execution—essential for high-frequency environments.
* **Safety Guards:** Hard-coded position limits and max-order-size checks to prevent runaway algorithms.
* **Professional Logging:** Structured, color-coded logs for audit trails and debugging.

##  Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Core Logic** | `Python 3.10` | Main application logic |
| **API Wrapper** | `ib_insync` | Asynchronous wrapper for IBKR Native API |
| **Data Processing** | `Pandas` / `Numpy` | Vectorized calculations for exposure |
| **Concurrency** | `AsyncIO` | Event loop management |
| **Logging** | `ColorLog` | Console visibility |

##  Quick Start

### 1. Prerequisites
* **Interactive Brokers Account** (Paper Trading strongly recommended).
* **TWS (Trader Workstation)** or **IB Gateway** running locally.
* **Python 3.9+**.

### 2. TWS Configuration
Navigate to `Global Configuration > API > Settings`:
* ✅ Enable ActiveX and Socket Clients
* ❌ Uncheck "Read-Only API"
* **Socket Port:** `7497` (Paper) or `7496` (Live)

###  Logic Flow
Connect to TWS API.

Subscribe to market data for the Underlying and the Option legs.

Calculate Net Delta = (Option Delta * 100 * Qty) + (Stock Shares).

Evaluate:

If Net Delta > +THRESHOLD: SELL Stock (Flatten Long exposure).

If Net Delta < -THRESHOLD: BUY Stock (Flatten Short exposure).

Loop every N seconds.

### Disclaimer
FOR EDUCATIONAL PURPOSES ONLY.

This software is provided "as is" and is not financial advice.

Risk: Volatility trading involves substantial risk of loss.

Testing: NEVER run this on a live account without extensive testing in a Paper Trading environment.

Liability: The contributors are not responsible for any financial losses incurred by the use of this software.