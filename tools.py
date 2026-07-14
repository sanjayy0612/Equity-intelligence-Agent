# tool.py
from langchain_core.tools import tool
import market_data
from metric import Metric

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
        df = market_data.price_history(symbol)
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
        data = market_data.profile(symbol)
        if data is None:
            return f"Error: No profile found for {symbol}"
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
        cmp_profile = market_data.profile(symbol)
        if cmp_profile is None:
            return f"Error: No profile found for {symbol}"

        # 2. Fetch Metrics
        company_metrics = market_data.metrics(symbol)
        if company_metrics is None:
            return f"Error: No financial metrics found for {symbol}"

        # 3. Get sector for benchmarking
        sector = cmp_profile.get("sector", "Unknown")

        # 4. Each Metric normalizes, benchmarks, and renders itself.
        def metric(name, key):
            return Metric(name, company_metrics.get(key, "N/A"), sector).render()

        # 5. Construct the Enhanced Dictionary with Context
        data_dict = {
            "Company Name": cmp_profile.get("name", "N/A"),
            "Sector": sector,
            "Industry": cmp_profile.get("industry_category", "N/A"),
            "Country": cmp_profile.get("hq_country", "N/A"),
            "Description": cmp_profile.get("long_description", "N/A")[:500] + "...",

            # Enhanced metrics with industry context
            "Profit Margin": metric("Profit Margin", "profit_margin"),
            "Return on Equity (ROE)": metric("Return on Equity (ROE)", "return_on_equity"),
            "Debt to Equity": metric("Debt to Equity", "debt_to_equity"),
            "P/E Ratio": metric("P/E Ratio", "pe_ratio"),
            "Current Ratio": metric("Current Ratio", "current_ratio"),
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
                metrics = market_data.metrics(symbol)
                profile = market_data.profile(symbol)

                if metrics and profile:
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
        metrics = market_data.metrics(symbol)
        profile = market_data.profile(symbol)

        if metrics is None or profile is None:
            return f"Error: Unable to fetch capital allocation data for {symbol}"
        
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
    
# --- PLANNED TOOLS (not yet implemented; add to tools_list once built) ---
# - get_institutional_ownership(symbol): major holders (Vanguard, BlackRock) and
#   position changes, to gauge whether institutions are buying or selling.
# - get_analyst_ratings(symbol): Buy/Hold/Sell recommendations, price targets, consensus.
# - get_cash_flow(symbol): operating/investing/financing cash flows for liquidity
#   and capital-allocation analysis.

# --- EXPORT LIST ---
tools_list = [
    stock_name,
    get_stock_price,
    get_company_profile,
    fundamental_analysis,
    compare_stocks,
    get_capital_allocation
]
