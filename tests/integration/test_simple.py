
def test_simple(client):
    response = client.post(
        'v1/prescriptions',
        headers={"Content-Type": "application/json"},
        json={'foo': 'bar'}
    )
    assert response.json() == {'foo': 'bar'}
