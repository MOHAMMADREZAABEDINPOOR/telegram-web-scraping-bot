#agno
"""
PIMX Interactive House Search Telegram Bot
Developed by Mohammadreza Abedinpour for PIMX

This bot listens for Telegram messages from users and provides house listings from Divar.
Uses telebot library for proper Telegram integration.
"""

import telebot
from telebot import types
from agno.agent import Agent
from agno.tools import tool
from scrapling import Fetcher
from agno.models.google import Gemini
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = "8273383219:AAEUQshygEWA25SuAa5nhkfP1SqgSKBnLV4"
CHAT_ID = "5675632554"

# Initialize Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Configure Gemini 1.5 Flash model using Agno framework
model = Gemini(
    id="gemini-1.5-flash",
    api_key="AIzaSyCsCWpBFhFdQdf-Fjv5tt618A3WydCZ7hw"
)

# City translation dictionary (Persian to English)
# Developed by Mohammadreza Abedinpour for PIMX
city_translations = {
    'تهران': 'tehran',
    'اصفهان': 'isfahan', 
    'مشهد': 'mashhad',
    'شیراز': 'shiraz',
    'تبریز': 'tabriz',
    'کرج': 'karaj',
    'اهواز': 'ahvaz',
    'قم': 'qom',
    'رشت': 'rasht',
    'کرمان': 'kerman',
    'همدان': 'hamedan',
    'یزد': 'yazd',
    'اردبیل': 'ardabil',
    'بندرعباس': 'bandar-abbas',
    'کرمانشاه': 'kermanshah',
    'زاهدان': 'zahedan',
    'ساری': 'sari',
    'قزوین': 'qazvin',
    'خرم آباد': 'khorramabad',
    'گرگان': 'gorgan'
}

# Property type URLs - Dynamic with city placeholder
# Developed by Mohammadreza Abedinpour for PIMX
property_urls = {
    # Residential Sale
    'apartment_buy': 'https://divar.ir/s/{city}/buy-apartment?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Capartment-sell',
    'villa_buy': 'https://divar.ir/s/{city}/buy-villa?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Chouse-villa-sell',
    'land_buy': 'https://divar.ir/s/{city}/buy-old-house?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Cplot-old',
    'residential_buy_all': 'https://divar.ir/s/{city}/buy-residential?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Cresidential-sell',
    
    # Residential Rent
    'apartment_rent': 'https://divar.ir/s/{city}/rent-apartment?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Capartment-rent',
    'villa_rent': 'https://divar.ir/s/{city}/rent-villa?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Chouse-villa-rent',
    'residential_rent_all': 'https://divar.ir/s/{city}/rent-residential?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Cresidential-rent',
    
    # Commercial Sale
    'office_buy': 'https://divar.ir/s/{city}/buy-office?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Coffice-sell',
    'store_buy': 'https://divar.ir/s/{city}/buy-store?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Cshop-sell',
    'industrial_buy': 'https://divar.ir/s/{city}/buy-industrial-agricultural-property?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Cindustry-agriculture-business-sell',
    'commercial_buy_all': 'https://divar.ir/s/{city}/buy-commercial-property?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Ccommercial-sell',
    
    # Commercial Rent
    'office_rent': 'https://divar.ir/s/{city}/rent-office?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Coffice-rent',
    'store_rent': 'https://divar.ir/s/{city}/rent-store?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Cshop-rent',
    'industrial_rent': 'https://divar.ir/s/{city}/rent-industrial-agricultural-property?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Cindustry-agriculture-business-rent',
    'commercial_rent_all': 'https://divar.ir/s/{city}/rent-commercial-property?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Ccommercial-rent',
    
    # All Properties
    'all_properties': 'https://divar.ir/s/{city}/real-estate?business-type=personal&map_bbox=51.107464%2C35.399564%2C51.636307%2C36.032207&map_interaction=list_only_used&map_place_hash=1%7C%7Creal-estate'
}

# User state management
user_states = {}

# Pagination settings
PROPERTIES_PER_PAGE = 1  # Show one property at a time

def translate_city_name(persian_city: str) -> str:
    """Convert Persian city name to English for Divar URL
    Developed by Mohammadreza Abedinpour for PIMX
    """
    persian_city = persian_city.strip()
    english_city = city_translations.get(persian_city)
    
    if english_city:
        return english_city
    else:
        logger.info(f"City '{persian_city}' not found in translations. Using Tehran as default.")
        return 'tehran'

