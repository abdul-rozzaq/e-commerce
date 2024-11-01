# import os
# import sys

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# import django

# django.setup()


import random
from django.utils.text import slugify
from project.models import Product, Category, ProductSize, ProductColor, ProductImage, AdditionalInfo

# Barcha kerakli modellar uchun ma'lumotlarni olib kelamiz
categories = list(Category.objects.all())
sizes = list(ProductSize.objects.all())
colors = list(ProductColor.objects.all())

# Mahsulot nomlari uchun namunalar
product_names = [
    "Telefon",
    "Noutbuk",
    "Kitob",
    "Sumka",
    "Ko'ylak",
    "Shim",
    "Poyabzal",
    "O'yinchoq",
    "Soat",
    "Uy jihozi",
    "Go'zallik mahsuloti",
    "Uy anjomi",
    "Kiyim-kechak",
    "Kompyuter",
    "Ofis stoli",
    "Yozuv daftari",
    "Uy o'yinlari",
    "Avtomobil aksessuari",
    "Karnay",
    "Smartfon",
]

# Rasmlar ro'yxati
image_paths = [
    "product-images/cat-1.jpg",
    "product-images/cat-2.jpg",
    "product-images/cat-3.jpg",
    "product-images/cat-4.jpg",
    "product-images/product-1.jpg",
    "product-images/product-2.jpg",
    "product-images/product-3.jpg",
    "product-images/product-4.jpg",
    "product-images/product-5.jpg",
    "product-images/product-6.jpg",
    "product-images/product-9.jpg",
]

# Qo'shimcha ma'lumotlar kalitlari uchun namunalar
additional_info_keys = ["Material", "Og'irlik", "Kafolat", "Rangi", "O'lchami"]

# 100 ta mahsulot yaratamiz
for i in range(100):
    # Tasodifiy nom va tavsif tanlash
    name = random.choice(product_names) + f" {i + 1}"
    description = f"{name} - Bu mahsulot {name.lower()} haqida batafsil tavsif."

    # Tasodifiy kategoriya, narx, va mavjudlik miqdorini aniqlash
    category = random.choice(categories)
    price = round(random.uniform(5.00, 500.00), 2)
    count = random.randint(1, 100)

    # Mahsulotni yaratamiz
    product = Product.objects.create(category=category, name=name, slug=slugify(name), description=description, price=price, count=count)

    # Tasodifiy o'lchamlar va ranglarni qo'shamiz
    selected_sizes = random.sample(sizes, k=random.randint(1, min(3, len(sizes))))
    selected_colors = random.sample(colors, k=random.randint(1, min(3, len(colors))))
    product.sizes.set(selected_sizes)
    product.colors.set(selected_colors)

    # Har bir mahsulotga kamida 3 ta rasm qo'shamiz
    num_images = random.randint(3, 5)  # 3 dan 5 gacha rasm
    for _ in range(num_images):
        image_path = random.choice(image_paths)
        ProductImage.objects.create(product=product, image=image_path)

    # Qo'shimcha ma'lumotlar qo'shamiz
    num_additional_info = random.randint(2, 5)  # 2 dan 5 gacha qo'shimcha ma'lumot
    for _ in range(num_additional_info):
        key = random.choice(additional_info_keys)
        value = f"{key} haqida ma'lumot"
        AdditionalInfo.objects.create(product=product, key=key, value=value)

print("100 ta mahsulot muvaffaqiyatli yaratildi!")
