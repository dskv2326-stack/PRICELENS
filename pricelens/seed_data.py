from datetime import datetime
from decimal import Decimal
from pathlib import Path

from app import create_app
from models import (
    ClothingProduct,
    GadgetsProduct,
    GroceryProduct,
    Price,
    db,
)


PRODUCTS = [
    ("Aashirvaad Atta 5kg", "Aashirvaad", "Grocery", "aashirvaad-atta-5kg", [299, 305, 294]),
    ("Tata Salt 1kg", "Tata", "Grocery", "tata-salt-1kg", [28, 30, 29]),
    ("Fortune Sunflower Oil 1L", "Fortune", "Grocery", "fortune-sunflower-oil-1l", [158, 162, 155]),
    ("Amul Butter 500g", "Amul", "Grocery", "amul-butter-500g", [285, 291, 282]),
    ("Mother Dairy Milk 1L", "Mother Dairy", "Grocery", "mother-dairy-milk-1l", [66, 68, 65]),
    ("Saffola Oats 1kg", "Saffola", "Grocery", "saffola-oats-1kg", [199, 205, 194]),
    ("Maggi Noodles Pack", "Maggi", "Grocery", "maggi-noodles-pack", [72, 74, 70]),
    ("India Gate Basmati Rice 5kg", "India Gate", "Grocery", "india-gate-basmati-rice-5kg", [529, 538, 522]),
    ("Patanjali Honey 500g", "Patanjali", "Grocery", "patanjali-honey-500g", [179, 184, 176]),
    ("Surf Excel Detergent 2kg", "Surf Excel", "Grocery", "surf-excel-detergent-2kg", [389, 397, 380]),
    ("Colgate Toothpaste 200g", "Colgate", "Grocery", "colgate-toothpaste-200g", [118, 121, 116]),
    ("Nescafe Classic 100g", "Nescafe", "Grocery", "nescafe-classic-100g", [325, 332, 319]),
    ("Parle-G Biscuits Family Pack", "Parle", "Grocery", "parle-g-family-pack", [45, 47, 44]),
    ("Taj Mahal Tea 500g", "Taj Mahal", "Grocery", "taj-mahal-tea-500g", [312, 318, 307]),
    ("Kelloggs Corn Flakes 875g", "Kelloggs", "Grocery", "kelloggs-corn-flakes-875g", [368, 374, 360]),
    ("India Gate Basmati Rice 5kg", "India Gate", "Grocery", "india-gate-basmati-rice-5kg", [529, 538, 522]),
    ("Aashirvaad Whole Wheat Atta 5kg", "Aashirvaad", "Grocery", "aashirvaad-whole-wheat-atta-5kg", [299, 305, 294]),
    ("Fortune Sunflower Oil 1L", "Fortune", "Grocery", "fortune-sunflower-oil-1l", [158, 162, 155]),
    ("Amul Fresh Milk 1L", "Amul", "Grocery", "amul-fresh-milk-1l", [62, 64, 61]),
    ("Madhur Pure Sugar 1kg", "Madhur", "Grocery", "madhur-pure-sugar-1kg", [52, 54, 50]),
    ("Tata Iodized Salt 1kg", "Tata", "Grocery", "tata-iodized-salt-1kg", [28, 30, 29]),
    ("Suguna Farm Fresh Eggs 12 pcs", "Suguna", "Grocery", "suguna-farm-fresh-eggs-12pcs", [78, 82, 76]),
    ("Britannia Brown Bread 400g", "Britannia", "Grocery", "britannia-brown-bread-400g", [38, 40, 37]),
    ("Parle-G Biscuits Pack 100g", "Parle", "Grocery", "parle-g-biscuits-pack-100g", [10, 12, 9]),
    ("Surf Excel Easy Wash Detergent Powder 1kg", "Surf Excel", "Grocery", "surf-excel-easy-wash-1kg", [189, 195, 184]),
    ("Dove Cream Beauty Bath Soap 100g", "Dove", "Grocery", "dove-cream-beauty-bath-soap-100g", [58, 62, 55]),
    ("Colgate Strong Teeth Toothpaste 150g", "Colgate", "Grocery", "colgate-strong-teeth-toothpaste-150g", [95, 99, 92]),
    ("Apple iPhone 15 128GB", "Apple", "Gadgets", "iphone-15-128gb", [71999, 71499]),
    ("Samsung Galaxy S24", "Samsung", "Gadgets", "samsung-galaxy-s24", [68999, 68249]),
    ("OnePlus 12", "OnePlus", "Gadgets", "oneplus-12", [61999, 61499]),
    ("Nothing Phone 2", "Nothing", "Gadgets", "nothing-phone-2", [39999, 39499]),
    ("Redmi Note 13 Pro", "Xiaomi", "Gadgets", "redmi-note-13-pro", [26999, 26399]),
    ("iPad Air M2", "Apple", "Gadgets", "ipad-air-m2", [59999, 59249]),
    ("MacBook Air M3", "Apple", "Gadgets", "macbook-air-m3", [114999, 113499]),
    ("HP Pavilion 15", "HP", "Gadgets", "hp-pavilion-15", [70999, 69999]),
    ("Boat Airdopes 141", "Boat", "Gadgets", "boat-airdopes-141", [1299, 1249]),
    ("Sony WH-CH520", "Sony", "Gadgets", "sony-wh-ch520", [4199, 4099]),
    ("Samsung 55-inch 4K TV", "Samsung", "Gadgets", "samsung-55-4k-tv", [54999, 54199]),
    ("Mi Smart Band 8", "Xiaomi", "Gadgets", "mi-smart-band-8", [2999, 2899]),
    ("Canon EOS 1500D", "Canon", "Gadgets", "canon-eos-1500d", [39999, 39299]),
    ("Seagate 1TB SSD", "Seagate", "Gadgets", "seagate-1tb-ssd", [6499, 6329]),
    ("Logitech MX Master 3S", "Logitech", "Gadgets", "logitech-mx-master-3s", [8999, 8799]),
    ("Mens Slim Fit Jeans", "Levis", "Clothing", "mens-slim-fit-jeans", [1899, 1799]),
    ("Womens Kurti Set", "Biba", "Clothing", "womens-kurti-set", [1699, 1599]),
    ("Mens Formal Shirt", "Van Heusen", "Clothing", "mens-formal-shirt", [1499, 1399]),
    ("Womens Sneakers", "Puma", "Clothing", "womens-sneakers", [2499, 2399]),
    ("Unisex Hoodie", "H&M", "Clothing", "unisex-hoodie", [1999, 1899]),
    ("Mens Running Shoes", "Nike", "Clothing", "mens-running-shoes", [4599, 4399]),
    ("Womens Denim Jacket", "Only", "Clothing", "womens-denim-jacket", [2799, 2699]),
    ("Mens Polo T-Shirt", "U.S. Polo", "Clothing", "mens-polo-tshirt", [1199, 1099]),
    ("Womens Palazzo Pants", "W", "Clothing", "womens-palazzo-pants", [999, 949]),
    ("Kids School Uniform Set", "Allen Solly", "Clothing", "kids-school-uniform-set", [1499, 1429]),
    ("Mens Ethnic Kurta", "Manyavar", "Clothing", "mens-ethnic-kurta", [2199, 2099]),
    ("Womens Saree", "Sangria", "Clothing", "womens-saree", [2599, 2499]),
    ("Mens Blazer", "Raymond", "Clothing", "mens-blazer", [5299, 5099]),
    ("Womens Activewear Leggings", "Adidas", "Clothing", "womens-activewear-leggings", [1499, 1399]),
("Mens Casual Jacket", "Roadster", "Clothing", "mens-casual-jacket", [2999, 2849]),

    # Additional Grocery (+10)
    ("Britannia Bread 400g", "Britannia", "Grocery", "britannia-bread-400g", [38, 40, 37]),
    ("Lipton Tea 250g", "Lipton", "Grocery", "lipton-tea-250g", [189, 195, 184]),
    ("Good Day Biscuits 300g", "Britannia", "Grocery", "good-day-biscuits-300g", [58, 60, 56]),
    ("Lays Potato Chips 52g", "Lays", "Grocery", "lays-chips-52g", [22, 24, 20]),
    ("Dove Soap 75g", "Dove", "Grocery", "dove-soap-75g", [58, 62, 55]),
    ("Head & Shoulders 340ml", "Head & Shoulders", "Grocery", "head-shoulders-340ml", [389, 399, 379]),
    ("Sensodyne Toothpaste 100g", "Sensodyne", "Grocery", "sensodyne-toothpaste-100g", [168, 175, 162]),
    ("Rin Detergent 3kg", "Rin", "Grocery", "rin-detergent-3kg", [289, 298, 279]),
    ("Vim Liquid 500ml", "Vim", "Grocery", "vim-liquid-500ml", [169, 175, 164]),
    ("Real Fruit Juice 1L", "Real", "Grocery", "real-fruit-juice-1l", [89, 92, 86]),

    # Additional Gadgets (+12)
    ("Samsung Galaxy Buds 2", "Samsung", "Gadgets", "samsung-galaxy-buds2", [7999, 7799]),
    ("Apple Watch SE", "Apple", "Gadgets", "apple-watch-se", [24999, 23999]),
    ("Dell Inspiron Laptop", "Dell", "Gadgets", "dell-inspiron-laptop", [49999, 48999]),
    ("JBL Go 3 Speaker", "JBL", "Gadgets", "jbl-go3-speaker", [2499, 2299]),
    ("Noise ColorFit Pro 4", "Noise", "Gadgets", "noise-colorfit-pro4", [3999, 3699]),
    ("Samsung Galaxy Watch 4", "Samsung", "Gadgets", "samsung-galaxy-watch4", [18999, 17999]),
    ("OnePlus Nord Buds 2", "OnePlus", "Gadgets", "oneplus-nord-buds2", [2999, 2799]),
    ("iPhone 14 128GB", "Apple", "Gadgets", "iphone-14-128gb", [61999, 60999]),
    ("MacBook Pro M3", "Apple", "Gadgets", "macbook-pro-m3", [169999, 167999]),
    ("Logitech K380 Keyboard", "Logitech", "Gadgets", "logitech-k380-keyboard", [2999, 2799]),
    ("WD Blue 1TB HDD", "Western Digital", "Gadgets", "wd-blue-1tb-hdd", [4499, 4299]),
    ("SanDisk 128GB Pen Drive", "SanDisk", "Gadgets", "sandisk-128gb-pendrive", [999, 899]),

    # Additional Clothing (+13)
    ("Levis Graphic T-Shirt", "Levis", "Clothing", "levis-graphic-tshirt", [1299, 1199]),
    ("Adidas Ultraboost Shoes", "Adidas", "Clothing", "adidas-ultraboost-shoes", [12999, 12499]),


]

