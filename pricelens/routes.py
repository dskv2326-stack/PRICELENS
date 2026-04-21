from collections import defaultdict
from datetime import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func

from models import (
    Clothing,
    Gadgets,
    Grocery,
    User,
    UserHistory,
    db,
)


main_bp = Blueprint("main", __name__)
bcrypt = Bcrypt()
GROCERY_IMAGE_OVERRIDES = {
    "Aashirvaad Atta 5kg": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Wheat_flour.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Wheat_flour.jpg",
        "author": "Oliwier Brzezinski",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Tata Salt 1kg": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Iodized_salt_packet.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Iodized_salt_packet.jpg",
        "author": "Ethantrott",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Fortune Sunflower Oil 1L": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Bottle_1_liter_Sunflower_refined_oil.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Bottle_1_liter_Sunflower_refined_oil.jpg",
        "author": "Exgsp Gmbh LLC BOTTLE",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Amul Butter 500g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Butter_block.JPG",
        "source": "https://commons.wikimedia.org/wiki/File:Butter_block.JPG",
        "author": "Meanos",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/mark/1.0/",
    },
    "Mother Dairy Milk 1L": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Milk-bottle.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Milk-bottle.jpg",
        "author": "FiveRings",
        "license_name": "CC BY 3.0",
        "license_url": "https://creativecommons.org/licenses/by/3.0/",
    },
    "Saffola Oats 1kg": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Food_oat_oats.JPG",
        "source": "https://commons.wikimedia.org/wiki/File:Food_oat_oats.JPG",
        "author": "Logictheo",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Maggi Noodles Pack": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Maggi_noodles.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Maggi_noodles.jpg",
        "author": "Soorajsharma26",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "India Gate Basmati Rice 5kg": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Basmati_Rice_Bag_%2849906485468%29.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Basmati_Rice_Bag_(49906485468).jpg",
        "author": "Ajay Suresh",
        "license_name": "CC BY 2.0",
        "license_url": "https://creativecommons.org/licenses/by/2.0/",
    },
    "Patanjali Honey 500g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/HoneyJar.JPG",
        "source": "https://commons.wikimedia.org/wiki/File:HoneyJar.JPG",
        "author": "Vicki Nunn",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Surf Excel Detergent 2kg": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Laundry_detergent_1.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Laundry_detergent_1.jpg",
        "author": "MartinMerinsky",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Colgate Toothpaste 200g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Colgate_tandpasta_tube.JPG",
        "source": "https://commons.wikimedia.org/wiki/File:Colgate_tandpasta_tube.JPG",
        "author": "Unknown",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Nescafe Classic 100g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Nescaf%C3%A9_tin_Classic.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Nescaf%C3%A9_tin_Classic.jpg",
        "author": "Albertyanks",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Parle-G Biscuits Family Pack": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Parle-G_Biscuit.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Parle-G_Biscuit.jpg",
        "author": "Ashish Gupta",
        "license_name": "CC BY 2.0",
        "license_url": "https://creativecommons.org/licenses/by/2.0/",
    },
    "Kelloggs Corn Flakes 875g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Kellogg%27s_Corn_Flakes.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Kellogg%27s_Corn_Flakes.jpg",
        "author": "Stephen Fulljames",
        "license_name": "CC BY-SA 2.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/2.0/",
    },
    "Britannia Bread 400g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Loaf_Of_Bread.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Loaf_Of_Bread.jpg",
        "author": "congerdesign",
        "license_name": "CC0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Lipton Tea 250g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Lipton_tea_bag.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Lipton_tea_bag.jpg",
        "author": "BAGANIAH LAW",
        "license_name": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
    "Lays Potato Chips 52g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Lays.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Lays.jpg",
        "author": "Gaurav Dhwaj Khadka",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Dove Soap 75g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Dove_IIII.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Dove_IIII.jpg",
        "author": "Milad Mosapoor",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Head & Shoulders 340ml": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Head_%26_Shoulders_Shampoo_%2851013601187%29.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Head_%26_Shoulders_Shampoo_(51013601187).jpg",
        "author": "Ajay Suresh",
        "license_name": "CC BY 2.0",
        "license_url": "https://creativecommons.org/licenses/by/2.0/",
    },
    "Sensodyne Toothpaste 100g": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Sensodyne_toothpaste_Iran.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Sensodyne_toothpaste_Iran.jpg",
        "author": "Milad Mosapoor",
        "license_name": "Attribution (per file)",
        "license_url": "https://commons.wikimedia.org/wiki/File:Sensodyne_toothpaste_Iran.jpg",
    },
    "Rin Detergent 3kg": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Laundry_detergent_1.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Laundry_detergent_1.jpg",
        "author": "MartinMerinsky",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Vim Liquid 500ml": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/VIM_washing_powder.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:VIM_washing_powder.jpg",
        "author": "Ehamberg",
        "license_name": "CC BY-SA 3.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/3.0/",
    },
    "Real Fruit Juice 1L": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Orangejuice.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Orangejuice.jpg",
        "author": "rawpixel.com",
        "license_name": "CC0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
}


