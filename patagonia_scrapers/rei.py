import requests as req
from bs4 import BeautifulSoup as bs 
import csv
# opts = Options()
# opts.headless=True
# opts.add_argument("--window-size=1920,1200")

# DRIVER_PATH = "/opt/homebrew/bin/chromedriver"
# driver = webdriver.Chrome(options=opts, executable_path=DRIVER_PATH)
# URL ="https://google.com"
# driver.get(URL)
# driver.find_elements(By.)
# soup = bs
REI_PRODUCTS = []

"""
DATA STRUCTURE
{
    "product_brand": "",
    "product_title": "",
    "product_type": "",
    "product_units": "", -> What counts as a unit?
    "color": "",
    "gender": "", -> M, F, U

}
"""

def get_gender(title):
    if "Men" in title or "Boy" in title:
        return "M"
    if "Women" in title or "Girl" in title:
        return "F"
    else:
        return "U"

def get_product_data(product_span, color_group):
    colors = color_group.find_all("button")
    for color in colors:
        if "title" not in color.attrs:
            break
        if color.attrs["title"] is None:
            break
        product_data = {}
        product_data["product_brand"] = product_span[0].text
        title = product_span[1].text
        product_data["product_title"] =  title
        if " - " not in title:
            print("title does not have -:", title)
            continue
        title_parts = title.split(" ")
        product_type_idx = title_parts.index("-")-1
        product_data["product_type"] = title_parts[product_type_idx]
        # product_data["product_units"] = None
        product_data["color"] = color.attrs["title"]
        product_data["gender"] = "M" if "Men's" in title else "F" if "Women's" in title else "U"
        REI_PRODUCTS.append(product_data)

def beautiful_soup(response):
    html = bs(response.text, "html.parser")
    grid_container = html.find("ul", {"class": "cdr-grid_11-1-0 cdr-grid--gutter-medium@xs_11-1-0 cdr-grid--gutter-medium@sm_11-1-0 cdr-grid--gutter-large@md_11-1-0 cdr-grid--gutter-large@lg_11-1-0 _9LGEi0F4X4AsY1DIaa70j"})
    products = grid_container.find_all("li")
    filtered_products = []

    for product in products:
        # only append product if the class starts with letter 'p'
        if product is not None and "class" in product.attrs and product.attrs["class"][0].startswith("p"):
            filtered_products.append(product)    
    # filtered_products = filtered_products[:-1] # remove last product 'None'
    for fp in filtered_products:
        color_swatches_outer = fp.find("div", {"class": "_2aWU30tKwoW1olResC5Lft"})
        color_swatches_inner = color_swatches_outer.find("div", {"class": "_2sIPWBiJ_TDDUYIdkkEEah"})
        color_group = color_swatches_inner.find("div", {"role": "group"})

        product_desc = fp.find("a", {"class": "_1A-arB0CEJjk5iTZIRpjPs _2gicqyVSZCnmQ7-YrmbwIl"})
        product_desc_h2 = product_desc.find("h2", {"class": "dl_7C8km92zuNzeZlZyS2"})
        product_span = product_desc_h2.find_all("span")
        if color_group is not None:
            get_product_data(product_span, color_group)

    return

PATAGONIA_URL = "https://www.rei.com/b/patagonia/c/all?ir=brand%3Apatagonia&pagesize=90"
for page in range(1, 7):
    if page > 1:
        r = req.get("{}&page={}".format(PATAGONIA_URL, page))
        beautiful_soup(r)
    else:
        r = req.get(PATAGONIA_URL)
        beautiful_soup(r)



csv_file = "REI_Patagonia_Products.csv"
csv_columns = ["product_brand", "product_title", "product_type", "color", "gender"]
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in REI_PRODUCTS:
        writer.writerow(data)

