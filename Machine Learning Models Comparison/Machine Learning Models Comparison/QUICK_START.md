# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Run the App
```powershell
python -m streamlit run app.py
```

### Step 3: Use the Dashboard
1. Open browser at `http://localhost:8501`
2. Select **"Churn"** as target column (not customerID!)
3. Click **"Run Model Comparison"**
4. View results and download outputs

---

## 📊 Expected Results (Telco Churn Dataset)

| Model | Accuracy |
|-------|----------|
| Logistic Regression | ~79% |
| SVM | ~79% |
| Random Forest | ~79% |
| Decision Tree | ~78% |
| KNN | ~76% |

---

## ⚡ Command Line Usage

### Basic:
```powershell
python src\compare_models.py --data data\telco_churn.csv --target Churn --drop-cols customerID
```

### Advanced:
```powershell
python src\compare_models.py --data data\telco_churn.csv --target Churn --drop-cols customerID --test-size 0.25 --cv 10
```

---

## 🎯 Common Mistakes to Avoid

❌ **DON'T** select `customerID` as target → It's an ID column!  
✅ **DO** select `Churn` as target → It's the classification label

❌ **DON'T** forget to drop ID columns  
✅ **DO** drop `customerID`, `PassengerId`, etc.

❌ **DON'T** use datasets with < 20 samples  
✅ **DO** use datasets with 100+ samples for meaningful results

---

## 📁 Output Files Location

All results saved in `outputs/` folder:
- `model_comparison_telco_churn.csv` - Results table
- `best_model_telco_churn.pkl` - Trained model
- `accuracy_comparison.png` - Bar chart
- `best_model_confusion_matrix.png` - Confusion matrix

---

## 🆘 Troubleshooting

**App won't start?**
```powershell
pip install --upgrade streamlit
```

**Training too slow?**
- Reduce CV folds to 3
- Use smaller dataset
- Check you didn't select an ID column as target

**"Module not found" error?**
```powershell
pip install -r requirements.txt --upgrade
```

---

## 💡 Pro Tips

1. **For presentations**: Use the Streamlit app (more visual)
2. **For batch processing**: Use command line
3. **For reproducibility**: Always set `--random-state 42`
4. **For faster training**: Reduce `--cv` to 3 folds
5. **For better results**: Drop irrelevant columns before training

---

## 📞 Need Help?

Check the full README.md for detailed documentation!