GADGETS_IMAGE_OVERRIDES = {
    'Apple iPhone 15 128GB': {
        'url': 'images/gadgets/Smartphone_with_Android.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smartphone_with_Android.jpg',
        'author': 'Vonguru',
        'license_name': 'CC BY-SA 2.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/2.0/',
    },
    'Samsung Galaxy S24': {
        'url': 'images/gadgets/Smartphone_with_Android.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smartphone_with_Android.jpg',
        'author': 'Vonguru',
        'license_name': 'CC BY-SA 2.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/2.0/',
    },
    'OnePlus 12': {
        'url': 'images/gadgets/Smartphone_with_Android.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smartphone_with_Android.jpg',
        'author': 'Vonguru',
        'license_name': 'CC BY-SA 2.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/2.0/',
    },
    'Nothing Phone 2': {
        'url': 'images/gadgets/Smartphone_with_Android.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smartphone_with_Android.jpg',
        'author': 'Vonguru',
        'license_name': 'CC BY-SA 2.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/2.0/',
    },
    'Redmi Note 13 Pro': {
        'url': 'images/gadgets/Smartphone_with_Android.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smartphone_with_Android.jpg',
        'author': 'Vonguru',
        'license_name': 'CC BY-SA 2.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/2.0/',
    },
    'iPhone 14 128GB': {
        'url': 'images/gadgets/Smartphone_with_Android.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smartphone_with_Android.jpg',
        'author': 'Vonguru',
        'license_name': 'CC BY-SA 2.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/2.0/',
    },
    'iPad Air M2': {
        'url': 'images/gadgets/Tablet.jpeg',
        'source': 'https://commons.wikimedia.org/wiki/File:Tablet.jpeg',
        'author': '???',
        'license_name': 'CC BY-SA 3.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/',
    },
    'MacBook Air M3': {
        'url': 'images/gadgets/Laptop_image.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Laptop_image.jpg',
        'author': 'Darakshanehaluddin',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'HP Pavilion 15': {
        'url': 'images/gadgets/Laptop_image.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Laptop_image.jpg',
        'author': 'Darakshanehaluddin',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Dell Inspiron Laptop': {
        'url': 'images/gadgets/Laptop_image.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Laptop_image.jpg',
        'author': 'Darakshanehaluddin',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'MacBook Pro M3': {
        'url': 'images/gadgets/Laptop_image.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Laptop_image.jpg',
        'author': 'Darakshanehaluddin',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Boat Airdopes 141': {
        'url': 'images/gadgets/Opera_TWS.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Opera_TWS.jpg',
        'author': 'The Final Checklist',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Samsung Galaxy Buds 2': {
        'url': 'images/gadgets/Opera_TWS.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Opera_TWS.jpg',
        'author': 'The Final Checklist',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'OnePlus Nord Buds 2': {
        'url': 'images/gadgets/Opera_TWS.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Opera_TWS.jpg',
        'author': 'The Final Checklist',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Sony WH-CH520': {
        'url': 'images/gadgets/Headphones_(56330).jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Headphones_(56330).jpg',
        'author': '17mdnasim89',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Samsung 55-inch 4K TV': {
        'url': 'images/gadgets/1990s_Television_Set.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:1990s_Television_Set.jpg',
        'author': 'ProtoKiwi',
        'license_name': 'CC BY 4.0',
        'license_url': 'https://creativecommons.org/licenses/by/4.0/',
    },
    'Mi Smart Band 8': {
        'url': 'images/gadgets/Smart_Watch.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smart_Watch.jpg',
        'author': 'hawkHD',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Apple Watch SE': {
        'url': 'images/gadgets/Smart_Watch.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smart_Watch.jpg',
        'author': 'hawkHD',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Noise ColorFit Pro 4': {
        'url': 'images/gadgets/Smart_Watch.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smart_Watch.jpg',
        'author': 'hawkHD',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Samsung Galaxy Watch 4': {
        'url': 'images/gadgets/Smart_Watch.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Smart_Watch.jpg',
        'author': 'hawkHD',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Canon EOS 1500D': {
        'url': 'images/gadgets/Canon_EOS_600D_with_EF-S_18-55mm.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Canon_EOS_600D_with_EF-S_18-55mm.jpg',
        'author': 'Wewa',
        'license_name': 'CC BY-SA 3.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/',
    },
    'Seagate 1TB SSD': {
        'url': 'images/gadgets/Intel_512G_M2_Solid_State_Drive.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Intel_512G_M2_Solid_State_Drive.jpg',
        'author': 'David290',
        'license_name': 'CC BY-SA 4.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
    },
    'WD Blue 1TB HDD': {
        'url': 'images/gadgets/Hard_drive.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Hard_drive.jpg',
        'author': 'Anselm Sch?ler',
        'license_name': 'CC BY-SA 4.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
    },
    'Logitech MX Master 3S': {
        'url': 'images/gadgets/Computer_mice.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Computer_mice.jpg',
        'author': 'George Hodan',
        'license_name': 'CC0',
        'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
    },
    'Logitech K380 Keyboard': {
        'url': 'images/gadgets/Computer_Keyboard.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:Computer_Keyboard.jpg',
        'author': 'Srini297',
        'license_name': 'CC BY-SA 4.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
    },
    'JBL Go 3 Speaker': {
        'url': 'images/gadgets/JBL_Flip_bluetooth_speaker.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:JBL_Flip_bluetooth_speaker.jpg',
        'author': 'Gpkp',
        'license_name': 'CC BY-SA 4.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/4.0/',
    },
    'SanDisk 128GB Pen Drive': {
        'url': 'images/gadgets/USB_flash_drive.jpg',
        'source': 'https://commons.wikimedia.org/wiki/File:USB_flash_drive.jpg',
        'author': 'Dori',
        'license_name': 'Public Domain',
        'license_url': 'https://creativecommons.org/publicdomain/mark/1.0/',
    },

    "Apple iPhone 15 128GB": {"url": "Gadgets_images/Iphone_13.jpeg"},
    "iPhone 14 128GB": {"url": "Gadgets_images/Iphone_13.jpeg"},
    "Samsung Galaxy S24": {"url": "Gadgets_images/Samsung_Galaxy.jpeg"},
    "OnePlus 12": {"url": "Gadgets_images/Oneplus.jpeg"},
    "Redmi Note 13 Pro": {"url": "Gadgets_images/Redmi.jpeg"},
    "MacBook Air M3": {"url": "Gadgets_images/Mac.jpeg"},
    "MacBook Pro M3": {"url": "Gadgets_images/Mac.jpeg"},
    "HP Pavilion 15": {"url": "Gadgets_images/Hp.jpeg"},
    "Dell Inspiron Laptop": {"url": "Gadgets_images/Del.jpeg"},
    "Boat Airdopes 141": {"url": "Gadgets_images/Boat_TWS.jpeg"},
    "Sony WH-CH520": {"url": "Gadgets_images/Sony_Headphone.jpeg"},
    "Samsung 55-inch 4K TV": {"url": "Gadgets_images/Xiaomi_Tv.jpeg"},
    "Noise ColorFit Pro 4": {"url": "Gadgets_images/Noise_Watch.jpeg"},

    # Local gadget images
    "Apple iPhone 13 128GB": {"url": "Gadgets_images/Iphone_13.jpeg"},
    "iPhone 13 128GB": {"url": "Gadgets_images/Iphone_13.jpeg"},
    "Samsung Galaxy S21 FE 128GB": {"url": "Gadgets_images/Samsung_Galaxy.jpeg"},
    "OnePlus Nord CE 3 Lite 128GB": {"url": "Gadgets_images/Oneplus.jpeg"},
    "Redmi Note 12 Pro 128GB": {"url": "Gadgets_images/Redmi.jpeg"},
    "Realme Narzo 60 128GB": {"url": "Gadgets_images/Realme_Narzo.jpeg"},
    "HP Pavilion Laptop 16GB RAM 512GB SSD": {"url": "Gadgets_images/Hp.jpeg"},
    "HP Pavilion Laptop 16GB 512GB": {"url": "Gadgets_images/Hp.jpeg"},
    "Dell Inspiron Laptop 8GB RAM 512GB SSD": {"url": "Gadgets_images/Del.jpeg"},
    "Dell Inspiron Laptop 8GB 512GB": {"url": "Gadgets_images/Del.jpeg"},
    "Apple MacBook Air M1 256GB SSD": {"url": "Gadgets_images/Mac.jpeg"},
    "MacBook Air M1 256GB": {"url": "Gadgets_images/Mac.jpeg"},
    "boAt Airdopes 141 Wireless Earbuds": {"url": "Gadgets_images/Boat_TWS.jpeg"},
    "Boat Airdopes 141": {"url": "Gadgets_images/Boat_TWS.jpeg"},
    "Sony WH-CH520 Wireless Headphones": {"url": "Gadgets_images/Sony_Headphone.jpeg"},
    "Sony WH-CH520 Headphones": {"url": "Gadgets_images/Sony_Headphone.jpeg"},
    "Noise Smartwatch": {"url": "Gadgets_images/Noise_Watch.jpeg"},
    "Mi Smart LED TV 43 inch": {"url": "Gadgets_images/Xiaomi_Tv.jpeg"},
}

CLOTHING_IMAGE_OVERRIDES = {
    "Mens Slim Fit Jeans": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Jeans.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Jeans.jpg",
        "author": "Oktaeder",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/mark/1.0/",
    },
    "Womens Kurti Set": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Kurta_Indian_Dress_for_Woman.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Kurta_Indian_Dress_for_Woman.jpg",
        "author": "satemkemet",
        "license_name": "CC BY-SA 2.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/2.0/",
    },
    "Mens Formal Shirt": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Dress_Shirt_%283161023616%29.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Dress_Shirt_(3161023616).jpg",
        "author": "Marcus Quigmire",
        "license_name": "CC BY-SA 2.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/2.0/",
    },
    "Womens Sneakers": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Sneakers_2.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Sneakers_2.jpg",
        "author": "Saffrondattal",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Unisex Hoodie": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Hoodie_with_print.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Hoodie_with_print.jpg",
        "author": "Doublecor",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Mens Running Shoes": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Running_shoes.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Running_shoes.jpg",
        "author": "Tiia Monto",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Womens Denim Jacket": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Denim_Jacket_%2851079649933%29.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Denim_Jacket_(51079649933).jpg",
        "author": "ajay_suresh",
        "license_name": "CC BY 2.0",
        "license_url": "https://creativecommons.org/licenses/by/2.0/",
    },
    "Mens Polo T-Shirt": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Polo_Shirt_%E2%80%A2_public_domain_vector_image.svg",
        "source": "https://commons.wikimedia.org/wiki/File:Polo_Shirt_%E2%80%A2_public_domain_vector_image.svg",
        "author": "OpenClipartVectors",
        "license_name": "CC0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Womens Palazzo Pants": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Palazzo_trousers.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Palazzo_trousers.jpg",
        "author": "David Ring",
        "license_name": "CC0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Kids School Uniform Set": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/School_uniform.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:School_uniform.jpg",
        "author": "Dad",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/mark/1.0/",
    },
    "Mens Ethnic Kurta": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Kurta_-_Mens.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Kurta_-_Mens.jpg",
        "author": "Veera.sj",
        "license_name": "CC0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Womens Saree": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Saree_image.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Saree_image.jpg",
        "author": "Mohanraj55",
        "license_name": "CC0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Mens Blazer": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Navy_blazer_jacket.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Navy_blazer_jacket.jpg",
        "author": "????",
        "license_name": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    },
    "Womens Activewear Leggings": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Leggings.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Leggings.jpg",
        "author": "lebonbonmulticolore",
        "license_name": "CC BY 2.0",
        "license_url": "https://creativecommons.org/licenses/by/2.0/",
    },
    "Mens Casual Jacket": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Bomber_jacket.jpg",
        "source": "https://commons.wikimedia.org/wiki/File:Bomber_jacket.jpg",
        "author": "Spazzo",
        "license_name": "Public Domain",
        "license_url": "https://creativecommons.org/publicdomain/mark/1.0/",
    },
    "Levis Graphic T-Shirt": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/T-shirt_brand_graphic_-_Wikimedia_Foundation.png",
        "source": "https://commons.wikimedia.org/wiki/File:T-shirt_brand_graphic_-_Wikimedia_Foundation.png",
        "author": "Jasmina El Bouamraoui; Karabo Poppy Moletsane",
        "license_name": "CC0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    },
    "Adidas Ultraboost Shoes": {
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Adidas_shoe.JPG",
        "source": "https://commons.wikimedia.org/wiki/File:Adidas_shoe.JPG",
        "author": "ChickenFalls",
        "license_name": "CC BY-SA 3.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/3.0/",
    },
    "Allen Solly Formal Shirt Size L": {
        "url": "Clothing_images/Allen solly formal shirt.jpeg",
    },
    "Puma Hoodie Size L": {
        "url": "Clothing_images/Puma Hoodie.jpeg",
    },
    "Biba Kurti Size M": {
        "url": "Clothing_images/Biba kurti.jpeg",
    },
    "Nike Sports T-Shirt Size M": {
        "url": "Clothing_images/Nike sports tshirt.jpeg",
    },
    "Van Heusen Trousers Size 34": {
        "url": "Clothing_images/Van Heusan.jpeg",
    },
    "Adidas Track Pants Size M": {
        "url": "Clothing_images/Adidas track pant.jpeg",
    },
    "Roadster Denim Jacket Size L": {
        "url": "Clothing_images/Roadstarr Dmein jacket.jpeg",
    },
    "Fabindia Kurta Size XL": {
        "url": "Clothing_images/Fabindia Kurta.jpeg",
    },
    "Zara Casual Shirt Size L": {
        "url": "Clothing_images/Zara casual shirt.jpeg",
    },
    "Levis Slim Fit Jeans Size 32": {
        "url": "Clothing_images/Levi Slim fit jeans.jpeg",
    },
    "H&M Cotton T-Shirt Size M": {
        "url": "Clothing_images/H&M cotton tshirt.jpeg",
    },
    "W Printed Kurta Size L": {
        "url": "Clothing_images/W printed Kurta.jpeg",
    },}

