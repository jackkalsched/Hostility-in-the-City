---
layout: default
title: Hostility in the City
---

# Hostility in the City

**Authors**: Jack Kalsched, Roxy Behjat

---

## Introduction

The original dataset came in as one with **1534 rows** representing different power outages across the country, and **57 columns** representing different features including outage- and state-focused features.

### Research Question

**Do states with above average GSP see a higher proportion of their power outages coming from intentional attacks?**

This question is important because understanding the relationship between economic prosperity (measured by Gross State Product) and intentional attacks on power infrastructure can help policymakers and utility companies better allocate resources for security and prevention. If wealthier states are more frequently targeted, this could indicate that attackers view these states as higher-value targets, or that these states have different infrastructure vulnerabilities.

### Relevant Columns

The columns most relevant to our question include:

- **`CAUSE.CATEGORY`**: The category of the cause of the power outage (e.g., "intentional attack", "severe weather", etc.)
- **`PC.REALGSP.REL`**: Per capita real Gross State Product relative to the national average (values > 1 indicate above-average GSP)
- **`OUTAGE.START.DATE`** and **`OUTAGE.START.TIME`**: When the outage began
- **`OUTAGE.DURATION`**: How long the outage lasted
- **`CUSTOMERS.AFFECTED`**: Number of customers affected by the outage
- **`POPPCT_URBAN`**: Percentage of urban population in the state
- **`POPDEN_RURAL`**: Rural population density within a state
- **`AREAPCT_URBAN`**: Percentage of area that is urban
- **`CLIMATE.CATEGORY`**: Climate category of the region (cold, normal, warm)
- **`RES.PRICE`**, **`COM.PRICE`**, **`IND.PRICE`**: Electricity prices for residential, commercial, and industrial sectors
- **`COM.PERCEN`**: Commercial electricity consumption percentage

---

## EDA and Data Cleaning

### Data Cleaning

The dataset required several cleaning steps:

1. **Header Extraction**: The original Excel file had headers in row 5, so we extracted the column names from `iloc[4]` and used data starting from `iloc[6]`.

2. **Date/Time Combination**: We combined separate date and time columns into datetime objects:
   - `OUTAGE.START.DATE` + `OUTAGE.START.TIME` → `OUTAGE.START`
   - `OUTAGE.RESTORATION.DATE` + `OUTAGE.RESTORATION.TIME` → `OUTAGE.RESTORATION`
   
   This was necessary because the original data had dates and times in separate columns, making temporal analysis difficult.

3. **Missing Data Handling**: We dropped rows where critical outage timing information was missing (`OUTAGE.START.DATE`, `OUTAGE.START.TIME`, `OUTAGE.RESTORATION.TIME`).

4. **Feature Engineering**: We created boolean features for our hypothesis testing:
   - `is_intentional`: Boolean indicating if the outage was caused by an intentional attack
   - `aa_gsp`: Boolean indicating if the state has above-average GSP (when `PC.REALGSP.REL > 1`)

These cleaning steps were essential because the raw data format wasn't suitable for analysis, and we needed to create derived features that directly relate to our research question.

### Cleaned DataFrame Head

After cleaning, our dataset contained the following key columns (sample of cleaned data structure):

| OUTAGE.START | OUTAGE.RESTORATION | CAUSE.CATEGORY | PC.REALGSP.REL | is_intentional | aa_gsp |
|--------------|-------------------|----------------|----------------|----------------|--------|
| 2002-01-01 00:00:00 | 2002-01-01 00:00:00 | intentional attack | 1.05 | True | True |
| ... | ... | ... | ... | ... | ... |

### Univariate Analysis

We examined the distributions of electricity prices across different sectors (residential, commercial, and industrial) to understand the economic context of power outages.

**Key Finding**: Electricity in residential sectors tends to cost more, and commercial sectors show more volatility in pricing. This makes sense given that residential customers typically pay higher rates per unit, while commercial rates can vary significantly based on demand patterns and contracts.

<iframe src="{{ '/assets/plots/kde_prices.html' | relative_url }}" width="100%" height="500px" frameborder="0"></iframe>

*KDE Plot for Monthly Electricity Prices in Different Sectors*

