"""Client-approved company facts and page metadata. No invented certifications or product sizes."""
COMPANY = "GangaShree Roots Private Limited"
PHONE = "+91 81694 56633"
EMAIL = "GangaShreeroots@gmail.com"
REGIONS = {
    "Maharashtra": ["Mumbai", "Thane", "Palghar"],
    "Uttar Pradesh": ["Prayagraj", "Jaunpur", "Varanasi", "Pratapgarh", "Sultanpur", "Ayodhya", "Chitrakoot"],
}
# Approximate city centres, not office/factory coordinates. GeoNames CC BY.
CITY_CENTRES = {
    "Mumbai": (19.07283, 72.88261, 1275339),
    "Thane": (19.19704, 72.96355, 1254661),
    "Palghar": (19.69693, 72.76543, 1260730),
    "Prayagraj": (25.44478, 81.84322, 1278994),
    "Jaunpur": (25.75356, 82.68689, 1269135),
    "Varanasi": (25.31668, 83.01041, 1253405),
    "Pratapgarh": (25.89509, 81.9424, 1259337),
    "Sultanpur": (26.25788, 82.07269, 1255491),
    "Ayodhya": (26.79909, 82.2047, 1278094),
    "Chitrakoot": (25.21473, 80.91645, 1267629),
}
OFFICES = [
    {"name": "Head office", "street": "505, Dattani Prism 1, Husaini Colony, Behind Dattani Mall", "city": "Vasai West, Mumbai Region", "state": "Maharashtra", "pin": "401202"},
    {"name": "Registered office", "street": "Pachkhara, Jasra", "city": "Prayagraj", "state": "Uttar Pradesh", "pin": "212107"},
]
VALUES = [
    ("Quality & safety", "We are committed to high standards of product quality, hygiene and safety across manufacturing and packaging."),
    ("Trust & transparency", "Honest business practices, open communication and lasting relationships with customers, distributors, suppliers and partners."),
    ("Purity & responsibility", "We prioritize product integrity and responsible manufacturing, recognizing the everyday importance of drinking water and beverages."),
    ("Innovation & excellence", "We seek better technologies, efficient production methods and innovative beverage solutions for evolving consumer needs."),
    ("Sustainability & environmental care", "We aim to improve resource efficiency, reduce unnecessary waste and encourage responsible packaging and environmental practices."),
    ("Customer commitment", "We strive to deliver dependable products, consistent service and value that earns customer confidence every day."),
    ("Integrity & sustainable growth", "Ethical business, teamwork and responsible expansion that benefits employees, stakeholders, partners and communities."),
]
PORTFOLIO = [
    {"id": "water", "name": "Packaged drinking water", "tag": "Everyday refreshment", "description": "Revenger packaged drinking water brings everyday hydration to the table, the workplace and the moments in between. Contact our team for 500 ml and 1 litre retail supply enquiries.", "accent": "water", "image": "images/revenger-water-1l.png", "image_width": 1108, "image_height": 1420},
    {"id": "soda", "name": "Soda", "tag": "A sparkling pause", "size": "500 ml", "description": "A carbonated refreshment for a variety of occasions. Explore Revenger soda for your retail or beverage business; ask our team about current availability.", "accent": "soda", "image": "images/revenger-soda-500ml.png", "image_width": 1024, "image_height": 1536},
    {"id": "jeera-soda", "name": "Jeera soda", "tag": "Familiar flavour. Fresh fizz.", "size": "500 ml", "description": "A distinctive cumin-flavoured carbonated beverage from the Revenger portfolio. A flavourful choice for consumers who enjoy a traditional jeera taste with fizz.", "accent": "jeera", "image": "images/revenger-jeera-soda-500ml.png", "image_width": 1024, "image_height": 1536},
    {"id": "lemon-soda", "name": "Nimbu soda", "tag": "A little citrus lift", "size": "500 ml", "description": "A zesty, citrus-flavoured carbonated beverage for a refreshing change of pace. Speak with us about Revenger nimbu soda availability in your area.", "accent": "lemon", "image": "images/revenger-nimbu-soda-500ml.png", "image_width": 1024, "image_height": 1536},
]
LEADERS = [
    {"initials": "SB", "portrait": "images/subir-banerjee.jpeg", "portrait_width": 1067, "portrait_height": 1474, "name": "Subir Banerjee", "role": "Managing Director", "headline": "Engineering excellence. Strategic leadership.", "bio": "Subir Banerjee holds a Bachelor of Engineering degree from Mumbai and retired from Tata Communications, where he served as an Engineer. His technical background brings analytical thinking, systematic operations and disciplined problem-solving to his leadership.", "focus": "At GangaShree Roots, he focuses on strategic planning, business development, operational efficiency and long-term growth. He supports the Revenger brand through quality-focused practices and lasting business partnerships.", "quote": "Strong organizations are built on technical knowledge, disciplined execution, trusted partnerships, and a clear vision for the future."},
    {"initials": "RS", "portrait": "images/rakesh-salve.jpeg", "portrait_width": 1219, "portrait_height": 1290, "name": "Rakesh Salve", "role": "Chief Executive Officer", "headline": "Engineering expertise. Beverage innovation.", "bio": "Rakesh Salve is an engineering professional who worked as an ERS Engineer with Tata Communications. His technical experience and solution-oriented thinking support his approach to operational management and business leadership.", "focus": "As CEO, he focuses on bottling and packaging practices, product quality, supply-chain efficiency and distribution development. He aims to grow Revenger through continuous improvement and relationships with retailers, distributors and institutional customers.", "quote": "Great brands are built on quality, consistent execution, customer trust, and a vision that turns opportunities into sustainable growth."},
]
PAGES = {
    "home": {"path": "/", "label": "Home", "title": "Revenger | Drinking Water & Beverages in Maharashtra & UP", "description": "Discover Revenger packaged drinking water, soda, jeera soda and nimbu soda. Serving Mumbai, Thane, Palghar, Prayagraj and selected Uttar Pradesh cities."},
    "company": {"path": "/company", "label": "Our company", "title": "Our Company & Leadership | GangaShree Roots | Revenger", "description": "Meet GangaShree Roots Private Limited, the company behind Revenger, and its leaders: Managing Director Subir Banerjee and CEO Rakesh Salve."},
    "products": {"path": "/products", "label": "Our drinks", "title": "Packaged Drinking Water, Soda, Jeera & Nimbu Soda | Revenger", "description": "Explore Revenger packaged drinking water, soda, jeera soda and nimbu soda. Contact GangaShree Roots for product availability and retail enquiries."},
    "values": {"path": "/values", "label": "Our values", "title": "Quality, Trust & Responsible Growth | Revenger Values", "description": "Discover the values guiding GangaShree Roots: quality, transparency, customer commitment, innovation and responsible growth for the Revenger brand."},
    "areas": {"path": "/service-areas", "label": "Where we serve", "title": "Water & Beverage Retail Enquiries in Prayagraj & Mumbai | Revenger", "description": "Revenger serves Mumbai, Thane, Palghar, Prayagraj, Jaunpur, Varanasi, Pratapgarh, Sultanpur, Ayodhya and Chitrakoot. Enquire about water and beverages."},
    "contact": {"path": "/contact", "label": "Contact", "title": "Contact Revenger | Vasai West & Prayagraj Offices", "description": "Contact GangaShree Roots for Revenger water and beverage enquiries. Call +91 8169456633. Head office in Vasai West; registered office in Prayagraj."},
}
