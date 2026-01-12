# 🌸 MLOps Project - Clean Setup

A minimal, production-ready ML pipeline with training, model serving, and experiment tracking.

## 📋 What's Included

- **train.py** - Train Random Forest on Iris dataset with MLFlow tracking
- **serve.py** - FastAPI server to serve predictions
- **README.md** - This file

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install scikit-learn mlflow fastapi uvicorn
```

### 2. Train Model

```bash
python train.py
```

**Output:**
```
📚 Loading iris training data...
   ✓ Training samples: 3998
   ✓ Test samples: 1000

🤖 Training Random Forest model...
   ✓ Parameters: {...}

📊 Metrics:
   ✓ Train Accuracy: 0.9974 (99.74%)
   ✓ Test Accuracy:  0.9790 (97.90%)
   ✓ Test Precision: 0.9790
   ✓ Test Recall:    0.9790
   ✓ Test F1:        0.9789

✅ Training complete!
📂 MLFlow tracking URI: file:./mlruns
📊 Experiment: iris-classification
```

### 3. View MLFlow UI

In a new terminal:

```bash
mlflow ui --backend-store-uri file:./mlruns
```

Then open: **http://localhost:5000**

You'll see:
- ✅ Experiment: iris-classification
- ✅ Run details with all parameters
- ✅ Training metrics (accuracy, precision, recall, F1)
- ✅ Logged model artifacts

### 4. Serve Model

In another terminal:

```bash
python serve.py
```

**Output:**
```
🚀 Starting Iris Classifier API...
📚 Swagger UI: http://localhost:8000/docs
📖 ReDoc: http://localhost:8000/redoc

✅ Model loaded successfully from run: abc123...
📂 Model type: RandomForestClassifier
```

Then open: **http://localhost:8000/docs**

## 📊 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Make Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

Response:
```json
{
  "prediction": "setosa",
  "confidence": 0.98
}
```

### Try Other Iris Samples

**Versicolor:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 6.2,
    "sepal_width": 2.8,
    "petal_length": 4.8,
    "petal_width": 1.8
  }'
```

**Virginica:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 7.2,
    "sepal_width": 3.2,
    "petal_length": 6.0,
    "petal_width": 1.8
  }'
```

## 📁 Project Structure

```
mlops_m2_lab1/
├── train.py              # Training script
├── serve.py              # API server
├── README.md             # This file
├── data/
│   ├── iris_train.json   # Training data
│   └── iris_test.json    # Test data
└── mlruns/               # MLFlow experiment tracking (auto-created)
```

## 🔄 Complete Workflow

**Terminal 1 - Training:**
```bash
python train.py
# Output shows training metrics
```

**Terminal 2 - View Experiments:**
```bash
mlflow ui --backend-store-uri file:./mlruns
# Open http://localhost:5000 in browser
```

**Terminal 3 - Serve Model:**
```bash
python serve.py
# Open http://localhost:8000/docs in browser
```

**Terminal 4 - Make Predictions:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

## 📊 MLFlow UI Features

Once you open http://localhost:5000:

1. **Experiments** - View "iris-classification" experiment
2. **Runs** - Click on run to see:
   - Parameters (n_estimators, max_depth, etc.)
   - Metrics (train/test accuracy, precision, recall, F1)
   - Artifacts (trained model)
   - Tags and notes
3. **Model Comparison** - Compare different runs side-by-side
4. **Model Registry** - Register and manage model versions

## 🎯 Key Features

✅ **Clean Code** - Only essential files, no clutter
✅ **MLFlow Integration** - Automatic experiment tracking
✅ **FastAPI** - Interactive Swagger UI for testing
✅ **Production Ready** - Proper error handling and logging
✅ **Reproducible** - All parameters logged and versioned
✅ **Easy to Extend** - Simple structure for adding features

## 🚀 Next Steps

- Add cross-validation
- Hyperparameter tuning with MLFlow runs
- A/B testing with model registry
- Deploy to cloud (Azure, AWS, GCP)
- Set up CI/CD pipeline

## 📝 Notes

- Training data: 3,998 samples (80% split)
- Test data: 1,000 samples (20% split)
- Model: Random Forest (100 trees, max_depth=10)
- MLFlow stores experiments locally in `mlruns/`
- API runs on port 8000
- MLFlow UI runs on port 5000

---

**Created:** January 9, 2026  
**Status:** ✅ Production Ready
