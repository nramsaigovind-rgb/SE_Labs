# Lab 5: Static Code Analysis — Issue Report

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe YAML loading | Security | 21 | `yaml.load()` with an unsafe loader may construct arbitrary Python objects. | Replaced with `yaml.safe_load()`. |
| Hardcoded password | Security | 66 | A database password was embedded directly in the source code. | Read the password from the `WARDEN_DB_PASSWORD` environment variable. |
| Insecure remote logging | Security | 72 | The remote logging configuration listener can introduce security risks. | Disabled the unauthenticated listener. |
| Flask debug mode | Security | 80 | Debug mode may expose an interactive debugger and enable code execution. | Set `debug=False`. |
| Weak random generator for security-sensitive use | Security | 56 | Bandit flags the standard random generator as unsuitable for security-sensitive randomness. | Used `secrets.SystemRandom()` for the lottery. |
| Mutable default argument | Code quality | 29 | The default list can be shared across function calls. | Changed the default to `None` and initialized a new list inside the function. |
| Incorrect type checking | Code quality | 30 | `type(year) != int` is less idiomatic and accepts no distinction for Boolean values. | Used `isinstance()` and explicitly rejected Boolean values. |
| Incorrect room allocation logic | Bug | 29–39 | The original code did not enforce room gender and used an incorrect capacity comparison. | Checked room gender and capacity before allocating. |
| Incorrect vacancy counting | Bug | 58–63 | The original function counted beds only in completely empty rooms. | Counted each room's remaining capacity. |
| Style and documentation violations | Style | Multiple | Missing docstrings, inconsistent naming, unused imports, and formatting problems were reported. | Added docstrings, used `snake_case`, removed unused imports, and reformatted the code. |

## Verification

The after reports are stored in `reports/after/`. The original reports are stored in `reports/before/`. Final scores and remaining findings must be recorded from the actual tool output.