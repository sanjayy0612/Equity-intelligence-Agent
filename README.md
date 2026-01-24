# 📈 Equity-intelligence-Agent

> A modular financial intelligence agent that performs grounded analysis using deterministic tools, supports extensible reasoning states, and is designed to scale across models and interfaces.

![Python](https://img.shields.io/badge/Python-100%25-blue)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-green)
![OpenBB](https://img.shields.io/badge/OpenBB-Integration-orange)

## 🎯 Overview

**EQ-Agent** is an AI-powered financial analyst that provides real-time stock analysis, fundamental metrics, and industry-contextualized insights. Built with LangChain and OpenBB, it combines the power of large language models with reliable financial data sources.

## ✨ Features

- **🔍 Real-time Stock Data**: Fetch current and historical stock prices
- **📊 Fundamental Analysis**: Deep dive into company financials with industry benchmarks
- **🏭 Industry Context**: Compare metrics against sector-specific standards
- **⚖️ Comparative Analysis**: Side-by-side comparison of multiple stocks
- **💰 Capital Allocation Insights**: Understand buyback strategies and ROE drivers
- **🎯 Smart Symbol Resolution**: Convert company names to ticker symbols automatically

## 🛠️ Tools Available

| Tool | Description |
|------|-------------|
| `stock_name` | Converts company names to ticker symbols |
| `get_stock_price` | Fetches historical price data (last 5 days) |
| `get_company_profile` | Retrieves company description and overview |
| `fundamental_analysis` | Comprehensive financial metrics with industry benchmarks |
| `compare_stocks` | Multi-stock comparison with ROE-based ranking |
| `get_capital_allocation` | Analyzes buyback activity and capital strategy |

## 📸 Screenshots

### Agent in Action
![EQ-Agent Analysis](path/to/screenshot2.png)
*Real-time fundamental analysis with industry-contextualized insights*

### Repository Structure
![Repository Overview](path/to/screenshot1.png)
*Clean, modular Python architecture*

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
pip install langchain langchain-core openbb
```

### Installation

```bash
# Clone the repository
git clone https://github.com/sanjayy0612/Equity-intelligence-Agent.git
cd Equity-intelligence-Agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (if needed)
cp .env.example .env
```

### Usage

```python
from tools import fundamental_analysis, compare_stocks

# Analyze a single stock
result = fundamental_analysis("AAPL")
print(result)

# Compare multiple stocks
comparison = compare_stocks("TSLA,F,GM")
print(comparison)
```

## 📋 Industry Benchmarks

The agent includes pre-configured benchmarks for major sectors:

- **Technology**: High margins (20% avg), high P/E (30 avg)
- **Automotive**: Moderate margins (6% avg), lower P/E (15 avg)
- **Healthcare**: Strong margins (15% avg), moderate P/E (22 avg)
- **Financial Services**: High margins (25% avg), leverage-heavy
- **Energy**: Variable margins (8% avg), cyclical patterns
- **Consumer Cyclical**: Tight margins (5% avg), inventory-intensive

## 🏗️ Architecture

```
Equity-intelligence-Agent/
│
├── ai_engine.py          # LangChain agent orchestration
├── app.py                # User interface / API layer
├── context_schema.py     # Data models and schemas
├── exa.py                # Example usage and demos
├── main.py               # Entry point
├── states.py             # Agent reasoning states
├── tools.py              # Financial analysis tools
└── README.md             # This file
```

## 🧠 How It Works

1. **Query Processing**: User asks a financial question
2. **Tool Selection**: Agent intelligently selects appropriate tools
3. **Data Retrieval**: OpenBB fetches real-time financial data
4. **Contextualization**: Metrics are compared against industry benchmarks
5. **Response Generation**: LLM synthesizes insights in natural language

## 🎓 Example Queries

```
✅ "Analyze AMD's profitability"
✅ "Compare Tesla, Ford, and GM"
✅ "What's Apple's current ROE and how does it compare to the tech industry?"
✅ "Why is Tesla's ROE so high?"
✅ "Get me the latest stock price for Microsoft"
```

## 🔧 Configuration

### Adding New Companies

Edit the `COMPANY_TICKERS` dictionary in `tools.py`:

```python
COMPANY_TICKERS = {
    "your_company": "TICK",
    # ... existing entries
}
```

### Customizing Benchmarks

Modify `INDUSTRY_BENCHMARKS` in `tools.py` to adjust sector standards.

## 📊 Supported Metrics

- **Profitability**: Profit Margin, ROE, EPS
- **Valuation**: P/E Ratio, Price-to-Book
- **Leverage**: Debt-to-Equity
- **Liquidity**: Current Ratio
- **Growth**: Revenue trends, margin expansion

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenBB** for providing robust financial data APIs
- **LangChain** for the agent orchestration framework
- **Yahoo Finance** for real-time market data

## 📧 Contact

**Sanjay** - [@sanjayy0612](https://github.com/sanjayy0612)

Project Link: [https://github.com/sanjayy0612/Equity-intelligence-Agent](https://github.com/sanjayy0612/Equity-intelligence-Agent)

---

⭐ Star this repo if you find it helpful!
