import json
from . import app, client, cache, create_token_buyer, create_token_seller


class TestSuccessEvent():
    # signup
    def test_signup(self, client):
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
    def test_get_user_status(self, client):
        token = create_token_buyer()
        url = '/user/status'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers = h)
        assert res.status_code == 200


    # get all item
    def test_get_all_item(self, client):
        token = create_token_buyer()
        res = client.get(
            '/user/all', headers={'Authorization': 'Bearer '+token})
        assert res.status_code == 200

    # add to shopping bag
    def test_add_to_bag(self, client):
        token = create_token_buyer()
        url1='/user/beli/1'
        url2='/user/beli/2'
        data = {
            'qty': 1
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url1,query_string=data, headers=h)
        res = client.get(url2,query_string=data, headers=h)        
        assert res.status_code == 200

    #get all item in shopping bag
    def test_get_all_item_in_bag(self, client):
        token = create_token_buyer()
        url='/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers=h)
        assert res.status_code == 200

    #edit item in shopping bag
    def test_edit_item_in_bag(self, client):
        token = create_token_buyer()
        url='/user/nota/1'
        data = {
            'qty': 2
        }
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.put(url, json=data, headers=h)
        assert res.status_code == 200

    #delete item in shopping bag
    def test_delete_item_in_bag(self, client):
        token = create_token_buyer()
        url = '/user/nota/2'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.patch(url, headers=h)
        assert res.status_code == 200

    #pay
    def test_pay(self, client):
        token = create_token_buyer()
        url = '/user/nota/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 200

    #get all transactions
    def test_get_all_transactions(self, client):
        token = create_token_buyer()
        url = '/user/transactions'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers=h)
        assert res.status_code == 200


    #topup
    def test_topup(self, client):
        token = create_token_buyer()
        url = '/user/topup'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'topup': 10000
        }
        res = client.put(url, json=data, headers=h)
        assert res.status_code == 200

    #be a seller
    def test_be_a_seller(self, client):
        token = create_token_buyer()
        url = '/user/status'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.post(url, headers=h)
        assert res.status_code == 200

    #give rating
    def test_give_rating(self, client):
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

    #search item
    def test_search_item(self, client):
        token = create_token_buyer()
        url = '/user/all'
        h = {
            'Authorization': 'Bearer '+token
        }
        params = {
            'text': 'o'
        }
        res = client.post(url, headers=h, query_string=params)
        assert res.status_code == 200