import faker
import simpy
from random import randint, choice, random
from src.api import get_random_photo, get_photos_of_customers, get_product_by_id, get_accessories
from src.recognizer import recognizer
from src.functions import typewriter, typewriter_colorful, separator, align_center, clean_align_center

PROBABILITY_OF_A_CUSTOMER_HAVING_A_DEBT = 15
PROBABILITY_OF_A_CUSTOMER_HAVING_A_WITHDRAWAL = 40 
TIME_BETWEEN_VISITS = 10
NUMBER_OF_CICLOS = 100

SIZE_TO_ALIGN = 100

def start():
    global customer
    customer = {}
    
    global recognized_customers_list
    recognized_customers_list = []
    
    global report_of_old_purchases
    report_of_old_purchases = []
    
    global report_of_related_product
    report_of_related_product = []
    
    global withdrawal
    
    global good_customer
    
    global fake_data_generator
    fake_data_generator = faker.Faker(locale="pt_BR")


def simulate_visit():
    visitor = {
        "photo": get_random_photo(),
        "information": None
    }
    
    return visitor
    
def simulate_acquisition():
    acquisition_number = randint(1, 8)
    acquisition = []
    
    for i in range(0, acquisition_number):
        acquisition.append(randint(1, 8))

    return acquisition

def simulate_debt(acquisition):
    probability = randint(1, 100)
    debt = 0
    
    if acquisition:
        if probability <= PROBABILITY_OF_A_CUSTOMER_HAVING_A_DEBT:
            debt = randint(1, 1000) + round(random(), 2)
    
    return debt

def simulate_withdrawal(acquisition):
    withdrawal = "no"
    probability = randint(1, 100)
    
    if probability <= PROBABILITY_OF_A_CUSTOMER_HAVING_A_WITHDRAWAL:
        if acquisition:
            id = choice(acquisition)
            withdrawal = get_product_by_id(id)["product"]
    
    return withdrawal

def generate_customer(visitor):
    customer = visitor
    customer["information"] = {}
    customer["information"]["name"] = fake_data_generator.name()
    customer["information"]["acquisition"] = simulate_acquisition()
    acquisition = customer["information"]["acquisition"]
    customer["information"]["withdrawal"] = simulate_withdrawal(acquisition)
    customer["information"]["debt"] = simulate_debt(acquisition)
    
    return customer

def recognize_visitor(env):
    global fake_data_generator 
    global customer
    global recognized_customers_list
    
    while True:
        if(env.now == 0):
            separator(1, SIZE_TO_ALIGN)
        
        print("Reconhecendo um cliente no ciclo/tempo:", env.now, "qtd reconhecidos até agora:",len(recognized_customers_list))
        photos = get_photos_of_customers()
        visitor = simulate_visit()
        visitor_photo = visitor["photo"]
        
        recognized = recognizer(visitor_photo, photos)
        if recognized:
            customer = generate_customer(visitor)

            typewriter_colorful("Cliente com nome: " + customer["information"]["name"] + " encontrado.", 1)
            print()
            
        else:
            typewriter_colorful("Ninguém foi reconhecido no tempo: " + str(env.now), 0)
        yield env.timeout(TIME_BETWEEN_VISITS)

def generate_old_purchases_report(old_purchases_list):
    old_purchases = []
    
    for id in old_purchases_list:
        old_purchases.append(get_product_by_id(id))
    
    return old_purchases

def checks_old_purchases(env):
    global customer
    global report_of_old_purchases
    
    while True:
        if len(customer):
            typewriter("Verificando compras antigas feitas por " + customer["information"]["name"] + ".")
            typewriter("Gerando relatório...")
            print()
            report_of_old_purchases = generate_old_purchases_report(customer["information"]["acquisition"])

            yield env.timeout(TIME_BETWEEN_VISITS)
        else:
            yield env.timeout(1)

def format_product_to_report(product):
    product_to_return = {}
    product_to_return["id"] = product["id"]
    product_to_return["name"] = product["product"]
    
    return product_to_return

def generate_related_product_report(report_of_old_purchases):
    product_with_related_products = []
    
    for product in report_of_old_purchases:
        product_= format_product_to_report(product)
        accessories = []
        
        if len(product["accessories"]):
            accessories = []
            for accessory in get_accessories(product["id"]):
                accessory_ = format_product_to_report(accessory)
                accessories.append(accessory_)
        else:
            accessories = None
        
        product_["accessories"] = accessories
        product_with_related_products.append(product_)
    
    return product_with_related_products

