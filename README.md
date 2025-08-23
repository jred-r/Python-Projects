# Python Projects

This repository contains various Python projects that I work on in my spare time.

## Project Information

- **Name:** python-projects
- **Version:** 1.0
- **Description:** These are some projects that I work on in my spare time.
- **Python Version:** Requires Python >=3.11 (see [.python-version](.python-version))

## Getting Started

### 1. Initialize the Project

```sh
uv init 'python-projects'
```

### 2. Create a Virtual Environment

```sh
uv venv
```

### 3. Install Dependencies

```sh
uv sync
```

### 4. Add a Package

```sh
uv add requests
```

#### Specify a Version Constraint

```sh
uv add 'requests==2.31.0'
```

### 5. Remove a Package

```sh
uv remove requests
```

### 6. Upgrade a Package

```sh
uv lock --upgrade-package requests
```

### 7. Add Flask and Run a Development Server

```sh
uv add flask
uv run -- flask run -p 3000
```

## Main Script

To run the main script:

```sh
python main.py
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Resources

- [UV Documentation](https://docs.astral.sh/uv/concepts/projects/dependencies/#changing-dependencies)