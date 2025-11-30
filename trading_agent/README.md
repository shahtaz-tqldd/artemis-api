performance_review_agent = (
    "Analyzes closed and open trades from connected broker or uploaded history. "
    "Calculates win rate, expectancy, profit factor, max drawdown, Sharpe/Sortino ratios, "
    "best/worst pairs, sessions, and setups. Identifies behavioral patterns (overtrading, "
    "revenge trading, FOMO, cutting winners early, etc.) and delivers weekly/monthly performance reports."
)

trade_news_agent = (
    "Searches real-time forex news (Reuters, Bloomberg, ForexLive, central bank sites) "
    "and relevant X/Twitter sources for events affecting the user’s watched pairs or open positions. "
    "Returns concise, neutral bullet-point summaries with direct pair impact within 2 minutes of release."
)

market_regime_agent = (
    "Determines current market regime for each major and minor pair across multiple timeframes "
    "(strong trend, range-bound, high-volatility breakout, low-volatility compression) "
    "using ADX, ATR, Bollinger Bandwidth, and price-action structure. Clearly labels the regime "
    "for strategy adaptation."
)

risk_manager_agent = (
    "Enforces user-defined risk rules on every discussed trade: maximum risk % per trade, "
    "daily/weekly loss limits, volatility-adjusted position sizing, valid stop-loss placement "
    "(ATR or structure-based), minimum R:R, concurrent trade limits, drawdown protection, "
    "and leverage safety. Instantly flags and explains any violation. Also covers compliance "
    "(no martingale, no gambling-style behavior)."
)

economic_calendar_agent = (
    "Provides today’s and upcoming high-impact events (NFP, CPI, FOMC, ECB, BoJ, etc.) "
    "with previous/consensus/actual figures. Delivers pre-event volatility forecasts, "
    "historical pair reactions, and post-event interpretation of surprise magnitude and likely directional bias."
)

sentiment_agent = (
    "Aggregates real-time sentiment data: retail positioning (OANDA, IG, Myfxbook), "
    "COT net positions (trader categories), swap sentiment (SSCF), order-book imbalance (when available), "
    "and X/Twitter sentiment scores. States whether the crowd is extremely one-sided (contrarian signal) "
    "or balanced for each major pair."
)

correlation_exposure_agent = (
    "Monitors all open positions and calculates net currency exposure (e.g., net USD long/short), "
    "correlation risk across pairs, hedging ratio, total margin usage, and concentration risks "
    "(commodity bloc, EUR crosses, etc.). Immediately highlights over-exposure or dangerous correlations."
)

trade_idea_validator_agent = (
    "Takes any user-proposed trade idea (pair, direction, entry, SL, TP) and runs it through "
    "a full validation pipeline: regime compatibility, news conflict, sentiment alignment, "
    "correlation impact, risk-manager approval, R:R quality, and historical edge in similar conditions. "
    "Returns clear GO / NO-GO verdict with detailed reasoning."
)

journal_pattern_agent = (
    "Maintains a living trade journal. After each closed trade (manual input or auto-import), "
    "tags setup type, emotional state, mistakes, and adherence to plan. Over time reveals "
    "recurring psychological and strategic patterns with personalized improvement suggestions."
)

backtest_setup_researcher_agent = (
    "On demand, performs lightweight historical research (last 2–5 years) on price-action "
    "or indicator setups the user describes. Returns win rate, average R:R, profitability by session/timeframe, "
    "and seasonality — strictly for educational/backtesting purposes, never as live signals."
)