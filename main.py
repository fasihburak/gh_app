import os
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from enum import Enum
from datetime import date
import aiohttp


load_dotenv()
app = FastAPI()


class PerPageOptions(int, Enum):
    ten = 10
    fifty = 50
    hundred = 100


class SearchParams(BaseModel):
    from_date: date | None = None
    programming_language: str | None = None

    def return_search_str(self):
        # Because Github API requires a search parameter(q) when searching for repositories,
        # we need to make sure we have at least one search parameter (Here 'created' is chosen as such).
        search_str = 'created:>='
        if self.from_date:
            search_str += str(self.from_date)
        else:
            # Set the default date to a reasonably old date like 1970-01-01. Earlier dates are not validated on the GH server.
            search_str += '1970-01-01' 
        if self.programming_language:
            # "+" sign is encoded as "%2B" in the URL. Whitespace gets the job done here. Save it for discussion.
            search_str += f'+language:{self.programming_language}'
        return search_str


class QueryParams(SearchParams):
    top: PerPageOptions = PerPageOptions.ten

    def return_query_params(self):
        # Faced some issues with this method. The URL was not being formed correctly when sending the request. Discuss this.
        query_params = {'sort': 'stars', 'order': 'desc', 'per_page': self.top.value, 'q': self.return_search_str()}
        return query_params
    
    def return_query_str(self):
        query_str = f'?q={self.return_search_str()}'
        query_str += f'&sort=stars&order=desc&per_page={self.top.value}'
        return query_str



@app.get("/search/repositories/")
async def search_repositories(query_params: QueryParams = Depends()):
    query_str = query_params.return_query_str()
    print("Query Params:", query_params)
    base_url = os.environ['GITHUB_API_BASE_URL']
    async with aiohttp.ClientSession(base_url=base_url) as session:
        async with session.get(url='/search/repositories' + query_str) as response:
            print("WHOLE URL", response.url)
            payload = await response.json()
            return JSONResponse(status_code=response.status, content=payload)

