def test_get_people(client):
    company_id = client.get_company_id("aramco")
    assert len(client.search_people_by_company_id(company_id)) != 0

def test_get_emails(client):
    assert len(client.get_emails(["57dfa65ca6da980b2ffa8946"])) == 1
