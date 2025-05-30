# Unroutine! Dataset Source + ETL Logic

### Dataset Source
**Name:** Instacart Market Basket Analysis  
**Link:** [Kaggle Dataset](https://www.kaggle.com/datasets/hunter0007/ecommerce-dataset-for-predictive-marketing-2023)  
**Overview:** Contains over 2 million purchase records. Includes order timestamps, product info, and reordering behavior.  
**Relevance:** Enables prediction of when users deviate from staple buying habits based on timing.

### ETL Logic

**Extract:**
- Raw CSVs downloaded from Kaggle.
- Uploaded to Databricks FileStore.

**Transform:**
- Cleaned and joined order, product, and user data.
- Defined “staple items” for each user.
- Flagged orders as novelty if they included non-staple items.
- Extracted day-of-week and hour-of-day features.

**Load:**
- Saved transformed tables as Delta tables in Databricks for model training and visualization.
