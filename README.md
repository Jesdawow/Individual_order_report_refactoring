# Order Report Refactoring

## Project Overview

This project is based on an existing Python script that creates reports from order data.

The original program already worked, but most of the logic was placed in one file. During the refactoring, the program was divided into smaller modules with clearer responsibilities for loading data, validation, processing and report creation.

The program still has the same main purpose as before. It reads order data from a CSV file, validates and cleans the data, calculates order values and discounted values, creates sales and return reports, and saves the results as CSV files.

The main goal of the refactoring was to make the code easier to understand, test and continue working with without changing the meaning of the original reports.

## Setup

Python 3.13.7 was used for this project.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

The package versions used in the project are listed in `requirements.txt`.

## Dependencies

The project uses:

- `pandas`
- `pytest`

## Run the program

Run the program from the project root:
```bash
python main.py
```

The generated reports are saved in the `output/` folder.

## Run the tests

Run the automated tests from the project root:

```bash
python -m pytest -v
```

## Project Structure
```text
order_report_project/
├── data/
│   └── orders.csv
├── original/
│   └── old_order_report.py
├── output/
│   ├── overview.csv
│   ├── returns_by_category.csv
│   ├── sales_by_category.csv
│   └── sales_by_region.csv
├── src/
│   └── order_report/
│       ├── __init__.py
│       ├── config.py
│       ├── loading.py
│       ├── processing.py
│       ├── reporting.py
│       └── validation.py
├── tests/
│   ├── test_loading.py
│   ├── test_processing.py
│   ├── test_reporting.py
│   └── test_validation.py
├── .gitignore
├── code_review.md
├── main.py
├── README.md
└── requirements.txt
```

The main files have the following responsibilities:
- `main.py` starts the program and connects the different parts of the workflow
- `config.py` contains the configuration for input and output paths
- `loading.py` handles reading the order CSV file
- `validation.py` checks that the order data contains the required columns and reasonable values
- `processing.py` cleans the data and calculates the values used in the reports
- `reporting.py` creates and saves the different reports
- `tests/` contains the automated pytest tests
- `original/` contains the original version of the program before refactoring
- `code_review.md` contains the review of the original program before the refactoring began

## Reflection

### 1. Vilka var de viktigaste problemen i originalkoden?

The biggest problem was that almost the entire workflow was placed in one file. File loading, validation, data cleaning, calculations, report creation and saving were all mixed together.

The original code also used `print()` for execution messages, had broad error handling and contained repeated report logic. Some missing or invalid values were also replaced automatically without showing the user that this had happened.

### 2. Vilka förändringar tycker du förbättrade programmet mest?

I think separating the program into smaller modules made the biggest difference. Each file now has a clearer responsibility, which makes the code easier to follow and test.

Replacing `print()` with logging was also useful because the program now gives clearer information about what happens during a run. The warnings during data cleaning make it easier to see when missing or invalid values have been replaced.

### 3. Varför valde du den projektstruktur du använde?

I wanted the structure to follow the main steps of the program without creating too many small files.

Loading, validation, processing and reporting are separated because they have different responsibilities. `main.py` connects these parts and controls the order in which they run.

This also makes it easier to test individual parts of the program without running the entire workflow every time.

### 4. Var använde du OOP/dataclass och varför passade det där?

I used a `dataclass` called `ReportConfig` in `config.py` for the input file path and output folder.

I thought this was a suitable place to use a dataclass because the two paths belong together and are part of the program configuration. It also keeps the configuration separate from the rest of the program logic.

### 5. Vilka viktiga beteenden skyddar dina automatiska tester, och vilken nytta ger testerna om programmet förändras i framtiden?

The tests cover important parts of the program such as loading files, handling missing files, checking required columns, validating unreasonable values, cleaning the data and calculating order values.

They also test the main report calculations. If the program is changed later, the tests can help show if something that worked before has accidentally stopped working.

### 6. Vad var svårast?

The hardest part was splitting the original script into separate modules without changing the results.

I had to think about what should belong in loading, validation, processing and reporting, while still keeping the same calculations and overall behavior as the original program.

### 7. Vad hade du velat förbättra ytterligare om du haft mer tid?

Like in my other project, I would have liked to make it easier to choose another input file without changing `main.py`.

I would also have liked to save the logs to a file so previous runs could be reviewed later, improve the validation further and make some of the cleaning rules easier to change.