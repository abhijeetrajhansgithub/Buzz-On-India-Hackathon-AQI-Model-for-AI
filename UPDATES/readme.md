# The Required Updates

## Inclusion of Intel Modules

### Overview

This update involves integrating Intel-optimized modules into the existing codebase, leveraging Intel® oneAPI Data Analytics Library (oneDAL) for enhanced performance in data analytics tasks. oneDAL is designed to accelerate big data analysis by providing highly optimized algorithmic building blocks for all stages of data processing, including preprocessing, transformation, analysis, modeling, validation, and decision-making. These updates will focus on the integration of Intel’s scikit-learn-intelex and associated modules to speed up algorithmic computation, improve scalability, and increase throughput.

### Changes to the `run.py` File

The following changes are required in the `run.py` file to include Intel-optimized model calculations:

```python
# Intel Optimised Model
from algorithms.model.intel_optimised_models.use_intel_optimised_model_for_calculation import (
    intel__calculate_air_quality_manually,
    intel__calculate_air_quality_manually_final_suggested_verdict
)
```

### Purpose of Intel-Optimized Model

The functions from the `use_intel_optimised_model_for_calculation.py` file are responsible for generating predictions using models trained on Intel’s scikit-learn-intelex. This optimized version of scikit-learn is specifically built to speed up data analysis by utilizing Intel’s oneDAL library.

Intel® oneAPI Data Analytics Library (oneDAL) accelerates big data analytics by:

- Providing highly optimized algorithms for various stages of data analytics (preprocessing, transformation, analysis, modeling, validation, and decision-making).
- Optimizing data ingestion and algorithmic computations to enhance throughput and scalability.
- Supporting multiple modes of computation, including batch, online, and distributed processing.
- Offering C++ and Java* APIs along with connectors to popular data sources such as Spark* and Hadoop*.
- Including Python* wrappers as part of Intel Distribution for Python.

### File Breakdown

1. **`use_intel_optimised_model_for_calculation.py`:**
   - This file contains functions that perform predictions using models optimized by Intel’s scikit-learn-intelex.
   - These models are trained using Intel’s oneDAL library for improved speed and efficiency in handling large-scale data.

2. **Functions Imported:**
   - `intel__calculate_air_quality_manually`: This function calculates air quality predictions using the Intel-optimized model.
   - `intel__calculate_air_quality_manually_final_suggested_verdict`: This function refines the air quality predictions and provides the final suggested verdict based on the model's calculations.

### Directory Updates

The updated directory will include all changes and additions required to ensure that the project utilizes Intel-optimized modules to achieve the desired performance outcomes. These updates primarily focus on replacing standard model calculations with Intel-optimized versions to leverage the performance benefits of oneDAL.
