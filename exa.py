from openbb import obb



met = obb.equity.fundamental.metrics("AAPL").to_dict()
#print(estimates)
data_dict = {}

data_dict["P/E Ratio"] = met["pe_ratio"]
data_dict["Forward P/E"] = met["foward_pe"]
data_dict["EPS"] = met["eps"]
data_dict["Return on Equity"] = met["return_on_equity"]
data_dict["Profit Margin"] = met["profit_margin"]
data_dict["Debt to Equity"] = met["debt_to_equity"]
data_dict["Price to Book"] = met["price_to_book"]
data_dict["Current Ratio"] = met["current_ratio"]


print(data_dict)

cmp_profile=obb.equity.profile("AAPL").to_dict()


data_dict["Company_name"] = cmp_profile["name"]
data_dict["Sector"] = cmp_profile["sector"]
data_dict["Type_of_Industry"] = cmp_profile["industry_category"]
data_dict["Country"] = cmp_profile["hq_country"]
data_dict["Description"] = cmp_profile["long_description"]

print(data_dict)
