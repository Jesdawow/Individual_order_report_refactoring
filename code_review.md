# Code Review of `order_report.py`

## Starting Point

The original program can read order data from a CSV file, clean and transform the data, calculate sales and returns, and save several reports in `output/`.

The program produces all the required results, but most of the logic is located in one file. So the purpose of this code review is to identify areas that can be improved before refactoring the program.

## Review Findings

### Finding 1 - The program runs directly at import

**Observation:**
Most of the program is executed directly at module level. Reading data, processing it and creating reports starts immediately when `order_report.py` is executed or imported.

**Consequence:**
Importing the module can cause unexpected side effects such as reading and writing files. It also makes the code harder to reuse and test because importing a function would also start the entire workflow.

**Suggestion:**
Move the main workflow into a `main()` function and use a main guard so the program only starts when it is executed directly.

### Finding 2 - The code mixes several parts of the workflow

**Observation:**
The same script is responsible for loading the order file, cleaning values, checking the data, calculating new columns, building summaries and saving several output files.

**Consequence:**
Because the whole workflow is connected in one place, it becomes harder to work with one part without also depending on the others. For example, testing a calculation should not require the program to also read a CSV file and save reports.

**Suggestion:**
Split the workflow into separate parts so that loading, validation, calculations and report creation can be used and tested independently.

### Finding 3 - Data problems are replaced without being reported

**Observation:**
Some missing or invalid values are automatically replaced during the data cleaning. As an example, missing `quantity` values are replaced with `1`, invalid `discount` values become `0` and missing `unit_price` values are replaced with the median price.

**Consequence:**
The program can continue running, but these replacements may affect the final reports without making it clear that the original data contained problems. This can make the final results harder to understand and explain.

**Suggestion:**
Keep the cleaning rules if they are part of the expected behavior, but report when values are replaced. Logging warnings or validation messages would make these changes visible without changing the existing report calculations.

### Finding 4 - Similar report logic is repeated

**Observation:**
The reports for product category and region are built with almost the same sequence of steps. Both group the data, calculate order count, total sales and returns, calculate a return rate and then sort the results.

**Consequence:**
When the same logic exists in several places, future changes may need to be made more than once. This also increases the risk that similar reports start behaving differently by mistake.

**Suggestion:**
Move the shared report logic into a reusable function and pass the grouping column as an argument. This would reduce duplication while keeping the same calculations and report results.

### Finding 5 - Missing columns are not explained clearly

**Observation:**
The program checks if all required columns exist, but if one or more are missing it only raises a general error with the message `Fel data`.

**Consequence:**
The error message does not explain which columns are missing, so the user has to investigate the input file manually. This also makes the validation harder to test clearly.

**Suggestion:**
Identify the missing columns and include their names in the error message. A more specific exception, such as `ValueError`, could also be used instead of a general `Exception`.

### Finding 6 - Execution messages and errors are handled too generally

**Observation:**
The program uses `print()` to show information about the execution, like when data has been loaded or when a report has been saved. At the same time, almost the entire program is wrapped in one broad `except Exception`.

**Consequence:**
It becomes harder to separate normal execution information from actual errors. Different types of problems are also handled in the same way, which makes troubleshooting more difficult.

**Suggestion:**
Use Python logging instead of `print()` for messages about what the program is doing. Also handle expected errors more specifically instead of catching every possible error in the same way. 

### Finding 7 - File paths are hardcoded

**Observation:**
The input file and output folder are hardcoded in the script. The script also does not create the `output/` folder before saving the report files.

**Consequence:**
The program is less flexible if another input file or output location should be used. If the output folder is missing, saving the reports can also fail.

**Suggestion:**
Store the file paths in a clearer configuration and create the output folder automatically if it does not already exist.