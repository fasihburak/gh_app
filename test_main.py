import pytest
from aioresponses import aioresponses
from asyncio import TimeoutError
from fastapi.testclient import TestClient
import re
from main import app


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_search_with_all_params(anyio_backend):
    client = TestClient(app)
    with aioresponses() as mocked:
        pattern = re.compile(r'')
        mocked.get(url=pattern, status=200, body='{"test": false}')
        response = client.get("/search/repositories/?top=10&from_date=2023-12-31&programming_language=python")
        mocked.assert_called_once_with('/search/repositories?per_page=10&q=created:>=2023-12-31+language:python&sort=stars&order=desc')

@pytest.mark.anyio
async def test_search_with_only_top(anyio_backend):
    client = TestClient(app)
    with aioresponses() as mocked:
        pattern = re.compile(r'')
        mocked.get(url=pattern, status=200, body='{"test": false}')
        response = client.get("/search/repositories/?top=10")
        mocked.assert_called_once_with('/search/repositories?per_page=10&q=created:>=1970-01-01&sort=stars&order=desc')

@pytest.mark.anyio
async def test_search_with_top_and_language(anyio_backend):
    client = TestClient(app)
    with aioresponses() as mocked:
        pattern = re.compile(r'')
        mocked.get(url=pattern, status=200, body='{"test": false}')
        response = client.get("/search/repositories/?top=10&programming_language=python")
        mocked.assert_called_once_with('/search/repositories?per_page=10&q=created:>=1970-01-01+language:python&sort=stars&order=desc')

@pytest.mark.anyio
async def test_search_with_top_and_from_date(anyio_backend):
    client = TestClient(app)
    with aioresponses() as mocked:
        pattern = re.compile(r'')
        mocked.get(url=pattern, status=200, body='{"test": false}')
        response = client.get("/search/repositories/?top=10&from_date=2023-12-31")
        mocked.assert_called_once_with('/search/repositories?per_page=10&q=created:>=2023-12-31&sort=stars&order=desc')

@pytest.mark.anyio
async def test_search_timeout(anyio_backend):
    client = TestClient(app)
    with aioresponses() as mocked:
        pattern = re.compile(r'')
        mocked.get(url=pattern, exception=TimeoutError)
        with pytest.raises(TimeoutError):
            response = client.get("/search/repositories/?top=10&from_date=2023-12-31")