IMAGE_OVERRIDES = {
    "Grocery": GROCERY_IMAGE_OVERRIDES,
    "Clothing": CLOTHING_IMAGE_OVERRIDES,
    "Gadgets": GADGETS_IMAGE_OVERRIDES,
}


CATEGORY_MODELS = {
    "Grocery": Grocery,
    "Clothing": Clothing,
    "Gadgets": Gadgets,
}

CATEGORY_PRICE_FIELDS = {
    "Grocery": [("Blinkit", "blinkit_price"), ("Zepto", "zepto_price"), ("Instamart", "instamart_price")],
    "Clothing": [("Ajio", "ajio_price"), ("Myntra", "myntra_price")],
    "Gadgets": [("Amazon", "amazon_price"), ("Flipkart", "flipkart_price")],
}


def _resolve_image_url(product):
    if product.category == "Grocery":
        return product.image_url
    overrides = IMAGE_OVERRIDES.get(product.category)
    if overrides:
        override = overrides.get(product.name)
        if override:
            return override["url"]
    return product.image_url



def _product_prices(product):
    fields = CATEGORY_PRICE_FIELDS.get(product.category, [])
    rows = []
    for platform, field in fields:
        value = getattr(product, field, None)
        if value is None:
            continue
        rows.append({
            "platform": platform,
            "price": float(value),
            "is_cheapest": False,
            "last_updated": "-",
        })
    rows = sorted(rows, key=lambda x: x["price"])
    if rows:
        rows[0]["is_cheapest"] = True
    return rows