def create_main_menu():
    """Create main menu with 5 property type options
    Developed by Mohammadreza Abedinpour for PIMX
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("🏠 فروش مسکونی", callback_data="residential_sale")
    btn2 = types.InlineKeyboardButton("🏡 اجاره مسکونی", callback_data="residential_rent")
    btn3 = types.InlineKeyboardButton("🏢 فروش اداری و تجاری", callback_data="commercial_sale")
    btn4 = types.InlineKeyboardButton("🏬 اجاره اداری و تجاری", callback_data="commercial_rent")
    btn5 = types.InlineKeyboardButton("🏘️ همه آگهی ها", callback_data="property_all_properties")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    return markup

def create_residential_sale_menu():
    """Create residential sale submenu
    Developed by Mohammadreza Abedinpour for PIMX
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("🏠 آپارتمان", callback_data="property_apartment_buy")
    btn2 = types.InlineKeyboardButton("🏡 خانه و ویلا", callback_data="property_villa_buy")
    btn3 = types.InlineKeyboardButton("🗻 زمین و ملک کلنگی", callback_data="property_land_buy")
    btn4 = types.InlineKeyboardButton("📋 همه آگهی های فروش", callback_data="property_residential_buy_all")
    btn5 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    return markup

def create_residential_rent_menu():
    """Create residential rent submenu
    Developed by Mohammadreza Abedinpour for PIMX
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("🏠 آپارتمان", callback_data="property_apartment_rent")
    btn2 = types.InlineKeyboardButton("🏡 خانه و ویلا", callback_data="property_villa_rent")
    btn3 = types.InlineKeyboardButton("📋 همه آگهی ها", callback_data="property_residential_rent_all")
    btn4 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    
    return markup

def create_commercial_sale_menu():
    """Create commercial sale submenu
    Developed by Mohammadreza Abedinpour for PIMX
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("🏢 دفتر کار، اتاق اداری، مطب", callback_data="property_office_buy")
    btn2 = types.InlineKeyboardButton("🏪 مغازه و غرفه", callback_data="property_store_buy")
    btn3 = types.InlineKeyboardButton("🏭 صنعتی، کشاورزی، تجاری", callback_data="property_industrial_buy")
    btn4 = types.InlineKeyboardButton("📋 همه آگهی های فروش", callback_data="property_commercial_buy_all")
    btn5 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    return markup

def create_commercial_rent_menu():
    """Create commercial rent submenu
    Developed by Mohammadreza Abedinpour for PIMX
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("🏢 دفتر کار، اتاق اداری، مطب", callback_data="property_office_rent")
    btn2 = types.InlineKeyboardButton("🏪 مغازه و غرفه", callback_data="property_store_rent")
    btn3 = types.InlineKeyboardButton("🏭 صنعتی، کشاورزی، تجاری", callback_data="property_industrial_rent")
    btn4 = types.InlineKeyboardButton("📋 همه آگهی های اجاره", callback_data="property_commercial_rent_all")
    btn5 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    
    return markup

def create_pagination_menu(user_id: int, has_more: bool = True):
    """Create pagination menu for real-time single property fetching
    Each 'next' click fetches fresh data from Divar website
    Developed by Mohammadreza Abedinpour for PIMX
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if has_more:
        btn_continue = types.InlineKeyboardButton("➡️ آگهی بعدی", callback_data=f"continue_{user_id}")
        btn_menu = types.InlineKeyboardButton("🏠 منو", callback_data="back_to_main")
        markup.add(btn_continue, btn_menu)
    else:
        btn_menu = types.InlineKeyboardButton("🏠 بازگشت به منو", callback_data="back_to_main")
        markup.add(btn_menu)
    
    return markup