PLATFORMS = {
    "Grocery": ["Instamart", "Zepto", "Blinkit"],
    "Gadgets": ["Amazon", "Flipkart"],
    "Clothing": ["Myntra", "Ajio"],
}

CATEGORY_COLORS = {
    "Grocery": "#4b8f29",
    "Gadgets": "#1f6fb2",
    "Clothing": "#b04c79",
}


def _gadget_icon_svg(product_name: str, color: str) -> str:
    name = product_name.lower()

    if "watch" in name or "band" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="250" y="180" width="100" height="80" rx="16"/>  <rect x="270" y="140" width="60" height="40" rx="12"/>  <rect x="270" y="260" width="60" height="40" rx="12"/></g>'''
    if "buds" in name or "airdopes" in name or "wh-" in name or "head" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path d="M220 220a80 80 0 0 1 160 0"/>  <rect x="210" y="220" width="24" height="50" rx="8"/>  <rect x="366" y="220" width="24" height="50" rx="8"/></g>'''
    if "tv" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="215" y="160" width="170" height="100" rx="10"/>  <line x1="300" y1="260" x2="300" y2="285"/>  <line x1="250" y1="285" x2="350" y2="285"/></g>'''
    if "camera" in name or "eos" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="220" y="180" width="160" height="100" rx="12"/>  <circle cx="300" cy="230" r="30"/>  <rect x="250" y="165" width="60" height="25" rx="6"/></g>'''
    if "ssd" in name or "hdd" in name or "drive" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="235" y="170" width="130" height="80" rx="8"/>  <rect x="250" y="200" width="100" height="60" rx="6"/>  <circle cx="350" cy="210" r="6" fill="{color}" stroke="none"/></g>'''
    if "mouse" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="260" y="170" width="80" height="110" rx="40"/>  <line x1="300" y1="170" x2="300" y2="210"/></g>'''
    if "keyboard" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="215" y="190" width="170" height="80" rx="10"/>  <rect x="230" y="205" width="30" height="20" rx="4"/>  <rect x="270" y="205" width="30" height="20" rx="4"/>  <rect x="310" y="205" width="30" height="20" rx="4"/>  <rect x="350" y="205" width="30" height="20" rx="4"/>  <rect x="230" y="235" width="70" height="20" rx="4"/>  <rect x="310" y="235" width="70" height="20" rx="4"/></g>'''
    if "speaker" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="250" y="165" width="100" height="110" rx="12"/>  <circle cx="300" cy="205" r="14"/>  <circle cx="300" cy="245" r="26"/></g>'''
    if "pen drive" in name or "pendrive" in name or "usb" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="255" y="185" width="90" height="70" rx="10"/>  <rect x="280" y="155" width="40" height="30" rx="6"/>  <line x1="292" y1="170" x2="292" y2="185"/>  <line x1="308" y1="170" x2="308" y2="185"/></g>'''
    if "ipad" in name or "tablet" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="235" y="145" width="130" height="160" rx="16"/>  <circle cx="300" cy="290" r="6" fill="{color}" stroke="none"/></g>'''
    if "macbook" in name or "laptop" in name or "pavilion" in name or "inspiron" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="230" y="160" width="140" height="90" rx="8"/>  <line x1="210" y1="260" x2="390" y2="260"/>  <rect x="220" y="260" width="160" height="20" rx="6"/></g>'''
    if "phone" in name or "iphone" in name or "galaxy" in name or "oneplus" in name or "redmi" in name or "nothing" in name:
        return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="250" y="150" width="100" height="140" rx="16"/>  <circle cx="300" cy="280" r="6" fill="{color}" stroke="none"/></g>'''

    return f'''<g stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round">  <rect x="240" y="170" width="120" height="100" rx="16"/>  <line x1="240" y1="200" x2="360" y2="200"/>  <line x1="240" y1="230" x2="360" y2="230"/></g>'''


