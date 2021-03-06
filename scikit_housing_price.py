# -*- coding: utf-8 -*-
"""scikit_housing_price.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w-NtlfieX9iynpBkwyfdMi1SoBVZA50d
"""

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from itertools import cycle, islice
from pandas.plotting import parallel_coordinates

from google.colab import auth
auth.authenticate_user()

from google.colab import files
uploaded = files.upload()

import io
data = pd.read_csv(io.StringIO(uploaded['housing.csv'].decode('utf-8')))

data.info()

data.head()

data.describe().transpose()

features = ['longitude', 'latitude', 'median_income']
select_df = data[features]
select_df.columns

X = StandardScaler().fit_transform(select_df)
X[:5]

kmeans = KMeans(n_clusters=6) # number of clusters must be specified
model = kmeans.fit(X)
model

centers = model.cluster_centers_
centers[:5]

centers.shape

# Function that creates a DataFrame with a column for Cluster Number
def pd_centers(featuresUsed, centers):
	colNames = list(featuresUsed)
	colNames.append('prediction')

	# Zip with a column called 'prediction' (index)
	Z = [np.append(A, index) for index, A in enumerate(centers)]

	# Convert to pandas data frame for plotting
	P = pd.DataFrame(Z, columns=colNames)
	P['prediction'] = P['prediction'].astype(int)
	return P

# Function that creates Parallel Plots
def parallel_plot(data):
	my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k']), None, len(data)))
	plt.figure(figsize=(15,8)).gca().axes.set_ylim([-3,+3])
	parallel_coordinates(data, 'prediction', color = my_colors, marker='o')



P = pd_centers(features, centers)

P

parallel_plot(P)

# Create cluster label
data['econ_region'] = kmeans.fit_predict(X)
data['econ_region'] = data['econ_region'].astype("category")
data.head()

sns.set_style('whitegrid')
sns.relplot(x='longitude', y='latitude', hue='econ_region', data=data, kind='scatter');

median_attributes = ['econ_region', 'median_house_value', 'median_income', 'housing_median_age']
income_house = data[median_attributes]
income_house.groupby(['econ_region']).describe()