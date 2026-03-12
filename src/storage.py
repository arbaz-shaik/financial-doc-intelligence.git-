class CompanyStore:
    def __init__(self):
        self.companies = {}

    def add(self, company_id, company_data):
        self.companies[company_id] = company_data

    def get(self, company_id):
        return self.companies.get(company_id)
