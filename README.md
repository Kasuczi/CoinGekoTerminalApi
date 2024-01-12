# GeckoTerminalAPI Python Wrapper

## Overview
GeckoTerminalAPI is a Python wrapper for interacting with the GeckoTerminal API. This package simplifies accessing cryptocurrency data such as networks, new pools, decentralized exchanges (DEXes), pool information, and trending pools. It is designed for those interested in cryptocurrency market analysis, offering various endpoints to fetch real-time data.

## Features
- Fetch information about various blockchain networks.
- Retrieve new pools for specified networks.
- Get data on decentralized exchanges and pools by addresses.
- Access trending pools and global trending pool information.
- Perform searches for specific pools.

## Installation
To use the GeckoTerminalAPI, ensure you have Python installed on your system. You can then clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/GeckoTerminalAPI.git
cd GeckoTerminalAPI
pip install -r requirements.txt
```

## Usage
Here's a simple example to get you started:

```python
from gecko_terminal_api import GeckoTerminalAPI

api = GeckoTerminalAPI()
networks = api.get_networks()
print(networks)
```

Replace `gecko_terminal_api` with the appropriate module name if different.

## API Methods
- `get_networks()`: Fetch a list of all available networks.
- `get_new_pools(network, include=None)`: Get new pools for a given network.
- `get_dexes(page=1, include=None)`: Retrieve a list of DEXes.
- And more...

Refer to the code documentation for more details on each method.

## Contributing
Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an issue or submit a pull request.



Feel free to modify or extend this template to better suit your project's specific needs or personal preferences.
