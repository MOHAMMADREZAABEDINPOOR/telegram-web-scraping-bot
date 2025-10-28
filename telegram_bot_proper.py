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
PROPERTIES_PER_PAGE = 10

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
    """Create pagination menu with continue and main menu options
    Developed by Mohammadreza Abedinpour for PIMX
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if has_more:
        btn_continue = types.InlineKeyboardButton("➡️ ادامه", callback_data=f"continue_{user_id}")
        btn_menu = types.InlineKeyboardButton("🏠 منو", callback_data="back_to_main")
        markup.add(btn_continue, btn_menu)
    else:
        btn_menu = types.InlineKeyboardButton("🏠 بازگشت به منو", callback_data="back_to_main")
        markup.add(btn_menu)
    
    return markup

def get_property_listings(property_type: str, city_name: str = 'تهران', page: int = 1) -> tuple:
    """Get property listings from Divar for specified type and city
    Returns (result_text, has_more_pages, total_properties)
    Developed by Mohammadreza Abedinpour for PIMX
    """
    try:
        english_city = translate_city_name(city_name)
        
        # Get the URL template for the property type
        if property_type not in property_urls:
            return f"❌ نوع ملک '{property_type}' شناخته نشد.", False, 0
        
        url = property_urls[property_type].format(city=english_city)
        
        fetcher = Fetcher()
        logger.info(f"Fetching {property_type} data for city: {city_name} ({english_city}) - Page {page}")
        x = fetcher.get(url, stealthy_headers=True)
        
        names = x.css('div.kt-post-card__info > h2::text')
        mahales = x.css('div.kt-post-card__info > div.kt-post-card__bottom > span.kt-post-card__bottom-description.kt-text-truncate::text')
        
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
                deposit = prices1[i] if i < len(prices1) else "نامشخص"
                rent = prices2[i] if i < len(prices2) else "نامشخص"
                
                # Clean the text by removing existing "ودیعه:" and "اجاره:" labels if they exist
                deposit = deposit.replace("ودیعه:", "").strip()
                rent = rent.replace("اجاره:", "").strip()
                
                combined_prices.append(f"ودیعه: {deposit} | اجاره: {rent}")
            
            properties = list(zip(names, combined_prices, mahales))
        else:
            # For sale properties: Use single price extraction
            prices = x.css('div.kt-post-card__info > div.kt-post-card__description::text')
            properties = list(zip(names, prices, mahales))
        
        if not properties:
            return f"❌ هیچ آگهی برای {property_type} در {city_name} پیدا نشد. لطفاً شهر دیگری امتحان کنید.", False, 0
        
        # Calculate pagination
        start_index = (page - 1) * PROPERTIES_PER_PAGE
        end_index = start_index + PROPERTIES_PER_PAGE
        current_page_properties = properties[start_index:end_index]
        has_more = end_index < len(properties)
        
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
        
        # Create page header
        page_info = f" - صفحه {page}" if page > 1 else ""
        
        properties_lines = [f"🏠 {name}\n💰 {price}\n📍 {mahale}" for name, price, mahale in current_page_properties]
        result = f"🏘️ *{type_display} در {city_name}{page_info}:*\n\n" + "\n\n".join(properties_lines)
        result += f"\n\n📊 *نمایش:* {start_index + 1}-{min(end_index, len(properties))} از {len(properties)} آگهی"
        result += f"\n\n🏢 *ارائه شده توسط PIMX*\n👨‍💻 *توسعه یافته توسط محمدرضا عابدین پور*"
        
        return result, has_more, len(properties)
        
    except Exception as e:
        logger.error(f"Error fetching {property_type} data for {city_name}: {e}")
        return f"❌ خطا در دریافت اطلاعات. لطفاً دوباره تلاش کنید.", False, 0

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
            if user_id in user_states and user_states[user_id]['selected_property_type'] and user_states[user_id]['current_city']:
                # Get next page of results
                property_type = user_states[user_id]['selected_property_type']
                city_name = user_states[user_id]['current_city']
                current_page = user_states[user_id]['current_page'] + 1
                
                result, has_more, total_properties = get_property_listings(property_type, city_name, current_page)
                
                # Update user state
                user_states[user_id]['current_page'] = current_page
                
                # Send results with pagination menu
                bot.send_message(call.message.chat.id, result, parse_mode='Markdown')
                
                # Add pagination info message
                if has_more:
                    pagination_text = f"📝 *اگر می‌خواهید آگهی بیشتر دریافت کنید روی دکمه ادامه بزنید*\n🏠 *اگر می‌خواهید جستجوی جدید داشته باشید روی دکمه منو بزنید*"
                else:
                    pagination_text = f"🎆 *تمام آگهی‌ها نمایش داده شد!*\n🏠 *برای جستجوی جدید روی دکمه منو بزنید*"
                
                pagination_markup = create_pagination_menu(user_id, has_more)
                bot.send_message(call.message.chat.id, pagination_text, parse_mode='Markdown', reply_markup=pagination_markup)
                
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
                result, has_more, total_properties = get_property_listings(property_type, user_input, 1)
                
                # Update user state
                user_states[user_id] = {
                    'waiting_for_city': False, 
                    'selected_property_type': property_type,
                    'current_city': user_input,
                    'current_page': 1
                }
                
                # Delete processing message and send result
                bot.delete_message(message.chat.id, processing_msg.message_id)
                bot.reply_to(message, result, parse_mode='Markdown')
                
                # Add pagination info and buttons
                if has_more:
                    pagination_text = f"📝 *اگر می‌خواهید آگهی بیشتر دریافت کنید روی دکمه ادامه بزنید*\n🏠 *اگر می‌خواهید جستجوی جدید داشته باشید روی دکمه منو بزنید*"
                else:
                    pagination_text = f"🎆 *تمام آگهی‌ها نمایش داده شد!*\n🏠 *برای جستجوی جدید روی دکمه منو بزنید*"
                
                pagination_markup = create_pagination_menu(user_id, has_more)
                bot.send_message(message.chat.id, pagination_text, parse_mode='Markdown', reply_markup=pagination_markup)
                
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