#agno
"""
PIMX Interactive House Search Telegram Bot
Developed by Mohammadreza Abedinpour for PIMX

This bot asks users for city names and provides house listings from Divar.
"""

from agno.agent import Agent
from agno.tools import tool
from scrapling import Fetcher
from agno.tools.telegram import TelegramTools
from agno.models.google import Gemini
import os
import time

# Agent configuration with Gemini model
token = "8273383219:AAEUQshygEWA25SuAa5nhkfP1SqgSKBnLV4"
chatid = "5675632554"

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

def translate_city_name(persian_city: str) -> str:
    """Convert Persian city name to English for Divar URL
    Developed by Mohammadreza Abedinpour for PIMX
    """
    # Remove extra spaces and normalize
    persian_city = persian_city.strip()
    
    # Check if city exists in our translation dictionary
    english_city = city_translations.get(persian_city)
    
    if english_city:
        return english_city
    else:
        # If city not found, return tehran as default and log the issue
        print(f"City '{persian_city}' not found in translations. Using Tehran as default.")
        return 'tehran'

@tool(name='welcome_user', description='Welcome new users and ask for city name')
def welcome_user():
    """Welcome message and city selection for new users
    Developed by Mohammadreza Abedinpour for PIMX
    """
    return """🏙️ سلام! به ربات جستجوی املاک PIMX خوش آمدید!

🏠 لطفاً نام شهر مورد نظر خود را برای جستجوی خانه وارد کنید:

🌆 شهرهای قابل جستجو:
• تهران
• شیراز
• اصفهان
• مشهد
• تبریز
• کرج
• اهواز
• قم
• رشت
• کرمان
• همدان
• یزد
• اردبیل
• بندرعباس
• کرمانشاه
• زاهدان
• ساری
• قزوین
• خرم آباد
• گرگان

💡 فقط نام شهر را تایپ کنید...

🏢 توسعه یافته توسط محمدرضا عابدین پور برای PIMX"""

@tool(name='get_city_houses', description='Get house listings for specified city')
def get_city_houses(city_name: str):
    """Get house listings from Divar for specified city
    Developed by Mohammadreza Abedinpour for PIMX
    """
    # Translate city name from Persian to English
    english_city = translate_city_name(city_name)
    
    # Check if it's a valid city
    if english_city == 'tehran' and city_name != 'تهران':
        available_cities = "، ".join(list(city_translations.keys()))
        return f"""⚠️ شهر '{city_name}' در لیست شهرهای موجود نیست.

🔄 لطفاً از شهرهای زیر یکی را انتخاب کنید:
{available_cities}

💡 فقط نام شهر را وارد کنید..."""
    
    fetcher = Fetcher()
    # Use dynamic city name in URL
    url = f'https://divar.ir/s/{english_city}/buy-residential?business-type=personal&map_bbox=51.10746383666992%2C35.604400634765625%2C51.63630676269531%2C35.828468322753906&map_interaction=list_only_used&map_place_hash=1%7C%7Cresidential-sell'
    
    try:
        x = fetcher.get(url, stealthy_headers=True)
        print(f"Fetching data for city: {city_name} ({english_city})")
        print(x.reason)
        
        names = x.css('div.kt-post-card__info > h2::text')
        prices = x.css('div.kt-post-card__info > div.kt-post-card__description::text')
        mahales = x.css('div.kt-post-card__info > div.kt-post-card__bottom > span.kt-post-card__bottom-description.kt-text-truncate::text') 
        
        houses = list(zip(names, prices, mahales))
        
        if not houses:
            return f"❌ هیچ آگهی املاکی برای {city_name} ({english_city}) پیدا نشد. لطفاً شهر دیگری امتحان کنید."
        
        houses_lines = [f"🏠 {name} | 💰 {price} | 📍 {mahale}" for name, price, mahale in houses[:10]]  # Limit to 10 results
        result = f"🏘️ لیست املاک در {city_name}:\n\n" + "\n\n".join(houses_lines)
        result += f"\n\n📊 تعداد کل آگهی ها: {len(houses)}"
        result += f"\n\n🏢 ارائه شده توسط PIMX - توسعه یافته توسط محمدرضا عابدین پور"
        
        return result
        
    except Exception as e:
        return f"❌ خطا در دریافت اطلاعات برای {city_name}. لطفاً دوباره تلاش کنید.\n\n🔧 جزئیات خطا: {str(e)}"

# Create agent for interactive conversations
agent = Agent(
    name="PIMX Interactive House Search Bot",
    markdown=True,
    model=model,
    tools=[welcome_user, get_city_houses, TelegramTools(chat_id=chatid, token=token)],
    instructions="""
    You are PIMX Interactive House Search Bot developed by Mohammadreza Abedinpour.
    
    When user starts conversation or says hello:
    1. Use welcome_user tool to greet and show city options
    2. Send the welcome message to Telegram
    
    When user provides a city name:
    1. Use get_city_houses tool to get listings for that city
    2. Send the results to Telegram
    
    Always respond in Persian for Iranian users.
    Always include PIMX branding in responses.
    Keep responses friendly and helpful.
    """
)

def run_bot():
    """Run the interactive bot continuously
    Developed by Mohammadreza Abedinpour for PIMX
    """
    print("🤖 PIMX House Search Bot Started!")
    print("🏢 Developed by Mohammadreza Abedinpour for PIMX")
    print("=" * 50)
    
    # Send welcome message when bot starts
    print("📤 Sending welcome message...")
    response = agent.print_response("سلام! ربات جدید شروع شد. پیام خوشامدگویی را نمایش بده و به تلگرام بفرست")
    print(f"✅ Welcome sent: {response}")
    
    print("\n🔄 Bot is ready for user interactions...")
    print("💡 Users can now send city names to get house listings!")
    
    # In a real implementation, this would be connected to Telegram webhook
    # For now, we'll simulate user interactions
    while True:
        try:
            print("\n" + "="*50)
            user_input = input("👤 Simulate user input (city name or 'quit' to exit): ")
            
            if user_input.lower() == 'quit':
                print("🛑 Bot stopped.")
                break
                
            if user_input.strip():
                print(f"📥 Processing user input: {user_input}")
                response = agent.print_response(f"کاربر '{user_input}' رو وارد کرد. اگر نام شهره اطلاعات املاک رو بگیر و به تلگرام بفرست")
                print(f"📤 Response sent: {response}")
                
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    run_bot()