def _product_card_data(product):
    prices = _product_prices(product)
    cheapest = prices[0] if prices else None
    cheapest_platform = cheapest["platform"] if cheapest else None
    return {
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "category": product.category,
        "image_url": _resolve_image_url(product),
        "cheapest_price": cheapest["price"] if cheapest else None,
        "cheapest_platform": cheapest_platform,
        "last_updated": cheapest["last_updated"] if cheapest else "-",
        "prices": prices,
    }


def _record_user_history(user_id, category, product_id, auto_commit=True):
    entry = (
        UserHistory.query.filter_by(user_id=user_id, category=category, product_id=product_id)
        .order_by(UserHistory.viewed_at.desc())
        .first()
    )


    now = datetime.utcnow()
    for price in prices:
        price.last_updated = now

    db.session.commit()
    flash("Saved latest prices for all products.", "success")
    return redirect(request.referrer or url_for("main.index"))



@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/")
def index():
    category_counts = {
        "Grocery": Grocery.query.count(),
        "Clothing": Clothing.query.count(),
        "Gadgets": Gadgets.query.count(),
    }

    preferred_order = [("Grocery", "Groceries"), ("Clothing", "Clothings"), ("Gadgets", "Gadgets")]
    category_sections = []
    for category, label in preferred_order:
        model = CATEGORY_MODELS.get(category)
        if not model:
            continue
        if category_counts.get(category, 0) == 0:
            continue
        section_products = model.query.order_by(func.random()).limit(4).all()
        category_sections.append({
            "name": category,
            "label": label,
            "products": [_product_card_data(p) for p in section_products],
        })

    return render_template(
        "index.html",
        category_counts=category_counts,
        category_sections=category_sections,
    )


