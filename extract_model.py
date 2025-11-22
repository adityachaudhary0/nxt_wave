"""
Script to extract XGBoost model from PyCaret pickle file.
This bypasses PyCaret's Python version check by patching the module.
"""
import sys
import importlib.util
import joblib
import xgboost as xgb

# Patch pycaret's __init__.py to bypass version check
pycaret_init_path = 'venv/lib/python3.12/site-packages/pycaret/__init__.py'
with open(pycaret_init_path, 'r') as f:
    content = f.read()

# Save original
original_content = content

# Patch the version check
if 'elif sys.version_info >= (3, 12):' in content:
    content = content.replace(
        'elif sys.version_info >= (3, 12):\n    raise RuntimeError(',
        'elif sys.version_info >= (3, 12):\n    # Temporarily disabled\n    pass  # raise RuntimeError('
    )
    with open(pycaret_init_path, 'w') as f:
        f.write(content)

try:
    # Patch distutils import issue
    import setuptools
    if not hasattr(sys.modules.get('distutils', None), 'version'):
        import distutils
        if 'distutils' not in sys.modules:
            sys.modules['distutils'] = setuptools.distutils
    
    # Now try to import and load
    from pycaret.classification import load_model
    
    print("Loading PyCaret model...")
    model = load_model('models/Water_Potability/xgboost_without_source_month')
    
    # Extract the underlying XGBoost model
    # PyCaret models are typically wrapped, so we need to get the estimator
    if hasattr(model, 'estimator'):
        xgb_model = model.estimator
    elif hasattr(model, '_model'):
        xgb_model = model._model
    elif hasattr(model, 'model'):
        xgb_model = model.model
    else:
        # Try to get it from the model object directly
        xgb_model = model
    
    print(f"Model type: {type(xgb_model)}")
    
    # If it's a Pipeline, extract the final estimator
    if hasattr(xgb_model, 'steps') or hasattr(xgb_model, 'named_steps'):
        print("Model is a Pipeline, extracting final estimator...")
        if hasattr(xgb_model, 'named_steps'):
            # Get the last step which should be the model
            steps = list(xgb_model.named_steps.items())
            if steps:
                final_step_name, final_estimator = steps[-1]
                print(f"Final step: {final_step_name}, type: {type(final_estimator)}")
                xgb_model = final_estimator
        elif hasattr(xgb_model, 'steps'):
            if xgb_model.steps:
                final_step_name, final_estimator = xgb_model.steps[-1]
                print(f"Final step: {final_step_name}, type: {type(final_estimator)}")
                xgb_model = final_estimator
    
    # If it still has an estimator attribute, get it
    if hasattr(xgb_model, 'estimator'):
        xgb_model = xgb_model.estimator
        print(f"Extracted estimator, type: {type(xgb_model)}")
    
    print(f"Final model type: {type(xgb_model)}")
    print(f"Model attributes: {[attr for attr in dir(xgb_model) if not attr.startswith('_')][:10]}")
    
    # Save the pipeline (which includes preprocessing) and the raw model
    print("Saving models...")
    
    # Save the full pipeline for use with predict_model equivalent
    joblib.dump(model, 'models/Water_Potability/xgboost_pipeline.pkl')
    print("Saved full pipeline as pickle")
    
    # Save the XGBoost model directly if it's an XGBoost model
    if 'xgboost' in str(type(xgb_model)).lower() or hasattr(xgb_model, 'save_model'):
        if hasattr(xgb_model, 'save_model'):
            xgb_model.save_model('models/Water_Potability/xgboost_model.json')
            print("Saved XGBoost model as JSON format")
        
        joblib.dump(xgb_model, 'models/Water_Potability/xgboost_model.pkl')
        print("Saved XGBoost model as pickle format")
    else:
        # Save whatever we have
        joblib.dump(xgb_model, 'models/Water_Potability/xgboost_model.pkl')
        print("Saved model as pickle format")
    
    print("Model extracted successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Restore original content
    with open(pycaret_init_path, 'w') as f:
        f.write(original_content)

