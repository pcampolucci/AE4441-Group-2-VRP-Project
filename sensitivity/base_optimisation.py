import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import seaborn as sns

print(sns.__version__)

# first iteration of bases vs objective
n_bases = np.arange(1,9,1)
bases_lot = np.linspace(1,8,100)
obj_lst = [529, 488, 445, 411, 376, 374, 376, 375]
bases_used = np.array([100, 100, 67, 75, 100, 100, 71, 75])
bases_existing = np.array([1, 2, 3, 4, 5, 6, 7, 8])

# constant
base_fix_cost = 40
base_operation_cost = 60
base_expense = base_fix_cost*bases_existing + base_operation_cost*bases_used*bases_existing/100

# make polynomial interpolation for obj
model_obj = make_pipeline(PolynomialFeatures(6), Ridge())
model_obj.fit(n_bases[:, np.newaxis], obj_lst)
obj_poly = model_obj.predict(bases_lot[:, np.newaxis])

sns.despine()
sns.color_palette("rocket_r")
plt.scatter(n_bases, obj_lst, color="darkred")
plt.plot(bases_lot, obj_poly, color="gold")
plt.xlabel("# Bases")
plt.ylabel(f"Cost of operation [$]")
plt.title("Operational Cost Convergence vs Base Amount")
plt.grid(color='gray', linestyle=':')
plt.savefig("cost_base.png")

plt.show()
