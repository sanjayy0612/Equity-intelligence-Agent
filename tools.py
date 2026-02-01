# tool.py
from langchain_core.tools import tool
from openbb import obb

# --- INDUSTRY BENCHMARKS ---
INDUSTRY_BENCHMARKS = {
    "Automotive": {
        "profit_margin": {"low": 3, "avg": 6, "high": 10},
        "roe": {"low": 5, "avg": 12, "high": 20},
        "debt_to_equity": {"low": 10, "avg": 50, "high": 100},
        "pe_ratio": {"low": 8, "avg": 15, "high": 25},
        "current_ratio": {"low": 0.8, "avg": 1.2, "high": 1.8}
    },
    "Technology": {
        "profit_margin": {"low": 10, "avg": 20, "high": 35},
        "roe": {"low": 10, "avg": 18, "high": 30},
        "debt_to_equity": {"low": 5, "avg": 25, "high": 60},
        "pe_ratio": {"low": 15, "avg": 30, "high": 60},
        "current_ratio": {"low": 1.0, "avg": 1.8, "high": 3.0}
    },
    "Consumer Cyclical": {
        "profit_margin": {"low": 2, "avg": 5, "high": 10},
        "roe": {"low": 8, "avg": 15, "high": 25},
        "debt_to_equity": {"low": 20, "avg": 60, "high": 120},
        "pe_ratio": {"low": 10, "avg": 20, "high": 35},
        "current_ratio": {"low": 0.9, "avg": 1.3, "high": 2.0}
    },
    "Healthcare": {
        "profit_margin": {"low": 8, "avg": 15, "high": 25},
        "roe": {"low": 10, "avg": 18, "high": 28},
        "debt_to_equity": {"low": 10, "avg": 40, "high": 80},
        "pe_ratio": {"low": 12, "avg": 22, "high": 40},
        "current_ratio": {"low": 1.2, "avg": 2.0, "high": 3.5}
    },
    "Financial Services": {
        "profit_margin": {"low": 15, "avg": 25, "high": 40},
        "roe": {"low": 8, "avg": 12, "high": 18},
        "debt_to_equity": {"low": 100, "avg": 300, "high": 800},
        "pe_ratio": {"low": 8, "avg": 15, "high": 25},
        "current_ratio": {"low": 0.5, "avg": 1.0, "high": 1.5}
    },
    "Energy": {
        "profit_margin": {"low": 3, "avg": 8, "high": 15},
        "roe": {"low": 5, "avg": 12, "high": 20},
        "debt_to_equity": {"low": 20, "avg": 60, "high": 120},
        "pe_ratio": {"low": 8, "avg": 15, "high": 30},
        "current_ratio": {"low": 0.8, "avg": 1.2, "high": 1.8}
    }
}

def get_metric_assessment(value, sector, metric_name):
    """Helper function to assess a metric against industry benchmarks"""
    if value == "N/A" or value is None:
        return "N/A"
    
    # Map common metric names to our benchmark keys
    metric_map = {
        "Profit Margin": "profit_margin",
        "Return on Equity (ROE)": "roe",
        "Debt to Equity": "debt_to_equity",
        "P/E Ratio": "pe_ratio",
        "Current Ratio": "current_ratio"
    }
    
    benchmark_key = metric_map.get(metric_name)
    if not benchmark_key or sector not in INDUSTRY_BENCHMARKS:
        return "No benchmark available"
    
    benchmarks = INDUSTRY_BENCHMARKS[sector][benchmark_key]
    
    # Determine if this is a percentage metric or ratio
    is_percentage = metric_name in ["Profit Margin", "Return on Equity (ROE)"]
    unit = "%" if is_percentage else ""
    
    try:
        val = float(value)
        if val < benchmarks["low"]:
            return f"Below Industry Range ({benchmarks['low']}-{benchmarks['high']}{unit})"
        elif val < benchmarks["avg"]:
            return f"Near Industry Low (Avg: {benchmarks['avg']}{unit})"
        elif val <= benchmarks["high"]:
            return f"Within Industry Range (Avg: {benchmarks['avg']}{unit})"
        else:
            return f"Above Industry Average (Avg: {benchmarks['avg']}{unit})"
    except (ValueError, TypeError):
        return "Unable to compare"

# --- TOOL 1: Name to Ticker Converter ---
@tool
def stock_name(company_name: str):
    """
    Converts a company name (e.g., 'Apple', 'Tesla') into its stock ticker symbol (e.g., 'AAPL', 'TSLA').
    Use this BEFORE fetching stock price if you only have the company name.
    """
    COMPANY_TICKERS = {
        "apple": "AAPL",
        "microsoft": "MSFT",
        "google": "GOOGL",
        "alphabet": "GOOGL",
        "amazon": "AMZN",
        "meta": "META",
        "facebook": "META",
        "tesla": "TSLA",
        "nvidia": "NVDA",
        "netflix": "NFLX",
        "intel": "INTC",
        "amd": "AMD",
        "ibm": "IBM",
        "oracle": "ORCL",
        "salesforce": "CRM",
        "paypal": "PYPL",
        "uber": "UBER",
        "airbnb": "ABNB",
        "coca_cola": "KO",
        "pepsi": "PEP",
        "walmart": "WMT",
        "disney": "DIS",
        "ford": "F",
        "gm": "GM",
        "general motors": "GM",
        "toyota": "TM",
        "zoho": "Not Publicly Traded",
    }
    
    clean_name = company_name.lower().strip()
    return COMPANY_TICKERS.get(clean_name, f"Error: Ticker for '{company_name}' not found in database.")

