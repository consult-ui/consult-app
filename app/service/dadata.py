from typing import List

import httpx

from app.config import settings
from app.schemas.organization import OrganizationSuggestion, ExternalOrganization


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

    async def search_organization(self, tax_number: str) -> ExternalOrganization | None:
        resp = await self.client.post("/findById/party", json={
            "query": tax_number,
            "branch_type": "MAIN",
            "count": 1
        })
        data = resp.json()

        if not data["suggestions"]:
            return None

        dto = data["suggestions"][0]

        org_data = dto["data"]

        head_name = org_data.get("management")
        if head_name:
            head_name = head_name.get("name")

        address = org_data.get("address")
        if address:
            address = address["value"]

        activity_type = org_data.get("okved")
        if activity_type:
            activity_type = await self.get_okved_desc(activity_type)

        return ExternalOrganization(
            tax_number=tax_number,
            name=org_data["name"]["short_with_opf"],
            head_name=head_name,
            address=address,
            activity_type=activity_type,
        )

    async def get_okved_desc(self, code: str) -> str | None:
        resp = await self.client.post("/findById/okved2", json={"query": code})

        data = resp.json()

        if not data["suggestions"]:
            return None

        return data["suggestions"][0]["value"]

    async def suggest_organizations(self, query: str) -> List[OrganizationSuggestion]:
        resp = await self.client.post("/suggest/party", json={"query": query})
        data = resp.json()

        suggestion_list = data["suggestions"]

        res = []
        for dto in suggestion_list:
            org_data = dto["data"]

            inn = org_data.get("inn")
            if not inn:
                continue

            head_name = org_data.get("management")
            if head_name:
                head_name = head_name.get("name")

            suggest = OrganizationSuggestion(
                tax_number=inn,
                name=org_data["name"]["short_with_opf"],
                head_name=head_name,
            )
            res.append(suggest)

        return res


dadata = Dadata()
