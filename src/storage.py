from src.models import Company


class CompanyStore:
    def __init__(self) -> None:
        self.companies: dict[str, Company] = {}

    def add(self, company_id: str, company_data: Company) -> None:
        self.companies[company_id] = company_data

    def get(self, company_id: str) -> Company | None:
        return self.companies.get(company_id)

    def search_by_sector(self, sector: str) -> list[Company]:
        return [c for c in self.companies.values() if c.sector.lower() == sector.lower()]

    def search_by_name(self, name: str) -> list[Company]:
        return [c for c in self.companies.values() if name.lower() in c.name.lower()]

    def list_all(self) -> list[Company]:
        return list(self.companies.values())