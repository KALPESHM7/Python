
# Banking System (Python, Jupyter Notebook)

This repository contains a Jupyter Notebook (`BankingSystem.ipynb`) that implements a command-line Python banking system using dictionaries. Features include account creation (savings/checking), deposits, withdrawals, transaction logging, and more.

## Prerequisites

- Python 3.x installed on your system.
- Jupyter Notebook (or JupyterLab) installed.

### Install Jupyter via pip (if not already):
```bash
pip install notebook
```

## Clone the Repository

```bash
git clone https://github.com/KALPESHM7/Python.git
cd Python/BankSystem_using_Dictionary
```

## Launch & Run the Notebook

In the project directory, start Jupyter Notebook:

```bash
jupyter notebook
```

Once the browser opens, click on **BankingSystem.ipynb** to open it. Then, run the cells in order (using the **Run** button or press `Shift + Enter`).

## Alternate Execution via Terminal (Optional)

You can also execute all notebook cells in one go:

```bash
jupyter nbconvert --execute --to notebook BankingSystem.ipynb
```

This runs the notebook non-interactively and saves the output to a new file (`BankingSystem.nbconvert.ipynb`).

## Requirements for Testing

Make sure `pytest` is installed for running tests (if you’ve included test code):

```bash
pip install pytest
```

Then, to run tests (assuming they’re extracted to `test_bank_system.py`):

```bash
pytest test_bank_system.py
```

## Project Structure

```
Python/
└── BankSystem_using_Dictionary/
    ├── BankingSystem.ipynb
    └── README.md
```

## Summary of Available Actions

- Create new accounts (Savings or Checking)
- Deposit and Withdrawal operations
- View account balance
- Display transaction history and account details

---


