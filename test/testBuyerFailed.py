import json
from . import app, client, cache, create_token_buyer, create_token_seller, create_token_not_enough_saldo


class TestFailedEvent():
    # signup already taken
    def test_failed_signup(self, client):
        token = create_token_buyer()
        url = '/welcome/signup'
        data = {
            'nama': 'tes',
            'email': 'tes@tes.com',
            'password': 'tes'
        }
        res = client.post(url, json=data)
        assert res.status_code == 200

    # get user status
    def test_failed_get_user_status(self, client):
        token = create_token_buyer()
        url = '/user/status'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers = h)
        assert res.status_code == 200


    # get all item
    def test_failed_get_all_item(self, client):
        token = create_token_buyer()
        res = client.get(
            '/user/all', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200

    # qty invalid
    def test_failed_add_to_bag(self, client):
        token = create_token_buyer()
        url1='/user/beli/1'
        url2='/user/beli/2'
        data = {
            'qty': -1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    #get all item in shopping bag
    def test_failed_get_all_item_in_bag(self, client):
        token = create_token_buyer()
        url='/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers=h)
        assert res.status_code == 200

    #edit item in shopping bag qty invalid
    def test_failed_edit_item_in_bag(self, client):
        token = create_token_buyer()
        url='/user/nota/1'
        data = {
            'qty': -1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.put(url, json=data, headers=h)
        assert res.status_code == 500

    #delete item in shopping bag no header
    def test_failed_delete_item_in_bag(self, client):
        token = create_token_buyer()
        url = '/user/nota/2'
        h = {
            'Authorization': 'Bearer '
        }
        res = client.patch(url, headers=h)
        assert res.status_code == 500

    #pay not enough saldo
    def test_failed_pay(self, client):
        token = create_token_not_enough_saldo()
        url = '/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 400


    #be a seller not enough saldo
    def test_failed_be_a_seller(self, client):
        token = create_token_not_enough_saldo()
        url = '/user/status'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 200

    #give rating already give rating
    def test_failed_give_rating(self, client):
        token = create_token_buyer()
        url = '/user/give_rating/2'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'rating': 10
        }
        res = client.post(url, headers=h, json=data)
        assert res.status_code == 200