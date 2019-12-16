def test_schedule_email_by_eta(client, faker):
    resp = client.post('/email/schedule',
                       json={
                           'to': faker.email,
                           'eta': str(faker.datetime),
                           'body': faker.text,
                           'subject': faker.title
                       })
    assert resp.status_code == 200


def test_schedule_email_by_eta_failed(client, faker):
    pass


def test_schedule_email_by_countdown(client, faker):
    pass