# --- TOOL 2: Price Fetcher ---
@tool
def get_stock_price(symbol: str):
    """
    Fetches the historical stock price for a given ticker symbol (e.g., 'AAPL', 'NVDA').
    Returns the last 5 days of data.
    """
    print(f"\nDEBUG: 🛠️  Fetching price for {symbol}...") 
    try:
        df = obb.equity.price.historical(symbol, provider="yfinance").to_dataframe()
        return df.tail(5).to_string()
    except Exception as e:
        return f"Error fetching data: {str(e)}"

# --- TOOL 3: Company Profile ---
@tool
def get_company_profile(symbol: str):
    """
    Fetches the company profile and description for a given symbol.
    Use this to understand what a company does.
    """
    print(f"\nDEBUG: 🛠️  Fetching profile for {symbol}...")
    try:
        data = obb.equity.profile(symbol, provider="yfinance").to_dict()
        return str(data)[:1000] 
    except Exception as e:
        return f"Error fetching profile: {str(e)}"

# --- TOOL 4: Enhanced Fundamental Analysis ---
@tool
def fundamental_analysis(symbol: str):
    """
    Fetches a comprehensive fundamental analysis for a given stock symbol.
    Returns key metrics (P/E, EPS, ROE) with INDUSTRY CONTEXT and company profile.
    Use this when asked to 'analyze', 'evaluate', or 'describe' a company's financial health.
    """
    print(f"DEBUG: 🔍 Gathering fundamental intel for {symbol}...")
    try:
        # 1. Fetch Profile
        profile_res = obb.equity.profile(symbol, provider="yfinance")
        if not profile_res.results:
            return f"Error: No profile found for {symbol}"
        cmp_profile = profile_res.results[0].model_dump()

        # 2. Fetch Metrics
        metrics_res = obb.equity.fundamental.metrics(symbol, provider="yfinance")
        if not metrics_res.results:
            return f"Error: No financial metrics found for {symbol}"
        company_metrics = metrics_res.results[0].model_dump()

        # 3. Get sector for benchmarking
        sector = cmp_profile.get("sector", "Unknown")
        
        # 4. Extract and format metrics
        profit_margin = company_metrics.get("profit_margin")
        if profit_margin and isinstance(profit_margin, (int, float)):
            profit_margin_pct = round(profit_margin * 100, 2)
        else:
            profit_margin_pct = "N/A"
            
        roe = company_metrics.get("return_on_equity")
        if roe and isinstance(roe, (int, float)):
            roe_pct = round(roe * 100, 2)
        else:
            roe_pct = "N/A"
            
        debt_to_equity = company_metrics.get("debt_to_equity", "N/A")
        pe_ratio = company_metrics.get("pe_ratio", "N/A")
        current_ratio = company_metrics.get("current_ratio", "N/A")

        # 5. Construct the Enhanced Dictionary with Context
        data_dict = {
            "Company Name": cmp_profile.get("name", "N/A"),
            "Sector": sector,
            "Industry": cmp_profile.get("industry_category", "N/A"),
            "Country": cmp_profile.get("hq_country", "N/A"),
            "Description": cmp_profile.get("long_description", "N/A")[:500] + "...",
            
            # Enhanced metrics with industry context
            "Profit Margin": f"{profit_margin_pct}% - {get_metric_assessment(profit_margin_pct, sector, 'Profit Margin')}",
            "Return on Equity (ROE)": f"{roe_pct}% - {get_metric_assessment(roe_pct, sector, 'Return on Equity (ROE)')}",
            "Debt to Equity": f"{debt_to_equity} - {get_metric_assessment(debt_to_equity, sector, 'Debt to Equity')}",
            "P/E Ratio": f"{pe_ratio} - {get_metric_assessment(pe_ratio, sector, 'P/E Ratio')}",
            "Current Ratio": f"{current_ratio} - {get_metric_assessment(current_ratio, sector, 'Current Ratio')}",
            "EPS": company_metrics.get("eps", "N/A"),
            "Price to Book": company_metrics.get("price_to_book", "N/A"),
            
            # Analysis hint for the LLM
            "ANALYSIS_NOTE": f"This is a {sector} company. Compare metrics against {sector} industry standards, not absolute values."
        }
        
        return str(data_dict)

    except Exception as e:
        return f"Error gathering fundamentals: {str(e)}"