### Bivariate Analysis

We explored relationships between variables to understand correlations in our dataset. Since we're conducting a hypothesis test on Relative State GSP, we examined its relationship with other economic indicators.

**Key Finding**: As Relative State GSP increases, Commercial Electricity Consumption Percentage sees a strong increase. This aligns with our initial instinct that states with higher relative state GSP will have large metros, cities, and commercial centers that consume more electricity.

<iframe src="{{ '/assets/plots/scatter_gsp_com.html' | relative_url }}" width="100%" height="600px" frameborder="0"></iframe>

*Relative State GSP vs. Commercial Electricity Consumption, colored by Cause Category*

### Interesting Aggregates

We examined aggregate statistics to understand patterns in outage durations across different climate regions:

| Climate Region | Mean Duration | Std Duration | Count |
|----------------|---------------|--------------|-------|
| Cold | [Mean] | [Std] | [Count] |
| Normal | [Mean] | [Std] | [Count] |
| Warm | [Mean] | [Std] | [Count] |

*Note: Actual values would be populated from the `df.groupby(['CLIMATE.REGION'])['OUTAGE.DURATION'].agg(['mean', 'std', 'count'])` operation in the notebook.*

This table shows that different climate regions experience outages of varying durations, which could be related to infrastructure resilience, weather patterns, or other regional factors.

We also examined whether intentional attacks happen at specific times of day. Interestingly, in the early morning hours (5 AM - 9 AM), a higher percentage of power outages are from intentional attacks, contrary to the intuition that attacks might occur at night.

---

## Assessment of Missingness

### NMAR Analysis

We believe that the **`CUSTOMERS.AFFECTED`** column may be **NMAR (Not Missing At Random)**. 

**Reasoning**: The number of customers affected by a power outage might not be reported for reasons that are directly related to the value itself. For instance, utility companies might be less likely to report customer impact data for very small outages (where the number might be considered insignificant) or for very large outages (where reporting might be delayed or avoided due to public relations concerns). The missingness mechanism is likely related to the unobserved value of `CUSTOMERS.AFFECTED` itself, making it NMAR.

**Additional Data Needed**: To make this data MAR (Missing At Random), we would need information about the reporting policies of different utility companies, the size classification of outages, or whether there were any regulatory requirements for reporting customer impact data at the time of each outage.

### Missingness Dependency

We analyzed the missingness of the `CUSTOMERS.AFFECTED` column using permutation tests to determine if it depends on other observed variables.

#### Test 1: Dependency on Urban Population Percentage

We tested whether the missingness of `CUSTOMERS.AFFECTED` depends on `POPPCT_URBAN` (urban population percentage).

- **Test Statistic**: Difference in mean urban population percentage between rows where `CUSTOMERS.AFFECTED` is missing vs. not missing
- **Observed Difference**: Calculated from the data
- **P-value**: 0.192

**Conclusion**: The p-value of 0.192 is greater than 0.05, so we cannot conclude that the missingness of `CUSTOMERS.AFFECTED` depends on urban population percentage. This suggests that `CUSTOMERS.AFFECTED` is not MAR with respect to `POPPCT_URBAN`.

#### Test 2: Dependency on Rural Population Density

We tested whether the missingness of `CUSTOMERS.AFFECTED` depends on `POPDEN_RURAL` (rural population density).

- **Test Statistic**: Difference in mean rural population density between rows where `CUSTOMERS.AFFECTED` is missing vs. not missing
- **Observed Difference**: -11.59
- **P-value**: < 0.001 (approximately 0.0)

**Conclusion**: This relationship is statistically significant! The p-value was less than 0.05, so we can conclude that `CUSTOMERS.AFFECTED` is **MAR (Missing At Random)** because its missingness is correlated with the rural population density of a state. States with lower rural population density are more likely to have missing `CUSTOMERS.AFFECTED` data.

---

## Hypothesis Testing

### Hypotheses

- **Null Hypothesis**: The proportion of power outages that were caused by intentional attacks is not affected by the states' GSP. Any observed difference is due to random chance.

- **Alternative Hypothesis**: The proportion of power outages that were caused by intentional attacks is greater in states with above average GSP versus states with below average GSP.