def checks_related_product(env):
    global report_of_old_purchases
    global report_of_related_product
    global customer
    
    while True:
        if len(report_of_old_purchases):
            typewriter("Verificando produtos relacionados às últimas compras.")
            typewriter("Adicionando dados ao relatório...")
            print()
            report_of_related_product = generate_related_product_report(report_of_old_purchases)
            yield env.timeout(TIME_BETWEEN_VISITS)
        else:
            yield env.timeout(1)
        
def checks_withdrawal(env):
    global customer
    global withdrawal
    
    while True:
        if customer:
            typewriter("Verificando retiradas em nome de "+customer["information"]["name"]+".")
            typewriter("Adicionando dados ao relatório...")
            print()
            withdrawal = customer["information"]["withdrawal"]
            yield env.timeout(TIME_BETWEEN_VISITS)
        else:
            yield env.timeout(1)

def is_a_good_customer(env):
    global good_customer
    global customer
    
    while True:
        if customer:
            typewriter("Verificando histórico de bom cliente de " + customer["information"]["name"] + ".")
            typewriter("Adicionando dados ao relatório...")
            print()
            debt = customer["information"]["debt"] 
            if debt > 0:
                good_customer = f"Não, cliente possui uma divida de: {debt}"
            else:
                good_customer = "Sim, cliente não possui divida"
            yield env.timeout(TIME_BETWEEN_VISITS)    
        else:
            yield env.timeout(1)    

def trigger_responsible_for_the_sector(env):
    global withdrawal
    global customer
    
    while True:
        if customer:
            withdrawal = customer["information"]["withdrawal"]
            if withdrawal != "no":
                typewriter("Acionando responsável pelo setor de retiradas.")
                typewriter("O cliente: " + customer["information"]["name"] + " chegou para retirar o produto: " + withdrawal)
                print()
            yield env.timeout(TIME_BETWEEN_VISITS)
        else:
            yield env.timeout(1)

def header(name):
    align_center("RELATÓRIO COMPLETO PARA: "+ name.upper(),SIZE_TO_ALIGN)

def print_product(product):
    print()
    print("     Id do produto:", product["id"])
    print("     Produto:", product["name"])

def format_accessories(accessories):
    data = "Acessórios: [Não possui acessórios"
    
    if accessories:
        data = "Acessórios: ["
        for i in range(0, len(accessories)):
            if i < len(accessories)-1:
                product = accessories[i]
                data += product["name"] + ", "
            else:
                product = accessories[i]
                data += product["name"]
    data += "]"
    
    return data

def print_product_report(report_data):
    for product in report_data:
        print_product(product)
        accessories = format_accessories(product["accessories"])
        print("     "+accessories)

def body(report_of_related_product, withdrawal, good_customer):
    print("PRODUTO E SEUS ACESSÓRIOS:")
    print_product_report(report_of_related_product)
    print("\nRETIRADA DE PRODUTO:", withdrawal)
    print("\nBOM CLIENTE:", good_customer)

def footer():
    print()
    clean_align_center("FIM DO RELATÓRIO", SIZE_TO_ALIGN)
    print()

# clear data from the previous customer
def clear_previous_customer():
    global customer
    global report_of_old_purchases
    global report_of_related_product
    global recognized_customers_list
    
    recognized_customers_list.append(customer)
    customer = {}
    report_of_old_purchases = []
    report_of_related_product = []

def final_report(env):
    global customer
    global report_of_related_product
    global withdrawal
    global good_customer
    
    while True:
        if customer:
            print()
            typewriter("Imprimindo relatório final...")
            print()
            header(customer["information"]["name"])
            body(report_of_related_product, withdrawal, good_customer)
            footer()
            clear_previous_customer()
            yield env.timeout(TIME_BETWEEN_VISITS)
        else:
            yield env.timeout(1)
            

def run():
    try:
        env = simpy.Environment()
        # recognize a visitor as a customer
        env.process(recognize_visitor(env))
        # Checks for old purchases
        env.process(checks_old_purchases(env))
        # Checks for any products related to another purchase
        env.process(checks_related_product(env))
        # Checks if the customer has any products for withdrawal
        env.process(checks_withdrawal(env))
        # Action responsible for the withdrawal sector
        env.process(trigger_responsible_for_the_sector(env))
        # Checks if the customer is a good customer
        env.process(is_a_good_customer(env))
        # Print customer's final report
        env.process(final_report(env))
        
        env.run(until=NUMBER_OF_CICLOS)

    except KeyboardInterrupt:
        print("Thanks you!")

if __name__ == "__main__":
    start()
    run()