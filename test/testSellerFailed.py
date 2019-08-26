import json
from . import app, client, cache, create_token_buyer, create_token_seller


class TestFailedEvent():
    #get all myshop item non seller
    def test_get_all_myshop_item(self, client):
        token = create_token_buyer()
        url = '/user/myshop'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.get(url, headers = h)
        assert res.status_code == 200

    #get a shop item nonseller
    def test_get_a_shop_item(self, client):
        token = create_token_buyer()
        url = '/user/myshop/1'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.patch(url, headers = h)
        assert res.status_code == 200

    #edit item in shop nonseller
    def test_edit_item_in_shop(self, client):
        token = create_token_buyer()
        url = '/user/myshop/1'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'nama_barang': 'Baju',
            'harga_satuan': 2000,
            'qty': 10,
            'url_image': 'https://m.media-amazon.com/images/I/A13usaonutL._CLa%7C2140,2000%7C61hLBkLke6L.png%7C0,0,2140,2000+0.0,0.0,2140.0,2000.0._UX342_.png'
        }
        res = client.put(url, headers = h, json = data)
        assert res.status_code == 200

    #add item to shop nonseller
    def test_add_item_to_shop(self, client):
        token = create_token_buyer()
        url = '/user/myshop'
        h = {
            'Authorization': 'Bearer '+token
        }
        data = {
            'nama_barang': 'Kolor',
            'harga_satuan': 5000,
            'qty': 6,
            'url_image': 'https://cf.shopee.co.id/file/dec4af673399ad72e95bd3811b669e6e'
        }
        res = client.post(url, headers = h, json = data)
        assert res.status_code == 200

    #delete item in shop nonseller
    def test_delete_item_in_shop(self, client):
        token = create_token_buyer()
        url = '/user/myshop/8'
        h = {
            'Authorization': 'Bearer '+token
        }
        res = client.delete(url, headers = h)
        assert res.status_code == 200