def generate_svg(image_path: Path, product_name: str, category: str, force: bool = False):
    if image_path.exists() and not force:
        return

    color = CATEGORY_COLORS.get(category, "#333333")
    safe_title = product_name.replace("&", "and")
    icon_svg = ""
    circle_svg = f'<circle cx="300" cy="220" r="82" fill="{color}"/>'
    backdrop_svg = ""

    if category == "Gadgets":
        icon_svg = _gadget_icon_svg(product_name, color)
        icon_svg = f'<g transform="translate(0 -20) scale(1.5)">{icon_svg}</g>'
        circle_svg = ""
        backdrop_svg = f'<rect x="160" y="120" width="280" height="220" rx="32" fill="{color}" opacity="0.12"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">
<rect width="600" height="600" fill="#f7f7f7"/>
<rect x="36" y="36" width="528" height="528" rx="28" fill="{color}" opacity="0.12"/>
{backdrop_svg}
{circle_svg}
{icon_svg}
<text x="300" y="410" text-anchor="middle" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#1d1d1d">{safe_title}</text>
<text x="300" y="456" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="#4d4d4d">PriceLens {category}</text>
</svg>'''
    image_path.write_text(svg, encoding="utf-8")


def seed_products():
    app = create_app()
    image_dir = Path(__file__).parent / "static" / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    with app.app_context():
        for name, brand, category, slug, initial_prices in PRODUCTS:
            image_file = f"{slug}.svg"
            image_path = image_dir / image_file
            generate_svg(image_path, name, category)

            model = {
                'Grocery': GroceryProduct,
                'Clothing': ClothingProduct,
                'Gadgets': GadgetsProduct,
            }[category]
            product = model.query.filter_by(name=name).first()
            if not product:
                product = model(
                    name=name,
                    category=category,
                    brand=brand,
                    image_url=f"images/{image_file}",
                )
                db.session.add(product)
                db.session.flush()
            else:
                product.category = category
                product.brand = brand
                product.image_url = f"images/{image_file}"

            platforms = PLATFORMS[category]
            now = datetime.utcnow()

            for platform, raw_price in zip(platforms, initial_prices):
                price_value = Decimal(str(raw_price)).quantize(Decimal("0.01"))
                price_row = Price.query.filter_by(category=category, product_id=product.id, platform=platform).first()

                if not price_row:
                    price_row = Price(
                        category=category,
                        product_id=product.id,
                        platform=platform,
                        price=price_value,
                        last_updated=now,
                    )
                    db.session.add(price_row)
                else:
                    price_row.price = price_value
                    price_row.last_updated = now

        db.session.commit()
        print("Seed complete: 45 products with platform prices and local images.")

if __name__ == "__main__":
    seed_products()
