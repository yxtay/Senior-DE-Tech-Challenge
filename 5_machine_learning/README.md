# Senior Data Enginer Tech Challenge
---
## Section 5: Machine Learning
Using the dataset from https://archive.ics.uci.edu/ml/datasets/Car+Evaluation, create a machine learning model to predict the buying price given the following parameters:

Maintenance = High <br>
Number of doors = 4 <br>
Lug Boot Size = Big <br>
Safety = High <br>
Class Value = Good <br>

### Instructions

Run with docker compose
```
docker compose up --build
```

The model prediction of `low` buying price is printed out at the end of the script.

For a better model, I would have considered implementing early stopping with a validation dataset and hyperparameter tuning.
However, given such a small dataset, it is difficult to implement properly.

If time permits, I would also perform some model analysis such as evaluating loss, error rates, feature importance, etc.

### Clean up

```
docker compose down --volumes --remove-orphans --rmi all
```
