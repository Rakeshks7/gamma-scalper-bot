# The Math & Logic: Gamma Scalping

## 1. The Concept
Gamma Scalping is a non-directional strategy used by volatility traders and market makers. The goal is not to predict where the stock is going, but to profit from the **movement** (volatility) of the stock, regardless of direction.

The bot manages a **Long Straddle** (Long Call + Long Put) which gives the portfolio **Positive Gamma**.

## 2. The Greeks
To understand the code, you must understand the variables it monitors:

* **Delta ($\Delta$):** Represents directional risk.
    * If $\Delta = +50$, your position acts like owning 50 shares of stock.
    * If stock goes up \$1, you make \$50.
* **Gamma ($\Gamma$):** The rate of change of Delta.
    * As stock moves, Delta changes. This change is Gamma.
    * Long Options have **Positive Gamma**. This means as the stock rises, your position gets *longer* (Delta increases). As stock falls, your position gets *shorter* (Delta decreases).
* **Theta ($\Theta$):** Time decay.
    * The cost of holding long options. This is the "rent" you pay every day to hold the position.

## 3. The Mechanism: Buy Low, Sell High
Because we are **Long Gamma**, our Delta helps us automatically.

### Scenario: Stock is at $100. We hold a Straddle.
* **Start:** Net Delta is 0 (Neutral).

### Step A: Stock Rises to $102
1.  Because of Gamma, our Call Delta increases and Put Delta (negative) shrinks.
2.  **New Net Delta:** +40.
3.  **Bot Action:** The bot sees we are "Long 40 shares". To be neutral, it **SELLS 40 shares** of stock at $102.
4.  **Result:** We locked in cash. We are Delta Neutral again.

### Step B: Stock Falls back to $100
1.  The stock drops. Our Call Delta decreases.
2.  **New Net Delta:** -40 (because we are short the 40 shares we sold at $102).
3.  **Bot Action:** The bot sees we are "Short 40 shares". To be neutral, it **BUYS 40 shares** back at $100.
4.  **Result:** We sold at \$102 and bought at \$100. We made a profit on the shares.

## 4. The Profit Equation
The strategy is a battle between **Realized Volatility** (Scalping) and **Implied Volatility** (Theta).

$$\text{Profit} = (\text{Gamma PnL from Scalping}) - (\text{Theta Decay})$$

* **If the market is choppy:** The bot triggers frequently, harvesting small profits that exceed the daily Theta cost.
* **If the market is flat:** The bot sits idle, and you lose money on Theta decay.

## 5. Why this Bot?
Manual gamma scalping is impossible.
* Humans cannot calculate composite Delta across multiple option legs in real-time.
* Humans hesitate.
* This bot executes purely on math: `If Delta > Threshold, Hedge.`