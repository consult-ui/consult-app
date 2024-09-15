from typing import List

import httpx

from app.config import settings
from app.schemas.organization import OrganizationSuggestion


class Dadata:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url="http://suggestions.dadata.ru/suggestions/api/4_1/rs",
            headers={
                "Authorization": f"Token {settings.dadata_api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

    async def suggest_organizations(self, query: str) -> List[OrganizationSuggestion]:
        resp = await self.client.post("/suggest/party", json={"query": query})
        data = resp.json()

        suggestion_list = data["suggestions"]

        res = []
        for dto in suggestion_list:
            suggest = OrganizationSuggestion(tax_number=dto["data"]["inn"], name=dto["data"]["name"]["short_with_opf"])
            res.append(suggest)

        return res


dadata = Dadata()