@main_bp.route("/category/<string:category>")
def category(category):
    category_title = category.title()
    model = CATEGORY_MODELS.get(category_title)
    if not model:
        return render_template("category.html", category=category_title, products=[])
    products = model.query.order_by(func.random()).limit(12).all()
    product_cards = [_product_card_data(p) for p in products]
    return render_template(
        "category.html",
        category=category_title,
        products=product_cards,
    )


@main_bp.route("/product/<string:category>/<int:product_id>")
def product(category, product_id):
    category_title = category.title()
    model = CATEGORY_MODELS.get(category_title)
    if not model:
        return redirect(url_for("main.index"))
    item = model.query.get_or_404(product_id)
    prices = _product_prices(item)

    detailed_prices = prices

    if current_user.is_authenticated:
        _record_user_history(current_user.id, category_title, item.id)

    return render_template(
        "product.html",
        product=item,
        image_url=_resolve_image_url(item),
        prices=detailed_prices,
        cheapest=detailed_prices[0] if detailed_prices else None,
    )


@main_bp.route("/api/product/<string:category>/<int:product_id>/prices")
def product_prices(category, product_id):
    category_title = category.title()
    model = CATEGORY_MODELS.get(category_title)
    if not model:
        return jsonify({"prices": []})
    item = model.query.get_or_404(product_id)
    prices = _product_prices(item)
    response = jsonify({"prices": prices})
    response.headers["Cache-Control"] = "no-store"
    return response


