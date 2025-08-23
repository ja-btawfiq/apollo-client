# Apollo.io Python SDK

A lightweight, developer-friendly Python SDK for interacting with the [Apollo.io API](https://apolloio.github.io/apollo-api-docs/).

---

## 📦 Installation

Install from source:

```bash
git clone https://github.com/yourusername/apollo-client.git
cd apollo-client
poetry install
```

Activate the virtual environment:

```bash
poetry shell
```

---

## 🔑 Setup

You need an Apollo.io API key, which can be found in your [Apollo.io Developer Settings](https://app.apollo.io/#/settings/developer).

You can set it as an environment variable:

```bash
export APOLLO_API_KEY=your_api_key_here
```

Or pass it directly to the client:

```python
from apollo_client import ApolloClient
client = ApolloClient(api_key="your_api_key_here")
```

---

## 💡 Usage

### 1. Initialize the client

```python
from apollo_client import ApolloClient

client = ApolloClient(api_key="your_api_key")
```

---

## 🧪 Testing

Run tests using:

```bash
poetry run pytest
```
