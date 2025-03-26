# Agno Agent Boilerplate

This is a boilerplate project for implementing Agno agents. It provides a basic structure and example implementation of a custom Agno agent.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add any necessary environment variables:
```
# Add your environment variables here
```

## Usage

The main agent implementation is in `agno_agent.py`. To run the example:

```bash
python agno_agent.py
```

## Customization

To create your own agent:

1. Modify the `CustomAgent` class in `agno_agent.py`
2. Implement your custom logic in the `process` method
3. Update the configuration in the `main` function as needed

## Project Structure

- `agno_agent.py`: Main agent implementation
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (create this file)
- `README.md`: This file

## License

MIT License 