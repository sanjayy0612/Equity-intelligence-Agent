# metric.py
# A Metric owns the whole pipeline for one financial figure: normalize the raw
# value, guard the missing cases, compare it against the sector benchmark, and
# render the "18.4% - Within Industry Range" string. Parsing, judging, and
# formatting live together here instead of being split between the tools and a
# pure helper — so the behavior that actually breaks has one home and one test.

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

# Each metric the analysis surfaces: which benchmark key it maps to, and whether
# its raw value is a fraction that should render as a percentage (x100).
_METRIC_SPECS = {
    "Profit Margin":          {"key": "profit_margin",  "percent": True},
    "Return on Equity (ROE)": {"key": "roe",            "percent": True},
    "Debt to Equity":         {"key": "debt_to_equity", "percent": False},
    "P/E Ratio":              {"key": "pe_ratio",       "percent": False},
    "Current Ratio":          {"key": "current_ratio",  "percent": False},
}


class Metric:
    """One financial figure, aware of its own name, sector, and how to judge itself."""

    def __init__(self, name: str, raw_value, sector: str):
        self.name = name
        self.raw_value = raw_value
        self.sector = sector
        self._spec = _METRIC_SPECS.get(name)

    @property
    def _is_percent(self) -> bool:
        return bool(self._spec and self._spec["percent"])

    @property
    def value(self):
        """Display value: percent-scaled where appropriate, or 'N/A' if missing."""
        raw = self.raw_value
        if raw is None or raw == "N/A" or not isinstance(raw, (int, float)):
            return "N/A"
        return round(raw * 100, 2) if self._is_percent else raw

    def assessment(self) -> str:
        """Where this value sits relative to the sector benchmark."""
        val = self.value
        if val == "N/A":
            return "N/A"
        if not self._spec or self.sector not in INDUSTRY_BENCHMARKS:
            return "No benchmark available"

        b = INDUSTRY_BENCHMARKS[self.sector][self._spec["key"]]
        unit = "%" if self._is_percent else ""
        try:
            v = float(val)
        except (ValueError, TypeError):
            return "Unable to compare"

        if v < b["low"]:
            return f"Below Industry Range ({b['low']}-{b['high']}{unit})"
        elif v < b["avg"]:
            return f"Near Industry Low (Avg: {b['avg']}{unit})"
        elif v <= b["high"]:
            return f"Within Industry Range (Avg: {b['avg']}{unit})"
        else:
            return f"Above Industry Average (Avg: {b['avg']}{unit})"

    def render(self) -> str:
        """Full '18.4% - Within Industry Range' string used in tool output."""
        unit = "%" if self._is_percent else ""
        return f"{self.value}{unit} - {self.assessment()}"
