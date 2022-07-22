import falcon
from playhouse.shortcuts import model_to_dict
from cart_api.database import DatabaseCustomer


class Customer:
    def on_get(self, req, resp, customer_id):
        customer = DatabaseCustomer.get(id=customer_id)
        resp.media = model_to_dict(customer)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, customer_id):
        DatabaseCustomer.delete_by_id(customer_id)
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, customer_id):
        customer = DatabaseCustomer.get(id=customer_id)
        changes = req.media
        if "name" in changes:
            customer.quantity = changes["name"]
            customer.save()
        resp.status = falcon.HTTP_204

class Customers:
    def on_get(self, req, resp):
        response = []
        all_customers = DatabaseCustomer.select()
        for customer in all_customers:
            response.append(model_to_dict(customer))
        resp.media = response
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        new_customer = req.get_media()
        new_model = DatabaseCustomer(
            name=new_customer["name"],
            username=new_customer["username"],
            password=new_customer["password"],
            cart_id=new_customer["cart_id"]
        )
        new_model.save()
        resp.media = model_to_dict(new_model)
        resp.status = falcon.HTTP_201