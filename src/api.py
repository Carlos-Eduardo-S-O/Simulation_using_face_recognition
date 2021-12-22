from json import load
from random import choice

CUSTOMERS_PATH = "assets/dictionaries/customers.json"
PRODUCTS_PATH = "assets/dictionaries/products.json"
SECTORS_PATH  = "assets/dictionaries/sectors.json"
VISITORS_PATH = "assets/dictionaries/visitors.json"

def get_visitors():
    visitors_list = []
    
    with open(VISITORS_PATH, "r") as visitors_file:
        visitors = load(visitors_file)
        
        visitors_list = visitors["information"]
        
        visitors_file.close()
        
    return visitors_list

def get_customers():
    customers_list = []
    
    with open(CUSTOMERS_PATH, "r") as customers_file:
        customers = load(customers_file)
        
        customers_list = customers["information"]
        
        customers_file.close()
        
    return customers_list

def get_photos_of_customers():
    custumer_list = get_customers()
    photo_list = []

    for custumer in custumer_list:
        for photo in custumer["photos"]:
            photo_list.append(
                {
                    "photo": photo
                })
    
    return photo_list

def get_all_photos():
    visitors_list = get_visitors()
    photo_list = []

    for visitors in visitors_list:
        for photo in visitors["photos"]:
            photo_list.append(
                {
                    "photo": photo
                })
    
    return photo_list
    
def get_random_photo():
    photo_list = get_all_photos()
    
    return choice(photo_list)["photo"]
    
def get_products():
    product_list = []

    with open(PRODUCTS_PATH, "r") as products_file:
        products = load(products_file)
        
        product_list = products["products"]
        
        products_file.close()

    return product_list

def get_product_by_id(id):
    product_list = get_products()
    product_to_return = None
    
    for product in product_list:
        if product["id"] == id:
            product_to_return = product
            break
    
    return product_to_return

def get_product_name(id):
    name = get_product_by_id(id)
    
    return name

def get_accessories(id):
    accessories_list = get_product_by_id(id)["accessories"] 
    accessories_to_return = []
    
    for accessory in accessories_list:
        accessories_to_return.append(get_product_by_id(accessory))
    
    return accessories_to_return