def get_property_details(property_url: str) -> dict:
    """Extract detailed property information from individual property page
    Enhanced with better selectors for accurate property descriptions and multiple images
    Developed by Mohammadreza Abedinpour for PIMX
    """
    try:
        fetcher = Fetcher(auto_match=False)
        logger.info(f"Fetching detailed property data from: {property_url}")
        x = fetcher.get(property_url)
        
        # Extract multiple property images (up to 3) with enhanced selectors
        images = []
        
        # Try comprehensive image selectors and collect up to 3 images
        image_selectors = [
            # Primary carousel images
            'div.kt-col-6.kt-offset-1 > section:nth-child(1) > div > div > div.keen-slider.kt-base-carousel__slides.slides-f386a > div > figure > div > picture > img::attr(src)',
            # Alternative carousel structure
            '.kt-base-carousel__slides img::attr(src)',
            # Gallery images
            'img.kt-image-block__image::attr(src)',
            '.post-page__gallery img::attr(src)',
            '.kt-image-gallery img::attr(src)',
            # Property specific images
            '.property-images img::attr(src)',
            # General property images
            'img[src*="divar"][src*="image"]::attr(src)',
            # Any image that looks like property photos
            'img[alt*="عکس"]::attr(src)',
            'img[alt*="تصویر"]::attr(src)',
            # Fallback: all images except logos
            'img[src*=".jpg"]::attr(src)',
            'img[src*=".jpeg"]::attr(src)',
            'img[src*=".png"]::attr(src)',
            'img[src*=".webp"]::attr(src)'
        ]
        
        for selector in image_selectors:
            found_images = x.css(selector)
            for img in found_images:
                img_url = str(img).strip()
                # Enhanced validation for image URLs
                if (img_url and 
                    img_url not in images and 
                    len(images) < 3 and
                    ('http' in img_url or img_url.startswith('/')) and
                    # Check for image file extensions or image-related keywords
                    (any(ext in img_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', 'image', 'photo', 'picture']) or 
                     'divar.ir' in img_url) and
                    # Exclude logos, icons, and other non-property images
                    not any(exclude in img_url.lower() for exclude in ['logo', 'icon', 'avatar', 'profile', 'btn', 'button'])):
                    
                    # Make sure URL is absolute
                    if img_url.startswith('/'):
                        img_url = f'https://divar.ir{img_url}'
                    elif not img_url.startswith('http'):
                        img_url = f'https://divar.ir/{img_url}'
                    
                    images.append(img_url)
                    logger.info(f"Added image {len(images)}: {img_url[:100]}...")
            
            # If we have 3 images, we're done
            if len(images) >= 3:
                break
        
        # If we still don't have enough images, try a more general approach
        if len(images) < 3:
            logger.info(f"Only found {len(images)} images, trying general selector...")
            all_images = x.css('img::attr(src)')
            for img in all_images:
                img_url = str(img).strip()
                if (img_url and 
                    img_url not in images and 
                    len(images) < 3 and
                    ('http' in img_url or img_url.startswith('/')) and
                    not any(exclude in img_url.lower() for exclude in ['logo', 'icon', 'avatar', 'profile', 'btn', 'button', 'svg'])):
                    
                    if img_url.startswith('/'):
                        img_url = f'https://divar.ir{img_url}'
                    elif not img_url.startswith('http'):
                        img_url = f'https://divar.ir/{img_url}'
                    
                    images.append(img_url)
                    logger.info(f"Added fallback image {len(images)}: {img_url[:100]}...")
                
                if len(images) >= 3:
                    break
        
        logger.info(f"Final image count: {len(images)}")        
        
        # Extract metrazh (square footage) with multiple selectors
        metrazh_list = x.css('div.kt-col-5 > section:nth-child(1) > div.post-page__section--padded > table:nth-child(1) > tbody > tr > td:nth-child(1)::text')
        if not metrazh_list:
            metrazh_list = x.css('table tbody tr td:contains("متر")::text')
        if not metrazh_list:
            metrazh_list = x.css('[class*="metrazh"]::text')
        metrazh = str(metrazh_list[0]).strip() if metrazh_list else "نامشخص"
        
        # Extract sakht (construction year) with multiple selectors
        sakht_list = x.css('div.kt-col-5 > section:nth-child(1) > div.post-page__section--padded > table:nth-child(1) > tbody > tr > td:nth-child(2)::text')
        if not sakht_list:
            sakht_list = x.css('table tbody tr td:contains("ساخت")::text')
        if not sakht_list:
            sakht_list = x.css('[class*="year"]::text')
        sakht = str(sakht_list[0]).strip() if sakht_list else "نامشخص"
        
        # Extract room count with multiple selectors
        room_list = x.css('div.kt-col-5 > section:nth-child(1) > div.post-page__section--padded > table:nth-child(1) > tbody > tr > td:nth-child(3)::text')
        if not room_list:
            room_list = x.css('table tbody tr td:contains("اتاق")::text')
        if not room_list:
            room_list = x.css('[class*="room"]::text')
        room = str(room_list[0]).strip() if room_list else "نامشخص"
        
        # Extract detailed prices with multiple selectors
        prices3_list = x.css('div.kt-base-row__end.kt-unexpandable-row__value-box > p::text')
        if not prices3_list:
            prices3_list = x.css('.price-section p::text')
        if not prices3_list:
            prices3_list = x.css('[class*="price"] p::text')
        prices3 = str(prices3_list[0]).strip() if prices3_list else "نامشخص"
        
        # Extract ACTUAL property description with improved selectors
        # Focus on property-specific descriptions, not generic Divar PWA text
        description_list = []
        
        # Try specific property description selectors
        desc_selectors = [
            'div.kt-base-row.kt-base-row--large.kt-description-row > div > p::text',
            '.property-description p::text',
            '.post-description p::text',
            '.description-content p::text',
            '[class*="description"] p::text',
            '.kt-description-row p::text'
        ]
        
        for selector in desc_selectors:
            desc_texts = x.css(selector)
            for desc_text in desc_texts:
                text = str(desc_text).strip()
                # Filter out generic Divar PWA descriptions, navigation instructions, and other irrelevant content
                if (text and 
                    len(text) > 10 and
                    'وب‌اپلیکیشن' not in text and
                    'PWA' not in text and
                    'دیوار سرویسی' not in text and
                    'نصب آن' not in text and
                    'دانلود اپلیکیشن' not in text and
                    'به‌روز‌رسانی' not in text and
                    'در نوار پایین' not in text and
                    'روی دکمهٔ' not in text and
                    'در منوی باز شده' not in text and
                    'گزینهٔ را انتخاب کنید' not in text and
                    'را انتخاب کنید' not in text and
                    'در قسمت بالا' not in text and
                    text not in description_list):
                    description_list.append(text)
            if description_list:
                break
        
        description = " ".join(description_list) if description_list else "توضیحات موجود نیست"
        
        # Post-process description to remove any remaining navigation instructions
        if description != "توضیحات موجود نیست":
            # Remove patterns and navigation text
            import re
            # Remove numbered instructions and navigation text
            description = re.sub(r'در نوار پایین.*?دکمهٔ', '', description)
            description = re.sub(r'۲\..*?دکمهٔ', '', description) 
            description = re.sub(r'۳\..*?دکمهٔ', '', description)
            description = re.sub(r'در منوی باز شده.*?انتخاب کنید\.', '', description)
            description = re.sub(r'در قسمت بالا.*?دکمهٔ', '', description)
            # Remove any remaining "را انتخاب کنید. " or "را انتخاب کنید"
            description = re.sub(r'را انتخاب کنید\.?\s*', '', description)
            # Clean up extra spaces, dots and formatting
            description = re.sub(r'\s+', ' ', description).strip()
            description = re.sub(r'^\.+', '', description).strip()
            description = re.sub(r'^[\s\.]+', '', description).strip()
            # Remove trailing dots and spaces
            description = description.rstrip('. ')
        
        # Extract amenities/facilities with multiple selectors
        emkanat_list = x.css('div.kt-col-5 > section:nth-child(1) > div.post-page__section--padded > table:nth-child(10)::text')
        if not emkanat_list:
            emkanat_list = x.css('table:last-child tbody tr td::text')
        if not emkanat_list:
            emkanat_list = x.css('[class*="amenities"]::text')
        if not emkanat_list:
            emkanat_list = x.css('[class*="facilities"]::text')
        emkanat = " ".join([str(em).strip() for em in emkanat_list]) if emkanat_list else "امکانات مشخص نشده"
        
        # Debug logging
        logger.info(f"Extracted details - Images: {len(images)}, Metrazh: {metrazh}, Room: {room}, Description length: {len(description)}")
        
        return {
            'images': images,  # Now returns list of images instead of single image
            'metrazh': metrazh.strip(),
            'sakht': sakht.strip(),
            'room': room.strip(),
            'prices3': prices3.strip(),
            'description': description.strip(),
            'emkanat': emkanat.strip()
        }
        
    except Exception as e:
        logger.error(f"Error fetching property details from {property_url}: {e}")
        return {
            'images': [],
            'metrazh': "خطا در دریافت",
            'sakht': "خطا در دریافت",
            'room': "خطا در دریافت",
            'prices3': "خطا در دریافت",
            'description': "خطا در دریافت اطلاعات",
            'emkanat': "خطا در دریافت"
        }

def get_property_listings(property_type: str, city_name: str = 'تهران', page: int = 1) -> tuple:
    """Get one fresh property listing from Divar for specified type and city
    Real-time fetching - each request gets fresh data from website
    Returns: (result_text, has_more, count, images_list)
    Developed by Mohammadreza Abedinpour for PIMX
    """
    try:
        english_city = translate_city_name(city_name)
        
        # Get the URL template for the property type
        if property_type not in property_urls:
            return f"❌ نوع ملک '{property_type}' شناخته نشد.", False, 0, []
        
        url = property_urls[property_type].format(city=english_city)
        
        # Add sort parameter to get newest listings first and page offset for real-time fetching
        # Add timestamp to avoid caching issues
        import time
        timestamp = int(time.time())
        
        if '?' in url:
            url += f'&sort=sort_date&page={page}&_t={timestamp}'
        else:
            url += f'?sort=sort_date&page={page}&_t={timestamp}'
        
        fetcher = Fetcher(auto_match=False)
        logger.info(f"Real-time fetching {property_type} for {city_name} - Page {page} (fresh data)")
        x = fetcher.get(url)
        
        names = x.css('div.kt-post-card__info > h2::text')
        mahales = x.css('div.kt-post-card__info > div.kt-post-card__bottom > span.kt-post-card__bottom-description.kt-text-truncate::text')
        
        # Extract property links using the correct CSS selector
        links = x.css('article a::attr(href)')
        if not links:
            # Try alternative selector
            links = x.css('.kt-post-card a::attr(href)')
        
        # If links are relative, make them absolute
        full_links = []
        for link in links:
            link_str = str(link)  # Convert Adaptor to string
            if link_str.startswith('/'):
                full_links.append(f'https://divar.ir{link_str}')
            elif link_str.startswith('http'):
                full_links.append(link_str)
            else:
                full_links.append(f'https://divar.ir/{link_str}')
        
        # Check if this is a rental property type (residential rent or commercial rent categories)
        rental_types = [
            'apartment_rent', 'villa_rent', 'residential_rent_all',  # Residential rent
            'office_rent', 'store_rent', 'industrial_rent', 'commercial_rent_all'  # Commercial rent
        ]
        
        if property_type in rental_types:
            # For rental properties: Extract both deposit (ودیعه) and rent (اجاره)
            prices1 = x.css('div > div.kt-post-card__info > div:nth-child(2)::text')  # ودیعه (deposit)
            prices2 = x.css('div.kt-post-card__info > div:nth-child(3)::text')  # اجاره (rent)
            
            # Combine deposit and rent information
            combined_prices = []
            for i in range(max(len(prices1), len(prices2))):
                deposit = str(prices1[i]) if i < len(prices1) else "نامشخص"
                rent = str(prices2[i]) if i < len(prices2) else "نامشخص"
                
                # Clean the text by removing existing "ودیعه:" and "اجاره:" labels if they exist
                deposit = deposit.replace("ودیعه:", "").strip()
                rent = rent.replace("اجاره:", "").strip()
                
                combined_prices.append(f"ودیعه: {deposit} | اجاره: {rent}")
            
            prices = combined_prices
        else:
            # For sale properties: Use single price extraction
            prices = x.css('div.kt-post-card__info > div.kt-post-card__description::text')
        
        # Extract property based on page to ensure variety (not always the first one)
        if names and len(names) > 0:
            # Use page number to select different property from available results
            # This helps avoid showing the same property repeatedly
            property_index = (page - 1) % len(names) if len(names) > 1 else 0
            
            name = names[property_index] if len(names) > property_index else names[0]
            price = prices[property_index] if len(prices) > property_index else (prices[0] if prices else "قیمت نامشخص")
            mahale = mahales[property_index] if len(mahales) > property_index else (mahales[0] if mahales else "محل نامشخص")
            link = full_links[property_index] if len(full_links) > property_index else (full_links[0] if full_links else "https://divar.ir")
            
            # Fetch detailed property information from individual page
            logger.info(f"Fetching detailed information for property: {name}")
            property_details = get_property_details(link)
            
            # Debug logging for property details
            logger.info(f"Property details extracted:")
            logger.info(f"  - Images: {len(property_details['images'])}")
            logger.info(f"  - Metrazh: '{property_details['metrazh']}'")
            logger.info(f"  - Room: '{property_details['room']}'")
            logger.info(f"  - Sakht: '{property_details['sakht']}'")
            logger.info(f"  - Description length: {len(property_details['description'])}")
            logger.info(f"  - Amenities length: {len(property_details['emkanat'])}") 
            
            # Always assume more properties available for continuous real-time fetching
            has_more = True  # Real-time mode: always fetch next property when requested
            
            # Get property type display name
            type_names = {
                'apartment_buy': 'آپارتمان (فروش)',
                'villa_buy': 'خانه و ویلا (فروش)',
                'land_buy': 'زمین و ملک کلنگی (فروش)',
                'residential_buy_all': 'همه مسکونی (فروش)',
                'apartment_rent': 'آپارتمان (اجاره)',
                'villa_rent': 'خانه و ویلا (اجاره)',
                'residential_rent_all': 'همه مسکونی (اجاره)',
                'office_buy': 'دفتر کار و مطب (فروش)',
                'store_buy': 'مغازه و غرفه (فروش)',
                'industrial_buy': 'صنعتی و کشاورزی (فروش)',
                'commercial_buy_all': 'همه تجاری (فروش)',
                'office_rent': 'دفتر کار و مطب (اجاره)',
                'store_rent': 'مغازه و غرفه (اجاره)',
                'industrial_rent': 'صنعتی و کشاورزی (اجاره)',
                'commercial_rent_all': 'همه تجاری (اجاره)',
                'all_properties': 'همه آگهی ها'
            }
            
            type_display = type_names.get(property_type, property_type)
            
            # Format property display with enhanced formatting and emojis
            property_display = f"🏠 **{name}**\n"
            
            # Price section with clear formatting
            property_display += f"\n💰 **قیمت**\n{price}\n"
            
            # Add detailed price if different from main price
            if property_details['prices3'] != "نامشخص" and property_details['prices3'] != price and property_details['prices3'] != "خطا در دریافت":
                property_display += f"💵 جزئیات قیمت: {property_details['prices3']}\n"
            
            # Location section
            property_display += f"\n📍 **مکان**\n{mahale}\n"
            
            # Property specifications section
            if any(detail != "نامشخص" and detail != "خطا در دریافت" for detail in [property_details['metrazh'], property_details['room'], property_details['sakht']]):
                property_display += f"\n📊 **مشخصات ملک**\n"
                
                if property_details['metrazh'] != "نامشخص" and property_details['metrazh'] != "خطا در دریافت":
                    property_display += f"📏 متراژ: {property_details['metrazh']} متر\n"
                
                if property_details['room'] != "نامشخص" and property_details['room'] != "خطا در دریافت":
                    property_display += f"🛏️ تعداد اتاق: {property_details['room']}\n"
                
                if property_details['sakht'] != "نامشخص" and property_details['sakht'] != "خطا در دریافت":
                    property_display += f"🏗️ سال ساخت: {property_details['sakht']}\n"
            
            # Description section - always show if available
            if (property_details['description'] != "توضیحات موجود نیست" and 
                property_details['description'] != "خطا در دریافت اطلاعات" and
                len(property_details['description'].strip()) > 0):
                desc = property_details['description']
                if len(desc) > 250:
                    desc = desc[:250] + "..."
                property_display += f"\n📝 **توضیحات**\n{desc}\n"
            
            # Amenities section - always show if available
            if (property_details['emkanat'] != "امکانات مشخص نشده" and 
                property_details['emkanat'] != "خطا در دریافت" and
                len(property_details['emkanat'].strip()) > 0):
                amenities = property_details['emkanat']
                if len(amenities) > 150:
                    amenities = amenities[:150] + "..."
                property_display += f"\n🏡 **امکانات و ویژگی‌ها**\n{amenities}\n"
            
            # Link section
            property_display += f"\n🔗 **لینک آگهی در دیوار**\n{link}"
            
            # Prepare property images for separate sending (up to 3)
            property_images = property_details['images'] if property_details['images'] else []
            
            result = f"🏘️ {type_display} در {city_name}:\n\n{property_display}"
            result += f"\n\n⚡ داده‌های زنده و تفصیلی از دیوار (صفحه {page})\n🏢 ارائه شده توسط PIMX\n👨‍💻 توسعه یافته توسط محمدرضا عابدین پور"
            
            return result, has_more, 1, property_images
        else:
            return f"❌ هیچ آگهی برای {property_type} در {city_name} پیدا نشد. لطفاً شهر دیگری امتحان کنید.", False, 0, []
        
    except Exception as e:
        logger.error(f"Error fetching {property_type} data for {city_name}: {e}")
        return f"❌ خطا در دریافت اطلاعات. لطفاً دوباره تلاش کنید.", False, 0, []

def get_welcome_message() -> str:
    """Get welcome message with main menu
    Developed by Mohammadreza Abedinpour for PIMX
    """
    return f"""🏙️ *سلام! به ربات جستجوی املاک PIMX خوش آمدید!*

🔍 *لطفاً نوع ملک مورد نظر خود را انتخاب کنید:*

💡 *راهنما:*
• ابتدا نوع ملک را انتخاب کنید
• سپس نام شهر را به فارسی ارسال کنید
• مثال: تهران، شیراز، اصفهان

🏢 *توسعه یافته توسط محمدرضا عابدین پور برای PIMX*"""

# Telegram bot handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handle /start and /help commands"""
    try:
        welcome_msg = get_welcome_message()
        markup = create_main_menu()
        bot.reply_to(message, welcome_msg, parse_mode='Markdown', reply_markup=markup)
        logger.info(f"Welcome message sent to user {message.from_user.id}")
        
        # Initialize user state
        user_states[message.from_user.id] = {
            'waiting_for_city': False, 
            'selected_property_type': None,
            'current_city': None,
            'current_page': 1
        }
        
    except Exception as e:
        logger.error(f"Error sending welcome message: {e}")
        bot.reply_to(message, "خطا در ارسال پیام خوشامدگویی. لطفاً دوباره تلاش کنید.")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Handle all callback queries from inline keyboards"""
    try:
        user_id = call.from_user.id
        data = call.data
        
        logger.info(f"Callback received from user {user_id}: {data}")
        
        # Initialize user state if not exists
        if user_id not in user_states:
            user_states[user_id] = {
                'waiting_for_city': False, 
                'selected_property_type': None,
                'current_city': None,
                'current_page': 1
            }
        
        # Handle pagination - continue button
        if data.startswith("continue_"):
            logger.info(f"Pagination request received - Current state: {user_states.get(user_id, {})}")
            
            if user_id in user_states and user_states[user_id]['selected_property_type'] and user_states[user_id]['current_city']:
                # Get next page of results with fresh restart-like behavior
                property_type = user_states[user_id]['selected_property_type']
                city_name = user_states[user_id]['current_city']
                current_page = user_states[user_id]['current_page'] + 1
                
                logger.info(f"Fetching page {current_page} for {property_type} in {city_name}")
                
                # Send "fetching" message to simulate restart behavior
                fetching_msg = bot.send_message(call.message.chat.id, "🔄 در حال دریافت آگهی جدید...")
                
                result, has_more, total_properties, property_images = get_property_listings(property_type, city_name, current_page)
                
                # Delete fetching message
                bot.delete_message(call.message.chat.id, fetching_msg.message_id)
                
                # Update user state
                user_states[user_id]['current_page'] = current_page
                
                logger.info(f"Retrieved property with {len(property_images) if property_images else 0} images")
                
                # Send property images first if available (up to 3)
                images_sent = 0
                if property_images:
                    for i, image_url in enumerate(property_images[:3]):
                        try:
                            caption = f"🖼️ تصویر ملک {i+1}"
                            bot.send_photo(call.message.chat.id, image_url, caption=caption)
                            images_sent += 1
                            logger.info(f"Successfully sent image {i+1} for property")
                        except Exception as e:
                            logger.error(f"Error sending image {i+1} ({image_url}): {e}")
                            # Continue without this image if sending fails
                    
                    logger.info(f"Total images sent: {images_sent} out of {len(property_images)} available")
                
                # Send property details
                bot.send_message(call.message.chat.id, result)
                
                # Add pagination info message for real-time fetching
                if has_more:
                    pagination_text = f"📝 برای مشاهده جدیدترین آگهی روی 'آگهی بعدی' بزنید\n⚡ هر بار داده‌های تازه از دیوار دریافت می‌شود\n🏠 برای جستجوی جدید روی 'منو' بزنید"
                else:
                    pagination_text = f"🎆 تمام آگهی‌ها نمایش داده شد!\n🏠 برای جستجوی جدید روی 'منو' بزنید"
                
                pagination_markup = create_pagination_menu(user_id, has_more)
                bot.send_message(call.message.chat.id, pagination_text, reply_markup=pagination_markup)
                
                logger.info(f"Pagination - Page {current_page} sent for {property_type} in {city_name}")
            
            bot.answer_callback_query(call.id)
            return
        
        # Handle main menu selections
        if data == "residential_sale":
            markup = create_residential_sale_menu()
            bot.edit_message_text(
                "🏠 *فروش مسکونی*\n\nلطفاً نوع ملک مورد نظر خود را انتخاب کنید:",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown',
                reply_markup=markup
            )
            
        elif data == "residential_rent":
            markup = create_residential_rent_menu()
            bot.edit_message_text(
                "🏡 *اجاره مسکونی*\n\nلطفاً نوع ملک مورد نظر خود را انتخاب کنید:",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown',
                reply_markup=markup
            )
            
        elif data == "commercial_sale":
            markup = create_commercial_sale_menu()
            bot.edit_message_text(
                "🏢 *فروش اداری و تجاری*\n\nلطفاً نوع ملک مورد نظر خود را انتخاب کنید:",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown',
                reply_markup=markup
            )
            
        elif data == "commercial_rent":
            markup = create_commercial_rent_menu()
            bot.edit_message_text(
                "🏬 *اجاره اداری و تجاری*\n\nلطفاً نوع ملک مورد نظر خود را انتخاب کنید:",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown',
                reply_markup=markup
            )
            
        # Handle back to main menu
        elif data == "back_to_main":
            markup = create_main_menu()
            welcome_msg = get_welcome_message()
            bot.edit_message_text(
                welcome_msg,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown',
                reply_markup=markup
            )
            user_states[user_id] = {
                'waiting_for_city': False, 
                'selected_property_type': None,
                'current_city': None,
                'current_page': 1
            }
            
        # Handle property type selections
        elif data.startswith("property_"):
            property_type = data.replace("property_", "")
            user_states[user_id] = {
                'waiting_for_city': True, 
                'selected_property_type': property_type,
                'current_city': None,
                'current_page': 1
            }
            
            # Get property type display name
            type_names = {
                'apartment_buy': 'آپارتمان (فروش)',
                'villa_buy': 'خانه و ویلا (فروش)',
                'land_buy': 'زمین و ملک کلنگی (فروش)',
                'residential_buy_all': 'همه مسکونی (فروش)',
                'apartment_rent': 'آپارتمان (اجاره)',
                'villa_rent': 'خانه و ویلا (اجاره)',
                'residential_rent_all': 'همه مسکونی (اجاره)',
                'office_buy': 'دفتر کار و مطب (فروش)',
                'store_buy': 'مغازه و غرفه (فروش)',
                'industrial_buy': 'صنعتی و کشاورزی (فروش)',
                'commercial_buy_all': 'همه تجاری (فروش)',
                'office_rent': 'دفتر کار و مطب (اجاره)',
                'store_rent': 'مغازه و غرفه (اجاره)',
                'industrial_rent': 'صنعتی و کشاورزی (اجاره)',
                'commercial_rent_all': 'همه تجاری (اجاره)',
                'all_properties': 'همه آگهی ها'
            }
            
            type_display = type_names.get(property_type, property_type)
            
            cities_text = "، ".join(list(city_translations.keys())[:10])
            
            bot.edit_message_text(
                f"🏯 *{type_display}*\n\n🏙️ **لطفاً نام شهر را به فارسی ارسال کنید:**\n\n🏠 *شهرهای قابل جستجو:*\n{cities_text}\n\n📝 *مثال:* تهران، شیراز، اصفهان",
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            
        # Answer the callback query
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        logger.error(f"Error handling callback query: {e}")
        bot.answer_callback_query(call.id, "خطا در پردازش درخواست")

@bot.message_handler(func=lambda message: True)
def handle_city_input(message):
    """Handle city name input from users"""
    try:
        user_input = message.text.strip()
        user_id = message.from_user.id
        
        logger.info(f"Received message from user {user_id}: {user_input}")
        
        # Check if user is in a state waiting for city input
        if user_id in user_states and user_states[user_id]['waiting_for_city']:
            property_type = user_states[user_id]['selected_property_type']
            
            # Send typing action
            bot.send_chat_action(message.chat.id, 'typing')
            
            # Check if it's a valid city
            if user_input in city_translations:
                # Send processing message
                processing_msg = bot.reply_to(message, f"🔍 در حال جستجو برای {user_input}...")
                
                # Get property listings (first page)
                result, has_more, total_properties, property_images = get_property_listings(property_type, user_input, 1)
                
                # Update user state
                user_states[user_id] = {
                    'waiting_for_city': False, 
                    'selected_property_type': property_type,
                    'current_city': user_input,
                    'current_page': 1
                }
                
                # Delete processing message
                bot.delete_message(message.chat.id, processing_msg.message_id)
                
                # Send property images first if available (up to 3)
                images_sent = 0
                if property_images:
                    for i, image_url in enumerate(property_images[:3]):
                        try:
                            caption = f"🖼️ تصویر ملک {i+1}"
                            bot.send_photo(message.chat.id, image_url, caption=caption)
                            images_sent += 1
                            logger.info(f"Successfully sent image {i+1} for property")
                        except Exception as e:
                            logger.error(f"Error sending image {i+1} ({image_url}): {e}")
                            # Continue without this image if sending fails
                    
                    logger.info(f"Total images sent: {images_sent} out of {len(property_images)} available")
                
                # Send property details
                bot.reply_to(message, result)
                
                # Add pagination info and buttons for real-time fetching
                if has_more:
                    pagination_text = f"📝 برای مشاهده جدیدترین آگهی روی 'آگهی بعدی' بزنید\n⚡ هر بار داده‌های تازه از دیوار دریافت می‌شود\n🏠 برای جستجوی جدید روی 'منو' بزنید"
                else:
                    pagination_text = f"🎆 هیچ آگهی بیشتری یافت نشد!\n🏠 برای جستجوی جدید روی 'منو' بزنید"
                
                pagination_markup = create_pagination_menu(user_id, has_more)
                bot.send_message(message.chat.id, pagination_text, reply_markup=pagination_markup)
                
                logger.info(f"Property listings sent for {property_type} in {user_input} - Page 1")
                
            else:
                # City not found
                error_msg = f"⚠️ شهر '{user_input}' در لیست شهرهای موجود نیست.\n\n"
                error_msg += "🔄 لطفاً از شهرهای زیر یکی را انتخاب کنید:\n"
                error_msg += "تهران، شیراز، اصفهان، مشهد، تبریز، کرج، اهواز، قم، رشت، کرمان"
                
                bot.reply_to(message, error_msg)
                logger.info(f"Invalid city received: {user_input}")
        else:
            # User sent a message without selecting property type first
            welcome_msg = get_welcome_message()
            markup = create_main_menu()
            bot.reply_to(message, welcome_msg, parse_mode='Markdown', reply_markup=markup)
            user_states[user_id] = {'waiting_for_city': False, 'selected_property_type': None}
            
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        bot.reply_to(message, "❌ خطا در پردازش درخواست. لطفاً دوباره تلاش کنید.")

def run_bot():
    """Run the Telegram bot with error handling and auto-restart
    Developed by Mohammadreza Abedinpour for PIMX
    """
    logger.info("🤖 PIMX House Search Bot Started!")
    logger.info("🏢 Developed by Mohammadreza Abedinpour for PIMX")
    logger.info("=" * 50)
    
    # Start bot with auto-restart on error
    while True:
        try:
            logger.info("🔄 Starting bot polling...")
            bot.polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            logger.error(f"Bot error: {e}")
            logger.info("🔄 Restarting bot in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    run_bot()