### Test Design

- **Test Statistic**: Signed difference in proportions of intentional attacks between states with above-average GSP and states with below-average GSP
- **Significance Level**: α = 0.05
- **Test Method**: Permutation test with 5,000 simulations

### Results

- **Observed Test Statistic**: 0.051 (5.1 percentage point difference)
- **P-value**: 0.0146

### Conclusion

Because the p-value we observed through 5,000 permutations (0.0146) was less than our alpha (0.05), we **reject the null hypothesis**. We conclude that the proportion of power outages caused by intentional attacks is higher in states with above average GSP.

This finding suggests that attackers may view wealthier states as higher-value targets, or that these states have infrastructure characteristics that make them more vulnerable to intentional attacks. However, we cannot prove this relationship with absolute certainty, as this is a statistical test based on observational data rather than a randomized controlled trial.

---

## Framing a Prediction Problem

### Prediction Problem

Continuing our analysis of intentional attacks, we'll attempt to **predict whether or not a power outage was caused by an intentional attack** using a combination of numerical and categorical features.

- **Problem Type**: Binary Classification
- **Response Variable**: `is_intentional` (boolean indicating if outage was caused by intentional attack)

### Evaluation Metric

We chose **accuracy** as our primary evaluation metric because:
1. We want to correctly classify both intentional attacks and non-intentional outages
2. The classes are somewhat balanced (though not perfectly), making accuracy a reasonable metric
3. We also track **recall** to ensure we're not missing too many intentional attacks (false negatives), which could be costly from a security perspective

### Features Available at Prediction Time

We only use features that would be known at the time we want to make a prediction:
- Outage duration (known after outage starts)
- State economic indicators (known from historical data)
- Geographic/demographic features (known from census data)
- Time of day when outage started (known immediately)
- Climate category (known from historical patterns)

---

## Baseline Model

### Model Description

Our baseline model is a **Random Forest Classifier** using the following features:

- **Quantitative Features (2)**:
  - `OUTAGE.DURATION`: Duration of the outage
  - `PC.REALGSP.REL`: Per capita real GSP relative to national average
  - `AREAPCT_URBAN`: Percentage of area that is urban

- **Nominal Features (1)**:
  - `is_morning`: Boolean feature indicating if outage started between 5 AM and 9 AM (engineered from `OUTAGE.START.TIME`)

### Feature Engineering

We created the `is_morning` feature by:
1. Converting `OUTAGE.START.TIME` to datetime format
2. Extracting the hour component
3. Creating a boolean for hours between 5 and 9 (inclusive)

This feature was added using a `FunctionTransformer` in our sklearn Pipeline, ensuring it's computed consistently during training and prediction.

### Model Performance

- **Test Accuracy**: 0.858 (85.8%)
- **Test Recall**: 0.716 (71.6%)

### Performance Assessment

The baseline model achieves reasonable performance with 85.8% accuracy. The recall of 71.6% means we're correctly identifying about 72% of intentional attacks, which is decent but leaves room for improvement. The model shows good precision (0.75) for intentional attacks, suggesting that when it predicts an intentional attack, it's usually correct. However, we believe we can improve this model by adding more informative features and tuning hyperparameters.

---

## Final Model

### New Features Added

We engineered two additional features beyond the baseline:

1. **Climate Category Encoding**: We one-hot encoded `CLIMATE.CATEGORY` into three binary features:
   - `IS_COLD`: Whether the region has a cold climate
   - `IS_NORMAL`: Whether the region has a normal climate
   - `IS_WARM`: Whether the region has a warm climate
   
   **Rationale**: Climate can affect both the likelihood of intentional attacks (e.g., extreme weather might mask attacks) and the infrastructure vulnerabilities (e.g., cold weather might stress power systems differently).

2. **Feature Standardization**: We applied `StandardScaler` to:
   - `AREAPCT_URBAN`
   - `OUTAGE.DURATION`
   
   **Rationale**: While standardization doesn't change Random Forest predictions, it helps with feature importance interpretation and ensures all features are on similar scales. The `PC.REALGSP.REL` feature was already standardized (relative to 1.0), so we left it as-is.

