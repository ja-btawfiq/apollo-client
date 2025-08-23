import os
from apollo_sdk import ApolloClient
import pytest


@pytest.fixture
def api_key():
    return os.environ["APOLLO_API_KEY"]


@pytest.fixture
def client(api_key):
    return ApolloClient(api_key)
