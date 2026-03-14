class CompanyStore:
    def __init__(self):
        self.companies = {}

    def add(self, company_id, company_data):
        self.companies[company_id] = company_data

    def get(self, company_id):
        return self.companies.get(company_id)
    
    def search_by_sector(self, sector):
        return [company for company in self.companies.values() if company.sector.lower() == sector.lower()]
    
    def search_by_name(self,name):
        return[company for company in self.companies.values() if name.lower() in company.name.lower()]
    
    def search_by_ticker(self,ticker):
        return[company for company in self.companies.values() if ticker.lower() == company.ticker.lower()]