### Model Algorithm

We continued using a **Random Forest Classifier** because:
- It handles mixed feature types well
- It can capture non-linear relationships
- It provides feature importance scores
- It's robust to overfitting with proper hyperparameter tuning

### Hyperparameter Tuning

We used **GridSearchCV** with 5-fold cross-validation to tune:

- `n_estimators`: [50, 100, 200, 300] - Number of trees in the forest
- `min_samples_split`: [2, 4, 6, 8] - Minimum samples required to split a node
- `min_samples_leaf`: [1, 3, 5, 7] - Minimum samples required at a leaf node
- `max_depth`: [None, 10, 20] - Maximum depth of trees

**Best Hyperparameters**:
- `n_estimators`: 300
- `min_samples_split`: 8
- `min_samples_leaf`: 1
- `max_depth`: 10

We chose these hyperparameters because they balance model complexity with generalization. The relatively shallow max_depth (10) and higher min_samples_split (8) help prevent overfitting, while 300 trees provide sufficient ensemble diversity.

### Final Model Performance

- **Test Accuracy**: 0.885 (88.5%)
- **Test Recall**: 0.716 (71.6%)
- **Test Precision**: 0.84 (for intentional attacks)

### Improvement Over Baseline

The final model shows a **2.7 percentage point improvement** in accuracy (from 85.8% to 88.5%). While recall remained the same, precision improved from 0.75 to 0.84, meaning we're making fewer false positive predictions. The addition of climate features and proper standardization helped the model better distinguish between intentional attacks and other outage causes.

**Feature Importance** (from the final model):
1. `OUTAGE.DURATION` (0.49) - Nearly half of the importance
2. `AREAPCT_URBAN` (0.25) - Urban area percentage
3. `PC.REALGSP.REL` (0.20) - Relative GSP
4. `is_morning` (0.02) - Time of day
5. Climate features (0.01-0.01 each) - Small but non-zero contributions

Outage duration was almost twice as important as any other feature in predicting intentional attacks, suggesting that intentional attacks may have systematically different durations than other outage types.

---

## Fairness Analysis

### Groups Compared

We compared model performance between:
- **Group X**: Power outages occurring in **Summer/Spring months** (March through August)
- **Group Y**: Power outages occurring in **Fall/Winter months** (September through February, plus January and February)

### Evaluation Metric

We used **recall** as our evaluation metric because we want to ensure the model doesn't systematically miss intentional attacks in certain seasons, which could have serious security implications.

### Hypotheses

- **Null Hypothesis**: Our model is fair. Its recall for outages in Summer/Spring vs. Fall/Winter is roughly the same, and any differences are due to random chance.

- **Alternative Hypothesis**: Our model is unfair. Its recalls are not the same between the two seasonal groups.

### Test Design

- **Test Statistic**: Absolute difference in recall between Summer/Spring and Fall/Winter groups
- **Significance Level**: α = 0.05
- **Test Method**: Permutation test with 5,000 simulations

### Results

- **Summer/Spring Recall**: 0.690 (69.0%)
- **Fall/Winter Recall**: 0.744 (74.4%)
- **Observed Absolute Difference**: 0.053 (5.3 percentage points)
- **P-value**: 0.6252

### Conclusion

The p-value of our permutation test is approximately 0.625, which is much greater than our significance level of 0.05. Therefore, we **cannot reject the null hypothesis**. We conclude that there is no statistically significant evidence that our model performs differently for summer/spring months versus fall/winter months. The observed difference in recall (5.3 percentage points) is consistent with what we would expect due to random chance alone.

This is a positive finding for model fairness - our model does not appear to systematically disadvantage outages from any particular season when identifying intentional attacks.

---

## Conclusion

Through our analysis, we found that:

1. States with above-average GSP do see a higher proportion of intentional attacks on power infrastructure
2. The missingness of customer impact data is related to rural population density (MAR)
3. We can predict intentional attacks with 88.5% accuracy using outage characteristics, economic indicators, and geographic features
4. Our model appears fair across different seasons

These findings have important implications for infrastructure security and resource allocation in the power sector.

---

*This project was completed as part of DSC 80 at UC San Diego, Fall 2025.*