@main_bp.route("/api/products/prices")
def products_prices():
    items_param = request.args.get("items", "")
    tokens = [t.strip() for t in items_param.split(',') if t.strip()]

    if not tokens:
        response = jsonify({"prices": {}})
        response.headers["Cache-Control"] = "no-store"
        return response

    data = {}
    for token in tokens:
        if ':' not in token:
            continue
        category, raw_id = token.split(':', 1)
        category_title = category.title()
        model = CATEGORY_MODELS.get(category_title)
        if not model:
            continue
        try:
            product_id = int(raw_id)
        except ValueError:
            continue
        item = model.query.get(product_id)
        if not item:
            continue
        prices = _product_prices(item)
        if not prices:
            continue
        cheapest = prices[0]
        data[f"{category_title}:{product_id}"] = {
            "cheapest_price": float(cheapest["price"]),
            "cheapest_platform": cheapest["platform"],
            "last_updated": cheapest["last_updated"],
        }

    response = jsonify({"prices": data})
    response.headers["Cache-Control"] = "no-store"
    return response


@main_bp.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    results = []
    for model in (Grocery, Clothing, Gadgets):
        matches = model.query.filter(model.product_name.ilike(f"%{query}%")).all()
        results.extend([_product_card_data(p) for p in matches])

    if current_user.is_authenticated:
        for result in results[:5]:
            _record_user_history(current_user.id, result["category"], result["id"], auto_commit=False)
        db.session.commit()

    return jsonify(results)

@main_bp.route("/admin/save-prices", methods=["POST"])
@login_required
def save_prices():
    flash("Price updates are managed in the database.", "info")
    return redirect(request.referrer or url_for("main.index"))


@main_bp.route("/history")
@login_required
def history():
    entries = (
        UserHistory.query.filter_by(user_id=current_user.id)
        .order_by(UserHistory.viewed_at.desc())
        .all()
    )

    view_data = []
    for entry in entries:
        model = CATEGORY_MODELS.get(entry.category)
        product = None
        if model:
            product = model.query.get(entry.product_id)
        if not product:
            for fallback_model in CATEGORY_MODELS.values():
                product = fallback_model.query.get(entry.product_id)
                if product:
                    break
        if not product:
            continue
        card = _product_card_data(product)
        card["viewed_at"] = entry.viewed_at.strftime("%d %b %Y, %I:%M %p")
        view_data.append(card)

    return render_template("history.html", entries=view_data)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
            return render_template("register.html")

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(name=name, email=email, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Welcome to PriceLens.", "success")
        return redirect(url_for("main.index"))

    return render_template("register.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Logged in successfully.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("main.index"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("main.index"))


def init_extensions(app):
    bcrypt.init_app(app)












