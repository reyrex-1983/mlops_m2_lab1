#!/bin/bash
# Quick verification script for the MLOps pipeline

echo "🔍 MLOps Pipeline Verification"
echo "================================\n"

# Check Python imports
echo "✓ Testing Python imports..."
python3 -c "from src.config import *; from src.data_utils import *; from src.model_utils import *; from src.mlflow_utils import *; print('  ✅ All imports successful\n')" 2>/dev/null || echo "  ❌ Import test failed\n"

# Check files exist
echo "✓ Checking essential files..."
files=("train.py" "serve.py" "src/config.py" "src/data_utils.py" "src/model_utils.py" "src/mlflow_utils.py" "data/iris_train.json" "data/iris_test.json" "venv/bin/python")
for file in "${files[@]}"; do
    if [ -f "$file" ] || [ -d "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
    fi
done

echo "\n✓ Project statistics..."
echo "  📁 Total Python files: $(find . -name '*.py' -type f | grep -v venv | wc -l)"
echo "  📝 Total lines of code: $(find . -name '*.py' -type f | grep -v venv | xargs wc -l | tail -1 | awk '{print $1}')"
echo "  🏋️  Training samples: $(cat data/iris_train.json | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")"
echo "  🧪 Test samples: $(cat data/iris_test.json | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")"

echo "\n✅ Verification complete!"
echo "\n📖 Quick start:"
echo "   1. source venv/bin/activate"
echo "   2. python train.py          # Train the model"
echo "   3. python serve.py          # Start the API"
echo "   4. mlflow ui                # View experiments"
