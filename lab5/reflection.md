# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, and coding-style violations before deployment.

### 2. What did the tools identify?

Pylint identified code-quality problems, including missing docstrings, inconsistent function naming, unused imports, and a mutable default argument. Bandit identified potential security risks involving YAML loading, a hardcoded password, remote logging, debug mode, and random number generation. Flake8 identified unused imports and formatting violations.

### 3. How were the issues addressed?

The code was updated to use safe YAML loading, environment-based password configuration, disabled remote logging, disabled Flask debug mode, and a cryptographically secure random generator. The room allocation logic, vacancy calculation, function names, documentation, and formatting were also improved.

### 4. What did you learn?

I learned that a program can execute successfully while still containing security vulnerabilities, logical bugs, and style problems. Using multiple static analysis tools provides different perspectives on code quality. Rerunning the tools after making corrections helps verify whether the changes resolved the reported issues.