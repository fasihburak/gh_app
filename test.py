import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app, aiohttp  # replace with the actual name of your FastAPI app


client = TestClient(app)

async def mock_aiohttp_session_get(url):
    print("Request URL:", url)
    return "foo"


class TestSearchRepositories(unittest.TestCase):
    def test_search_repositories(self):
        response = client.get("/search/repositories/?top=10")
        with patch('aiohttp.ClientSession.get') as mock_get:
            assert mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()


# import unittest
# from unittest.mock import patch
# from fastapi.testclient import TestClient
# from main import app  # replace with the actual name of your FastAPI app

# class TestSearchRepositories(unittest.TestCase):
#     @patch('aiohttp.ClientSession.get')
#     def test_search_repositories(self, mock_get):
#         client = TestClient(app)
#         response = client.get("/search/repositories/?top=10&from_date=2023-12-31&programming_language=python")
#         self.assertEqual(response.status_code, 200)
#         mock_get.assert_called_once()
#         args, kwargs = mock_get.call_args
#         self.assertEqual(args[0], 'https://api.github.com/search/repositories?q=created=2023-12-31..*&sort=stars&order=desc&per_page=10&language=python')

# if __name__ == '__main__':
#     unittest.main()


#     @app.get("/search/repositories/")
# async def search_repositories(top: PerPageOptions = PerPageOptions.ten, from_date: date = None, programming_language: str = None):
# # async def search_repositories(top: PerPageOptions = PerPageOptions.ten, from_date: date = '2023-12-31', programming_language: str = 'python'):
#     args = locals()
#     print("ARGS", args)

#     async with aiohttp.ClientSession() as session:
        
#         @pytest.fixture
#         def client():
#             return TestClient(app)

#         def test_search_repositories_url(client):
#             with client.session as session:
#                 async def mock_get(url):
#                     assert url == 'https://api.github.com/search/repositories?q=created=2023-12-31..*&sort=stars&order=desc&per_page=10&language=python'
#                     return MockResponse()

#                 session.get = mock_get
#                 response = client.get("/search/repositories/")
#                 assert response.status_code == 200

#         class MockResponse:
#             def __init__(self):
#                 self.status = 200
#                 self.headers = {'content-type': 'application/json'}

#             async def json(self):
#                 return {"mock": "response"}