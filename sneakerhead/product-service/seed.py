# sneakerhead/product-service/seed.py
"""
Seed script: inserts 30 sneaker products into the database.
Run: python -m app.seed  (from inside the container or locally)
Skips if products already exist.
"""
import asyncio
import random
import uuid

from app.db.session import async_session_factory
from app.crud.product import get_product_count, create_product
from app.schemas.product import ProductCreate


PRODUCTS = [
    # ── Nike (8) ─────────────────────────────────────
    {
        "name": "Air Max 90",
        "brand": "Nike",
        "sku": "NIKE-AM90-001",
        "colorway": "White/Black/Team Red",
        "category": "Lifestyle",
        "description": "The Nike Air Max 90 stays true to its OG running roots with the iconic Waffle outsole, stitched overlays, and classic TPU details. Fresh colorways and new materials give the iconic silhouette a modern look while Max Air cushioning adds comfort to your journey.",
        "price": 130.00,
        "compare_at_price": 160.00,
        "is_featured": True,
    },
    {
        "name": "Air Force 1 '07",
        "brand": "Nike",
        "sku": "NIKE-AF1-002",
        "colorway": "Triple White",
        "category": "Lifestyle",
        "description": "The radiance lives on in the Nike Air Force 1 '07, the basketball original that puts a fresh spin on what you know best: durably stitched overlays, clean finishes and the perfect amount of flash to make you shine.",
        "price": 110.00,
        "compare_at_price": None,
        "is_featured": True,
    },
    {
        "name": "Dunk Low Retro",
        "brand": "Nike",
        "sku": "NIKE-DNKL-003",
        "colorway": "Black/White Panda",
        "category": "Lifestyle",
        "description": "Created for the hardwood but taken to the streets, the Nike Dunk Low Retro returns with crisp overlays and original team colors. This basketball icon channels '80s vibes with premium leather in the upper that looks good and breaks in even better.",
        "price": 115.00,
        "compare_at_price": 130.00,
        "is_featured": False,
    },
    {
        "name": "ZoomX Vaporfly NEXT% 3",
        "brand": "Nike",
        "sku": "NIKE-VF3-004",
        "colorway": "Volt/Black",
        "category": "Running",
        "description": "The Nike ZoomX Vaporfly NEXT% 3 helps you chase new goals and push your pace. It's made for the moments when you put it all on the line — whether you're chasing a personal record or a podium finish.",
        "price": 260.00,
        "compare_at_price": None,
        "is_featured": True,
    },
    {
        "name": "Kobe 6 Protro",
        "brand": "Nike",
        "sku": "NIKE-KB6-005",
        "colorway": "Grinch Green",
        "category": "Basketball",
        "description": "The Kobe 6 Protro 'Grinch' returns with updated technology while maintaining the beloved aesthetic. Featuring Zoom Air units and lightweight construction that made Kobe's signature line legendary on the court.",
        "price": 190.00,
        "compare_at_price": 220.00,
        "is_featured": False,
    },
    {
        "name": "SB Dunk Low Pro",
        "brand": "Nike",
        "sku": "NIKE-SBD-006",
        "colorway": "Fog Grey/White",
        "category": "Skate",
        "description": "The Nike SB Dunk Low Pro features a padded, low-cut collar and cushioned Zoom Air insole that lets you skate with comfort. Premium suede and leather give lasting durability whether you're skating or styling.",
        "price": 115.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    {
        "name": "Free Metcon 5",
        "brand": "Nike",
        "sku": "NIKE-FM5-007",
        "colorway": "Black/Anthracite",
        "category": "Training",
        "description": "The Nike Free Metcon 5 combines flexibility for sprint drills with stability for weightlifting. A chain-link mesh upper provides breathability and structure, while the wide heel provides a stable base for pushing heavy weight.",
        "price": 120.00,
        "compare_at_price": 140.00,
        "is_featured": False,
    },
    {
        "name": "Pegasus 41",
        "brand": "Nike",
        "sku": "NIKE-PG41-008",
        "colorway": "Summit White/Pure Platinum",
        "category": "Running",
        "description": "The Nike Pegasus 41 continues the legacy as the go-to daily trainer. ReactX foam delivers a smooth, responsive ride while the breathable mesh upper keeps your feet fresh mile after mile.",
        "price": 140.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    # ── Adidas (6) ───────────────────────────────────
    {
        "name": "Ultraboost Light",
        "brand": "Adidas",
        "sku": "ADI-UBL-001",
        "colorway": "Core Black/Core Black",
        "category": "Running",
        "description": "Experience epic energy with the adidas Ultraboost Light. Light BOOST cushioning provides incredible energy return and comfort. The Primeknit+ upper wraps the foot in adaptive support and breathability.",
        "price": 190.00,
        "compare_at_price": 210.00,
        "is_featured": True,
    },
    {
        "name": "Forum Low",
        "brand": "Adidas",
        "sku": "ADI-FL-002",
        "colorway": "Cloud White/Royal Blue",
        "category": "Lifestyle",
        "description": "First introduced in 1984, the adidas Forum Low was made for the basketball court but quickly became a street style icon. The ankle strap and premium leather upper carry heritage style forward into modern culture.",
        "price": 100.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    {
        "name": "Samba OG",
        "brand": "Adidas",
        "sku": "ADI-SMB-003",
        "colorway": "White/Black/Gum",
        "category": "Lifestyle",
        "description": "Born on the football pitch, the adidas Samba OG has become one of the most iconic sneakers ever. The soft leather upper, suede T-toe overlay, and gum rubber outsole make it unmistakably Samba.",
        "price": 100.00,
        "compare_at_price": 120.00,
        "is_featured": True,
    },
    {
        "name": "NMD_R1",
        "brand": "Adidas",
        "sku": "ADI-NMD-004",
        "colorway": "Grey Five/Lush Red",
        "category": "Lifestyle",
        "description": "The adidas NMD_R1 fuses key heritage running elements with a modern construction. BOOST cushioning and a stretchy knit upper deliver all-day comfort and style that transitions from city streets to casual hangouts.",
        "price": 150.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    {
        "name": "Adizero Adios Pro 3",
        "brand": "Adidas",
        "sku": "ADI-AAP3-005",
        "colorway": "Pulse Lime/Core Black",
        "category": "Running",
        "description": "The adidas Adizero Adios Pro 3 is built for speed with LIGHTSTRIKE PRO cushioning and ENERGYRODS 2.0 for explosive propulsion. Designed for elite runners chasing records on race day.",
        "price": 250.00,
        "compare_at_price": 280.00,
        "is_featured": False,
    },
    {
        "name": "Dropset 2 Trainer",
        "brand": "Adidas",
        "sku": "ADI-DS2-006",
        "colorway": "Aurora Black/Silver",
        "category": "Training",
        "description": "Engineered for versatile workouts, the adidas Dropset 2 features a wide, flat outsole for stability during lifts and a Bounce midsole for comfort during cardio sessions. The durable ripstop upper supports every movement.",
        "price": 120.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    # ── Jordan (5) ───────────────────────────────────
    {
        "name": "Air Jordan 1 Retro High OG",
        "brand": "Jordan",
        "sku": "JDN-AJ1H-001",
        "colorway": "Chicago/Lost and Found",
        "category": "Lifestyle",
        "description": "The Air Jordan 1 Retro High OG 'Lost and Found' captures the thrill of a vintage find. Premium leather, vintage details, and the iconic Wings logo bring the original 1985 energy to life with cracked overlays and pre-yellowed midsoles.",
        "price": 180.00,
        "compare_at_price": None,
        "is_featured": True,
    },
    {
        "name": "Air Jordan 4 Retro",
        "brand": "Jordan",
        "sku": "JDN-AJ4-002",
        "colorway": "Military Black",
        "category": "Lifestyle",
        "description": "The Air Jordan 4 Retro 'Military Black' delivers clean style with a white leather upper, grey accents, and black detailing. The mesh inserts and visible Air-Sole unit keep the heritage design fresh and breathable.",
        "price": 210.00,
        "compare_at_price": 250.00,
        "is_featured": True,
    },
    {
        "name": "Air Jordan 11 Retro",
        "brand": "Jordan",
        "sku": "JDN-AJ11-003",
        "colorway": "Cool Grey",
        "category": "Basketball",
        "description": "The Air Jordan 11 Retro 'Cool Grey' returns with patent leather mudguard, Ballistic mesh upper, and full-length Air cushioning. One of the most celebrated silhouettes in the Jordan lineup.",
        "price": 225.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    {
        "name": "Air Jordan 3 Retro",
        "brand": "Jordan",
        "sku": "JDN-AJ3-004",
        "colorway": "White Cement Reimagined",
        "category": "Lifestyle",
        "description": "The Air Jordan 3 'White Cement Reimagined' features the original cement print, elephant skin overlays, and a visible Air-Sole unit designed by Tinker Hatfield. A timeless icon in premium Nike Air branding.",
        "price": 200.00,
        "compare_at_price": 230.00,
        "is_featured": False,
    },
    {
        "name": "Luka 2",
        "brand": "Jordan",
        "sku": "JDN-LK2-005",
        "colorway": "Lake Bled",
        "category": "Basketball",
        "description": "Designed for Luka Dončić's dynamic playstyle, the Jordan Luka 2 delivers responsive IsoPlate technology, lightweight cushioning, and multidirectional traction for explosive court movements.",
        "price": 130.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    # ── New Balance (5) ──────────────────────────────
    {
        "name": "990v6",
        "brand": "New Balance",
        "sku": "NB-990V6-001",
        "colorway": "Grey/Silver",
        "category": "Lifestyle",
        "description": "The New Balance 990v6 continues the iconic lineage with FuelCell midsole cushioning, premium pigskin suede and mesh upper, and ENCAP technology. Proudly made in the USA, this shoe stands for quality and performance.",
        "price": 200.00,
        "compare_at_price": None,
        "is_featured": True,
    },
    {
        "name": "550",
        "brand": "New Balance",
        "sku": "NB-550-002",
        "colorway": "White/Green",
        "category": "Lifestyle",
        "description": "Originally released in 1989, the New Balance 550 is a heritage basketball shoe brought back for today's culture. Clean leather upper, perforated toe box, and retro 'N' branding deliver classic appeal.",
        "price": 110.00,
        "compare_at_price": 130.00,
        "is_featured": False,
    },
    {
        "name": "FuelCell SuperComp Elite v4",
        "brand": "New Balance",
        "sku": "NB-FSCE4-003",
        "colorway": "Neon Dragonfly",
        "category": "Running",
        "description": "The New Balance FuelCell SuperComp Elite v4 is an elite racing shoe featuring an Energy Arc carbon plate, FuelCell foam, and a streamlined upper designed for maximum speed on race day.",
        "price": 275.00,
        "compare_at_price": 300.00,
        "is_featured": False,
    },
    {
        "name": "TWO WXY v4",
        "brand": "New Balance",
        "sku": "NB-WXY4-004",
        "colorway": "Electric Teal/Black",
        "category": "Basketball",
        "description": "The New Balance TWO WXY v4 brings responsive FuelCell cushioning and a dynamic woven upper to the basketball court. Engineered for quick guards who need speed and support in equal measure.",
        "price": 140.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    {
        "name": "Fresh Foam X 1080v13",
        "brand": "New Balance",
        "sku": "NB-1080V13-005",
        "colorway": "Arctic Grey/Limelight",
        "category": "Running",
        "description": "The New Balance Fresh Foam X 1080v13 delivers a plush ride with Fresh Foam X midsole cushioning and a Hypoknit upper that adapts to the shape of your foot for unparalleled comfort on long runs.",
        "price": 165.00,
        "compare_at_price": 185.00,
        "is_featured": False,
    },
    # ── Puma (3) ─────────────────────────────────────
    {
        "name": "Suede Classic XXI",
        "brand": "Puma",
        "sku": "PUMA-SC21-001",
        "colorway": "Peacoat/White",
        "category": "Lifestyle",
        "description": "The Puma Suede Classic XXI reimagines the iconic silhouette with a premium suede upper and a sleek rubber outsole. From the streets to the stage, the Suede has been a cultural staple since 1968.",
        "price": 80.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    {
        "name": "MB.03",
        "brand": "Puma",
        "sku": "PUMA-MB03-002",
        "colorway": "LaMelo Blue/Red Blast",
        "category": "Basketball",
        "description": "The Puma MB.03 is LaMelo Ball's latest signature shoe featuring NITRO foam cushioning, a bold TPU wing, and a lightweight, breathable mesh upper designed for explosive plays and flashy style.",
        "price": 145.00,
        "compare_at_price": 165.00,
        "is_featured": False,
    },
    {
        "name": "Deviate NITRO Elite 2",
        "brand": "Puma",
        "sku": "PUMA-DNE2-003",
        "colorway": "Lime Pow/Black",
        "category": "Running",
        "description": "The Puma Deviate NITRO Elite 2 is a race-day weapon with a NITRO-infused midsole, an internal PWRPLATE carbon fiber plate, and an ultra-lightweight PWRTAPE upper for blistering speed.",
        "price": 230.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    # ── Asics (3) ────────────────────────────────────
    {
        "name": "GEL-Kayano 30",
        "brand": "Asics",
        "sku": "ASICS-GK30-001",
        "colorway": "Black/Carrier Grey",
        "category": "Running",
        "description": "Celebrating 30 years of stability, the ASICS GEL-KAYANO 30 features FF BLAST PLUS ECO cushioning, a 4D GUIDANCE SYSTEM for smooth transitions, and a recycled engineered mesh upper for sustainable performance.",
        "price": 160.00,
        "compare_at_price": 185.00,
        "is_featured": False,
    },
    {
        "name": "GEL-1130",
        "brand": "Asics",
        "sku": "ASICS-G1130-002",
        "colorway": "White/Clay Canyon",
        "category": "Lifestyle",
        "description": "The ASICS GEL-1130 draws from the original 2008 running shoe with its layered mesh and synthetic upper. Rearfoot GEL technology provides shock absorption, while the retro styling makes it a streetwear essential.",
        "price": 100.00,
        "compare_at_price": None,
        "is_featured": False,
    },
    {
        "name": "Unpre Ars 2",
        "brand": "Asics",
        "sku": "ASICS-UA2-003",
        "colorway": "Shocking Orange/Black",
        "category": "Basketball",
        "description": "The ASICS Unpre Ars 2 brings Japanese engineering to the hardwood with FF BLAST cushioning, a wraparound outsole design for multidirectional grip, and a supportive midfoot cage for lockdown performance.",
        "price": 140.00,
        "compare_at_price": 160.00,
        "is_featured": False,
    },
]


def _generate_sizes_inventory() -> dict:
    """Generate random stock for US sizes 7-13."""
    sizes = {}
    for s in range(7, 14):
        sizes[str(s)] = random.randint(0, 10)
    return sizes


def _generate_images(sku: str) -> list:
    """Generate 3 placeholder image URLs per product."""
    colors = ["e8ff00", "1a1a1a", "333333"]
    return [
        f"https://placehold.co/600x600/{colors[i]}/ffffff?text={sku.replace('-', '+')}"
        for i in range(3)
    ]


async def seed():
    async with async_session_factory() as db:
        count = await get_product_count(db)
        if count > 0:
            print(f"Database already has {count} products. Skipping seed.")
            return

        for p_data in PRODUCTS:
            data = ProductCreate(
                name=p_data["name"],
                brand=p_data["brand"],
                sku=p_data["sku"],
                colorway=p_data.get("colorway"),
                category=p_data["category"],
                description=p_data.get("description", ""),
                price=p_data["price"],
                compare_at_price=p_data.get("compare_at_price"),
                images=_generate_images(p_data["sku"]),
                sizes_inventory=_generate_sizes_inventory(),
                is_featured=p_data.get("is_featured", False),
                is_active=True,
                rating=round(random.uniform(3.5, 5.0), 2),
                review_count=random.randint(10, 500),
            )
            product = await create_product(db, data)
            print(f"  ✓ Seeded: {product.brand} {product.name} ({product.sku})")

        print(f"\n✅ Seeded {len(PRODUCTS)} products successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
