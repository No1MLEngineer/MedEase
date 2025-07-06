# Agent Development Guidelines for Planetary Scientist's Assistant (PSA)

This document provides guidelines for AI agents working on the Planetary Scientist's Assistant (PSA) project.

## Core Principles

1.  **Offline First:** Prioritize functionalities that can operate entirely offline. Any feature requiring internet access must be clearly marked and should be an optional enhancement.
2.  **Resource Efficiency:** Design components to be mindful of CPU, memory, and power usage, considering potential deployment in resource-constrained environments.
3.  **Modularity:** Develop features in distinct modules to promote maintainability and allow for easier future expansion or specialization (e.g., adding tools for specific scientific domains).
4.  **Reliability:** Strive for robust code. Implement error handling and consider edge cases, especially for data integrity and critical calculations.
5.  **Python Standard Library & Common Open-Source Libraries:**
    *   Utilize Python 3.
    *   Prefer Python's standard library where possible.
    *   If external libraries are needed, choose well-maintained, widely-used open-source options that are easily installable via pip (e.g., pandas, numpy, scipy, matplotlib, PyPDF2, sqlite3).
    *   Avoid libraries with restrictive licenses or those requiring paid APIs.
6.  **Colab Compatibility:** Write code that can be easily copied and run in Google Colab or similar Jupyter notebook environments. This means:
    *   Standard Python syntax.
    *   Clear dependency listings (e.g., provide `pip install` commands in comments or documentation if specific versions are needed).
    *   Standard file I/O that can be adapted to Colab's file system (e.g., Google Drive mounting).

## Project Structure

The project is organized into the following main directories:

-   `data_manager/`: For data loading, storage, and analysis tools.
-   `experiment_support/`: For experiment logging and protocol management.
-   `knowledge_base/`: For document and note management.
-   `sci_utils/`: For scientific calculators, unit converters, etc.
-   `ui/`: For user interface components (initially CLI).
-   `tests/`: For unit tests.
-   `main.py` or `app.py`: Main application entry point.

## Coding Conventions

-   Follow PEP 8 style guidelines for Python code.
-   Include docstrings for all modules, classes, and functions.
-   Write clear and concise comments where necessary.
-   Ensure variable and function names are descriptive.

## Testing

-   Write unit tests for new functionalities, especially for utility functions and core logic.
-   Place tests in the `tests/` directory, mirroring the module structure.
-   Use Python's `unittest` framework or `pytest`.

## Commits and Branching

-   (If applicable to the development environment) Use descriptive commit messages.
-   (If applicable) Create feature branches for significant new functionalities.

## Documentation

-   Keep `README.md` updated with project status, setup instructions, and usage examples.
-   Document any complex algorithms or design decisions within the code or in separate design documents if necessary.

By following these guidelines, we can ensure the PSA project is developed in a consistent, maintainable, and effective manner.
