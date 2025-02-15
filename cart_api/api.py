import falcon
from swagger_ui import falcon_api_doc
from cart_api.routes.heartbeat import Heartbeat
from cart_api.routes.products import Product, Products
from cart_api.routes.cartitems import CartItem, CartItems
from cart_api.routes.customer import Customer, Customers

# Instantiate RESTful API and resources
api = falcon.App(cors_enable=True)
api.req_options.strip_url_path_trailing_slash = True
hb = Heartbeat()
product = Product()
products = Products()
cartitem = CartItem()
cartitems = CartItems()
customer = Customer()
customers = Customers()

# Define our API's routes
api.add_route("/heartbeat", hb)
api.add_route("/v1/products/{product_id:int}", product)
api.add_route("/v1/products", Products())
api.add_route("/v1/cartitems/{cartitem_id:int}", cartitem)
api.add_route("/v1/cartitems", cartitems)
api.add_route("/v1/customer/{customer_id:int}", customer)
api.add_route("/v1/customers", Customers())

# Add a route which serves our OpenAPI specification
falcon_api_doc(
    api, config_path="/swagger/api.json", url_prefix="/", title="Cart API", editor=True
)


# Add custom error handling
def http405(req, resp, error, params):
    """Intercept any 405 type errors and return json"""
    resp.status = falcon.HTTP_405
    resp.media = {
        "code": "405_METHOD_NOT_ALLOWED",
        "message": "Cannot perform " + req.method + " on " + req.url,
    }


api.add_error_handler(falcon.HTTPMethodNotAllowed, http405)