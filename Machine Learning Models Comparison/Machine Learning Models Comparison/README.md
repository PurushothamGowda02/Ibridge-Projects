# Machine Learning Models Comparison Project (BCA Final Year)

This project compares multiple machine learning classification models on a dataset and identifies the best-performing model based on evaluation metrics.

## Features
- **Interactive Streamlit Dashboard** with real-time progress tracking
- Supports custom CSV dataset input or built-in datasets
- Automatic preprocessing:
  - Numeric features: standard scaling with median imputation
  - Categorical features: one-hot encoding with most frequent imputation
- Compares 5 optimized classification models:
  - Logistic Regression
  - Decision Tree
  - Random Forest (100 trees, parallel processing)
  - SVM (RBF kernel)
  - KNN (parallel processing)
- Comprehensive evaluation metrics:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - Cross-validation mean accuracy and standard deviation
- Smart validation:
  - Automatic detection of problematic datasets
  - Handles imbalanced classes gracefully
  - Skips cross-validation when not feasible
  - Works with any column selection (with warnings)
- Saves outputs:
  - CSV results table
  - Best model file (`.pkl`)
  - Accuracy comparison graph
  - Confusion matrix for best model

## Project Structure

```text
Machine Learning Models Comparison/
├── data/
│   ├── telco_churn.csv          # Built-in demo dataset
│   └── titanic.csv               # Additional demo dataset
├── outputs/                      # Generated results
│   ├── model_comparison_*.csv
│   ├── best_model_*.pkl
│   ├── accuracy_comparison.png
│   └── best_model_confusion_matrix.png
├── src/
│   └── compare_models.py         # Core ML logic
├── app.py                        # Streamlit web interface
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── REPORT_TEMPLATE.md           # Project report template
```

## Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**

2. **Create virtual environment** (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies**:

```powershell
pip install -r requirements.txt
```

## Usage

### Option 1: Streamlit Web Interface (Recommended)

Run the interactive dashboard:

```powershell
python -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**Features:**
- Upload your own CSV or use built-in Telco Churn dataset
- Select target column from dropdown
- Choose columns to drop (IDs, irrelevant features)
- Adjust test size, CV folds, and random state
- Real-time progress tracking during training
- Interactive visualizations
- Download results and trained model

**Tips:**
- Select a categorical column with repeated values as target (e.g., "Churn", "Status")
- Avoid selecting ID columns (customerID, PassengerId) as target
- Drop ID columns before training for better results
- For large datasets or many classes, training may take 1-3 minutes

### Option 2: Command Line Interface

#### Quick run with built-in demo dataset:

```powershell
python src\compare_models.py
```

#### Run with your own dataset:

```powershell
python src\compare_models.py --data data\your_dataset.csv --target target_column_name
```

#### Advanced options:

```powershell
python src\compare_models.py --data data\telco_churn.csv --target Churn --drop-cols customerID --test-size 0.25 --cv 10 --random-state 42
```

**Available arguments:**
- `--data`: Path to CSV dataset file
- `--target`: Target column name (required for CSV)
- `--drop-cols`: Comma-separated columns to drop (e.g., "customerID,Name")
- `--test-size`: Test split ratio (default: 0.2)
- `--random-state`: Random seed for reproducibility (default: 42)
- `--cv`: Number of cross-validation folds (default: 5)
- `--outdir`: Output directory (default: "outputs")

## Outputs

All results are saved in the `outputs/` directory:

- **`model_comparison_<dataset_name>.csv`** - Detailed comparison table with all metrics
- **`best_model_<dataset_name>.pkl`** - Trained best model (can be loaded with joblib)
- **`accuracy_comparison.png`** - Bar chart comparing model accuracies
- **`best_model_confusion_matrix.png`** - Confusion matrix visualization

## Model Details

### Optimized Hyperparameters

- **Logistic Regression**: max_iter=300, solver='lbfgs'
- **Decision Tree**: max_depth=10 (prevents overfitting)
- **Random Forest**: 100 estimators, max_depth=10, parallel processing
- **SVM**: RBF kernel, probability=True, cache_size=500MB
- **KNN**: 5 neighbors, parallel processing

### Performance Optimizations

- Parallel processing enabled (n_jobs=-1) for Random Forest and KNN
- Reduced tree depth to prevent overfitting and speed up training
- Smart cross-validation: automatically skips when not feasible
- Handles datasets with many classes gracefully

## Example Datasets

### Included Datasets

1. **Telco Churn** (`data/telco_churn.csv`)
   - Target: `Churn` (Yes/No)
   - Features: Customer demographics, services, billing
   - Samples: 7043
   - Use case: Predict customer churn

2. **Titanic** (`data/titanic.csv`)
   - Target: `Survived` (0/1)
   - Features: Passenger class, age, fare, etc.
   - Use case: Predict survival

### Suggested External Datasets

- Iris (classification)
- Breast Cancer Wisconsin (classification)
- Wine Quality (classification)
- Student Performance (classification version)

## Troubleshooting

### Common Issues

**Issue**: "Every row has a unique value in target column"
- **Solution**: You selected an ID column. Choose a categorical column with repeated values.

**Issue**: "Training takes too long"
- **Solution**: 
  - Reduce CV folds (try 3 instead of 5)
  - Use smaller test size (0.3 instead of 0.2)
  - Ensure you're not using an ID column as target

**Issue**: "Cross-validation skipped"
- **Reason**: Dataset has too many unique classes or too few samples per class
- **Impact**: CV metrics show "N/A" but training still works

**Issue**: "Stratified split failed"
- **Reason**: Some classes have very few samples
- **Solution**: App automatically falls back to non-stratified split

## Viva/Presentation Points

### Technical Concepts

1. **Why preprocessing is important**
   - Scaling ensures features are on same scale
   - Encoding converts categorical data to numeric
   - Imputation handles missing values

2. **Why use train-test split + cross-validation**
   - Train-test split: Unbiased evaluation on unseen data
   - Cross-validation: More robust performance estimate, reduces variance

3. **Difference between Accuracy and F1 Score**
   - Accuracy: Overall correctness (can be misleading with imbalanced data)
   - F1 Score: Harmonic mean of precision and recall (better for imbalanced classes)

4. **Why Random Forest/SVM may perform differently**
   - Random Forest: Ensemble method, handles non-linear relationships, less prone to overfitting
   - SVM: Finds optimal decision boundary, works well with high-dimensional data
   - Performance depends on data characteristics

5. **How to avoid overfitting**
   - Use cross-validation
   - Limit tree depth in Decision Trees/Random Forest
   - Use regularization in Logistic Regression
   - Keep test set separate until final evaluation

### Project Highlights

- Handles real-world messy data automatically
- User-friendly web interface with progress tracking
- Robust error handling and validation
- Optimized for performance (parallel processing)
- Comprehensive evaluation metrics
- Exportable results and trained models

## Technologies Used

- **Python 3.13+**
- **scikit-learn** - Machine learning algorithms
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib** - Plotting
- **seaborn** - Statistical visualizations
- **streamlit** - Web interface
- **joblib** - Model serialization

## Future Enhancements

- Add regression model support
- Hyperparameter tuning with GridSearchCV
- Feature importance visualization
- ROC curves and AUC scores
- Support for more model types (XGBoost, LightGBM)
- Model explainability (SHAP values)
- Automated feature engineering

## License

This project is for educational purposes (BCA Final Year Project).

## Author

BCA Final Year Student

---

**Note**: For best results, use datasets with:
- At least 100 samples
- Categorical target with 2-20 classes
- Balanced or moderately imbalanced classes
- Meaningful features (not just IDs)