# --- TOOL 5: Comparative Analysis ---
# --- TOOL 5: Comparative Analysis (Optimized with Sorting) ---
@tool
def compare_stocks(symbols: str):
    """
    Compares multiple stocks side-by-side. 
    Input: Comma-separated ticker symbols (e.g., 'TSLA,F,GM')
    Returns: Key metrics comparison table sorted by ROE (High to Low).
    """
    print(f"DEBUG: 📊 Comparing stocks: {symbols}...")
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(",")]
        comparison_data = []
        
        for symbol in symbol_list:
            try:
                # Fetch metrics
                metrics_res = obb.equity.fundamental.metrics(symbol, provider="yfinance")
                profile_res = obb.equity.profile(symbol, provider="yfinance")
                
                if metrics_res.results and profile_res.results:
                    metrics = metrics_res.results[0].model_dump()
                    profile = profile_res.results[0].model_dump()
                    
                    # Safe extraction of ROE for sorting
                    raw_roe = metrics.get("return_on_equity")
                    roe_val = raw_roe if isinstance(raw_roe, (int, float)) else 0
                    
                    comparison_data.append({
                        "Symbol": symbol,
                        "Company": profile.get("name", "N/A"),
                        "ROE %": round(roe_val * 100, 2),
                        "P/E Ratio": metrics.get("pe_ratio", "N/A"),
                        "Debt/Equity": metrics.get("debt_to_equity", "N/A"),
                        # hidden field for sorting
                        "_sort_value": roe_val 
                    })
            except Exception as e:
                comparison_data.append({"Symbol": symbol, "Error": str(e), "_sort_value": -999})
        
        # --- THE FIX: Sort data in Python so the LLM doesn't have to guess ---
        # Sort by ROE descending (Highest first)
        comparison_data.sort(key=lambda x: x.get("_sort_value", 0), reverse=True)
        
        # Remove the hidden sort key before returning string
        for item in comparison_data:
            item.pop("_sort_value", None)
        
        return str(comparison_data)
        
    except Exception as e:
        return f"Error comparing stocks: {str(e)}"

# --- TOOL 6: Capital Allocation Analysis ---
@tool
def get_capital_allocation(symbol: str):
    """
    Analyzes a company's capital allocation strategy including share buybacks, 
    dividends, and how they impact ROE. Use this when ROE is unusually high (>100%).
    """
    print(f"DEBUG: 💰 Analyzing capital allocation for {symbol}...")
    try:
        # Fetch key statistics that show buyback activity
        metrics_res = obb.equity.fundamental.metrics(symbol, provider="yfinance")
        profile_res = obb.equity.profile(symbol, provider="yfinance")
        
        if not metrics_res.results or not profile_res.results:
            return f"Error: Unable to fetch capital allocation data for {symbol}"
        
        metrics = metrics_res.results[0].model_dump()
        profile = profile_res.results[0].model_dump()
        
        # Calculate key indicators
        roe = metrics.get("return_on_equity")
        roe_pct = round(roe * 100, 2) if roe else "N/A"
        
        pb_ratio = metrics.get("price_to_book", "N/A")
        debt_to_equity = metrics.get("debt_to_equity", "N/A")
        
        # Construct analysis
        analysis = {
            "Company": profile.get("name", "N/A"),
            "ROE": f"{roe_pct}%",
            "Price to Book": pb_ratio,
            "Debt to Equity": debt_to_equity,
            
            "Analysis Context": (
                f"High ROE of {roe_pct}% combined with P/B ratio of {pb_ratio} suggests "
                f"{'aggressive buyback activity ' if isinstance(pb_ratio, (int, float)) and pb_ratio > 10 else ''}"
                f"and efficient capital allocation. "
                f"The debt-to-equity ratio of {debt_to_equity} indicates "
                f"{'conservative' if isinstance(debt_to_equity, (int, float)) and debt_to_equity < 50 else 'moderate'} "
                f"use of leverage."
            ),
            
            "ROE Interpretation": (
                "Very high ROE (>100%) typically results from: "
                "1) Share buyback programs reducing equity base, "
                "2) Efficient use of debt financing, "
                "3) Exceptional operational performance. "
                f"For {profile.get('name', 'this company')}, the combination of metrics suggests "
                "this is a deliberate capital allocation strategy, not financial distress."
            )
        }
        
        return str(analysis)
        
    except Exception as e:
        return f"Error analyzing capital allocation: {str(e)}"
    
@tool
def get_institutional_ownership(symbol: str):
    """
    Shows major institutional holders (Vanguard, BlackRock, etc.)
    and recent changes in their positions.
    get the data top companies holding the stock
    so that we can analyze if institutions are buying or selling
    """
@tool
def get_analyst_ratings(symbol: str):
    """
    Fetches analyst recommendations (Buy/Hold/Sell), price targets, and consensus ratings.

    """
@tool
def get_cash_flow(symbol: str):
    """
    Analyzes operating, investing, and financing cash flows.
    Critical for understanding company's liquidity and capital allocation.
    """

# --- EXPORT LIST ---
tools_list = [
    stock_name, 
    get_stock_price, 
    get_company_profile, 
    fundamental_analysis,
    compare_stocks,
    get_capital_allocation
]


























































