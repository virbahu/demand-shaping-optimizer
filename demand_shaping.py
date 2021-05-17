import numpy as np
from scipy.optimize import minimize
def demand_response(price, base_demand, elasticity, promo_lift=0):
    return base_demand*(price/base_demand*elasticity)**elasticity*(1+promo_lift)
def optimize_shape(products, target_capacity):
    n=len(products)
    def objective(x):
        prices=x[:n]; promos=x[n:]
        revenue=0; total_demand=0
        for i,p in enumerate(products):
            d=p["base_demand"]*(1-p["elasticity"]*(prices[i]-p["base_price"])/p["base_price"])*(1+promos[i]*p["promo_lift"])
            revenue+=d*prices[i]-promos[i]*p["promo_cost"]; total_demand+=d
        penalty=max(0,total_demand-target_capacity)*1000
        return -(revenue-penalty)
    x0=np.array([p["base_price"] for p in products]+[0.0]*n)
    bounds=[(p["min_price"],p["max_price"]) for p in products]+[(0,1)]*n
    res=minimize(objective,x0,bounds=bounds,method='SLSQP')
    return {products[i]["name"]:{"price":round(res.x[i],2),"promo":round(res.x[n+i],2)} for i in range(n)}
if __name__=="__main__":
    prods=[{"name":"SKU-A","base_price":50,"base_demand":200,"elasticity":1.5,"min_price":35,"max_price":65,"promo_lift":0.3,"promo_cost":2000},
           {"name":"SKU-B","base_price":30,"base_demand":400,"elasticity":2.0,"min_price":20,"max_price":40,"promo_lift":0.2,"promo_cost":1500}]
    print(optimize_shape(prods,500))
