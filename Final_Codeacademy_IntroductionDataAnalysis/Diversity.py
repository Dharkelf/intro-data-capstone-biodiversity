"""
Codeacademy.com
Introduction to Data Analysis

Reviewable Project -
Capstone Option 2: Biodiversity for the National Parks

Autor: Andy (Andreas Theil)
"""

#################################
#imports

import codecademylib
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

##################################
#
##################################

species = pd.read_csv('species_info.csv')

#Species analysis
species_count = len(species)
species_type = species.category.unique()

#Conservation Status analysis
conservation_statuses = species.conservation_status.unique()
conservation_counts = species.groupby('conservation_status').scientific_name.count().reset_index()

#Fill NaN
species.fillna('No Intervention', inplace=True)
conservation_counts_fixed = species.groupby('conservation_status').scientific_name.count().reset_index()

#Conservation stati and species
protection_counts = species.groupby('conservation_status').scientific_name.count().reset_index()\
    .sort_values(by='scientific_name')

#plot protection_counts
plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts)),protection_counts.scientific_name.values)
ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
labels = [e.get_text() for e in ax.get_xticklabels()]
print ax.get_title()
plt.show()

#count categories
species['is_protected'] = species.conservation_status != 'No Intervention'
category_counts = species.groupby(['category', 'is_protected']).scientific_name.count().reset_index()

#pivot chart
category_pivot = category_counts.pivot(columns='is_protected', index='category',\
                                       values='scientific_name').reset_index()
category_pivot.columns = ['category', 'not_protected', 'protected']
category_pivot['percent_protected'] = category_pivot.protected / (
        category_pivot.protected + category_pivot.not_protected)

# mammals vs. birds
contingency = [[30, 146], [75, 413]]
a, pval, c, d = chi2_contingency(contingency)

# reptile vs. mammals
contingency2 = [[5, 73], [30, 146]]
a, pval_reptile_mammal, c, d = chi2_contingency(contingency2)


##################################
#Foot and Mouth Reduction Effort
##################################

species = pd.read_csv('species_info.csv')

species.fillna('No Intervention', inplace = True)
species['is_protected'] = species.conservation_status != 'No Intervention'
observations=pd.read_csv('observations.csv')

species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
species_is_sheep=species[species['is_sheep']==True]
sheep_species=species[(species['is_sheep']==True)&(species['category']=="Mammal")]

sheep_observations = observations.merge(sheep_species)

obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()

plt.figure(figsize=(16, 4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park)),obs_by_park.observations.values)
ax.set_xticks(range(len(obs_by_park)))
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
plt.show()

#Sample size

baseline=15
minimum_detectable_effect=100 * 0.05 / 0.15
print minimum_detectable_effect
sample_size_per_variant=510

yellowstone_weeks_observing= 1.0*510 / 507
bryce_weeks_observing = 1.0*510 / 250