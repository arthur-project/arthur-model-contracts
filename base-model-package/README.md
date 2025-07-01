# Arthur Model Contracts - Base Model Package

A Python package that provides base classes for machine learning models, preprocessors, and postprocessors to be used with the Arthur backend system.

## Overview

This package defines the contract interface that models must implement to be properly loaded and executed by the Arthur backend. It includes base classes for:

- **BaseModel**: Template for machine learning models (Keras/PyTorch)
- **BasePreprocess**: Template for data preprocessing
- **BasePostprocess**: Template for data postprocessing

## Installation

```bash
pip install base-model-package
```

## Model Requirements for Neptune Integration

To deploy your model to the Arthur backend via Neptune, you need to provide specific files and follow certain conventions.

### Required Neptune Configuration

In Neptune, you must specify the following key:

**`files`** - Comma-separated list of file names to download, for example:
```
preprocessor.pkl,preprocessor.py,postprocessor.pkl,postprocessor.py,model.keras
```

### File Requirements

1. **Model Files**
   - **Keras models**: Save as `.keras` or `.h5` format with full architecture
   - **PyTorch models**: Save as `.pt`, `.pth`, or `.pytorch` format with full architecture
   - ⚠️ **Important**: We do not support loading weight dictionaries only - models must include the complete architecture

2. **Preprocessor Files** (if applicable)
   - `preprocessor.pkl` - Serialized preprocessor object
   - `preprocessor.py` - Python script containing the preprocessor class definition

3. **Postprocessor Files** (if applicable)
   - `postprocessor.pkl` - Serialized postprocessor object  
   - `postprocessor.py` - Python script containing the postprocessor class definition

4. **Custom Dependencies**
   - Any additional Python scripts that your preprocessor/postprocessor depends on
   - These must also be listed in the `files` key in Neptune

### Implementation Requirements

#### Preprocessor Implementation

Your preprocessor class **must inherit** from `BasePreprocess`:

```python
from base_model import BasePreprocess

class CustomPreprocessor(BasePreprocess):
    def __init__(self):
        super().__init__()
        # Your initialization code here
    
    def process(self, wave: list[float]) -> list[float]:
        # Your preprocessing logic here
        # Input: list of float values representing audio waveform
        # Output: preprocessed data as built-in Python types (e.g., list[float])
        pass
```

#### Postprocessor Implementation

Your postprocessor class **must inherit** from `BasePostprocess`:

```python
from base_model import BasePostprocess

class CustomPostprocessor(BasePostprocess):
    def __init__(self):
        super().__init__()
        # Your initialization code here
    
    def process(self, data: list[float]) -> list[tuple[str, float]]:
        # Your postprocessing logic here
        # Input: raw model output as built-in Python types (e.g., list[float])
        # Output: processed results as built-in Python types
        pass
```

#### Model Implementation (Optional)

While not required, you can optionally inherit from `BaseModel` for consistency:

```python
from base_model import BaseModel

class CustomModel(BaseModel):
    def __init__(self, path_to_model: str):
        super().__init__(path_to_model)
        # Load your model here
    
    def predict(self, wave: list[float], sample_rate: int = 16000) -> list[tuple[str, float]]:
        # Your prediction logic here
        # Input: audio waveform and sample rate
        # Output: list of (word, probability) tuples
        pass
```

## Example Neptune Configuration

Here's a complete example of what you need to upload to Neptune:

### Files to Upload:
- `model.keras` (or `model.pt` for PyTorch)
- `preprocessor.pkl`
- `preprocessor.py`
- `postprocessor.pkl`
- `postprocessor.py`
- Any additional custom dependencies

### Neptune Configuration:
```
files: preprocessor.pkl,preprocessor.py,postprocessor.pkl,postprocessor.py,model.keras
```

## Example Implementation

### preprocessor.py
```python
from base_model import BasePreprocess
import numpy as np

class AudioPreprocessor(BasePreprocess):
    def __init__(self):
        super().__init__()
        self.target_length = 16000
    
    def process(self, wave: list[float]) -> list[float]:
        # Convert to numpy array for internal processing
        wave_array = np.array(wave)
        
        # Normalize
        if np.max(np.abs(wave_array)) > 0:
            wave_array = wave_array / np.max(np.abs(wave_array))
        
        # Pad or truncate to target length
        if len(wave_array) > self.target_length:
            wave_array = wave_array[:self.target_length]
        else:
            wave_array = np.pad(wave_array, (0, self.target_length - len(wave_array)))
        
        # Return as built-in Python list
        return wave_array.tolist()
```

### postprocessor.py
```python
from base_model import BasePostprocess
import numpy as np

class AudioPostprocessor(BasePostprocess):
    def __init__(self):
        super().__init__()
        self.labels = ["word1", "word2", "word3"]  # Your class labels
    
    def process(self, data: list[float]) -> list[tuple[str, float]]:
        # Convert to numpy array for internal processing
        data_array = np.array(data)
        
        # Apply softmax to get probabilities
        probabilities = np.exp(data_array) / np.sum(np.exp(data_array))
        
        # Create list of (label, probability) tuples using built-in types
        results = [(label, float(prob)) for label, prob in zip(self.labels, probabilities.tolist())]
        
        # Sort by probability (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
```

### Creating Pickle Files
```python
import pickle

# Create and save preprocessor
preprocessor = AudioPreprocessor()
with open('preprocessor.pkl', 'wb') as f:
    pickle.dump(preprocessor, f)

# Create and save postprocessor
postprocessor = AudioPostprocessor()
with open('postprocessor.pkl', 'wb') as f:
    pickle.dump(postprocessor, f)
```

## Backend Integration

The Arthur backend will:

1. Download all files specified in the Neptune `files` key
2. Load the Python scripts to get class definitions
3. Deserialize the pickle files using the loaded class definitions
4. Load the model using standard Keras/PyTorch loading mechanisms
5. Execute the preprocessing → model inference → postprocessing pipeline

## Supported Model Formats

- **Keras**: `.keras`, `.h5`
- **PyTorch**: `.pt`, `.pth`, `.pytorch`

## Important Notes

- All preprocessor and postprocessor classes must inherit from the respective base classes
- Python scripts containing class definitions are required for proper deserialization
- Models must be saved with full architecture, not just weights
- Custom dependencies must be included in the Neptune files list
- File names specified in Neptune must match exactly

## Requirements

- Python >= 3.10
- Compatible with Keras and PyTorch models

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please contact the Arthur development team.