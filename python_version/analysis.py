import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)

# Load data
data_path = "C:/Users/yezii/OneDrive/Documents/cpleads_2/sp25project/data/sp25.csv" #raw data

#Columns Titles
header = pd.read_csv(data_path, nrows=1).columns.tolist()

df = pd.read_csv("C:/Users/yezii/OneDrive/Documents/cpleads_2/sp25project/data/sp25.csv", skiprows=3, header=None)
df.columns = header

# Keep only completed surveys
df = df[df["w1status"] == "Completed"].copy()


# Select columns of interest
columns_of_interest = [
    "rid",
    "proc1", "proc2", "proc3", "proc4", "proc5",
    "w1commitnum", "w1commithrs", "w1commitoverw", "w1freetime",
    "w3tsq8", "w1tsq13", "w1tsq14",
    "gendermale", "genderfemal"
]
df = df[columns_of_interest].copy()

# Compute pro_sum
proc_cols = ["proc1", "proc2", "proc3", "proc4", "proc5"]
df["pro_sum"] = df[proc_cols].sum(axis=1) #pro_sum

# Create gender variable
df["gender"] = np.select(
    [
        df["gendermale"] == 1,
        df["genderfemal"] == 1
    ],
    ["Male", "Female"],
    default="Other"
)

# Keep only Male and Female
df = df[df["gender"].isin(["Male", "Female"])]

# List of variables for t-tests
variables = [
    "pro_sum",
    "w1commithrs",
    "w1commitnum",
    "w1freetime",
    "w1commitoverw",
    "w3tsq8",
    "w1tsq13",
    "w1tsq14"
]

# Descriptive statistics for all variables above
print("\nDescriptive statistics by gender:\n")
for var in variables:
    desc = df.groupby("gender")[var].describe()
    print(f"\nVariable: {var}\n", desc)

#Two-sample t-tests
print("\nTwo-sample t-tests (Male vs Female):\n")
for var in variables:
    male_values = df[df["gender"] == "Male"][var]
    female_values = df[df["gender"] == "Female"][var]
    t_stat, p_val = ttest_ind(male_values, female_values, equal_var=False)
    print(f"{var}: t = {t_stat:.3f}, p = {p_val:.4f}")

#Boxplots for each variable 
for var in variables:
    plt.figure(figsize=(6,4))
    sns.boxplot(data=df, x="gender", y=var, palette={"Male":"#92c5de", "Female":"#f4a582"})
    sns.stripplot(data=df, x="gender", y=var, color="black", alpha=0.3)
    plt.title(f"{var} by Gender")
    plt.xlabel("Gender")
    plt.ylabel(var)
    plt.tight_layout()
    plt.show()

# Save processed data
df.to_csv("UROP_data_full.csv", index=False)

