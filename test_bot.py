from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8279777997:AAGKbKWpJt2fxzxlGK9SDuWvMTn4-wsub8c"

# Database connection
def get_db():
    conn = sqlite3.connect('healthcare.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== COMMAND HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - Welcome message"""
    user = update.effective_user
    message = f"""
👋 **Welcome {user.first_name}!**

🏥 **Healthcare Assistant Bot**

I can help you find hospitals and get health advice.

**What can I do?**
📍 Find hospitals by area
💊 Get health advice
📞 Find hospital contact details
🏥 List all areas with hospitals

**Try these:**
• `hospitals kukatpally`
• `hospitals aziznagar`
• `I have fever`
• `hospital contact details`
• `/help` - See all commands
"""
    await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
🏥 **Healthcare Bot - Help**

**Find Hospitals:**
• `hospitals [area name]` - Find hospitals in area
  Example: `hospitals kukatpally`
  
• `hospitals in narsingi` - Alternative format

**Get Health Advice:**
• Type your symptoms: `fever`, `cough`, `cold`, `headache`, `chest pain`
  Example: `I have fever`

**List Areas:**
• `/areas` - Show all hospital areas

**Available Areas:**
🔹 Kukatpally
🔹 Aziznagar  
🔹 Narsingi
🔹 Jubilee Hills
🔹 Shamshabad

**Commands:**
/start - Start bot
/help - Show this help
/areas - List all areas
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def areas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all areas"""
    conn = get_db()
    areas_list = conn.execute(
        'SELECT DISTINCT area FROM hospitals ORDER BY area'
    ).fetchall()
    conn.close()
    
    if areas_list:
        message = "🗺️ **Available Hospital Areas:**\n\n"
        for i, area in enumerate(areas_list, 1):
            message += f"{i}. {area['area']}\n"
        message += "\n💡 Try: `hospitals [area name]`"
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ No areas found")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    text = update.message.text.lower()
    user = update.effective_user
    
    # Search hospitals by area
    if 'hospital' in text:
        await search_hospitals(update, context, text)
    
    # Health advice
    elif any(word in text for word in ['fever', 'cough', 'cold', 'pain', 'headache', 'dizzy', 'nausea']):
        await give_health_advice(update, context, text)
    
    # Default
    else:
        response = """
I didn't understand. Try:
• `hospitals kukatpally`
• `I have fever`
• `/help` for more options
"""
        await update.message.reply_text(response)

async def search_hospitals(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Search hospitals by area"""
    # Extract area name
    if 'in ' in text:
        area = text.split('in ')[-1].strip()
    elif 'hospital' in text:
        parts = text.replace('hospital', '').strip().split()
        area = parts[0] if parts else None
    else:
        area = None
    
    if not area or len(area) < 2:
        await update.message.reply_text("❌ Please specify an area name.\nExample: `hospitals kukatpally`")
        return
    
    # Search database
    conn = get_db()
    hospitals = conn.execute(
        'SELECT hospital_id, name, phone, address FROM hospitals WHERE area LIKE ? ORDER BY name',
        (f'%{area}%',)
    ).fetchall()
    conn.close()
    
    if hospitals:
        response = f"🏥 **Hospitals in {area.title()}:**\n\n"
        for i, h in enumerate(hospitals, 1):
            response += f"{i}. {h['name']}\n"
            response += f"   📞 {h['phone']}\n"
            response += f"   📌 {h['address']}\n\n"
        await update.message.reply_text(response, parse_mode='Markdown')
    else:
        await update.message.reply_text(f"❌ No hospitals found in '{area}'.\n\nAvailable areas:\n• Kukatpally\n• Aziznagar\n• Narsingi\n• Jubilee Hills\n• Shamshabad")

async def give_health_advice(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Give health advice based on symptoms"""
    advice_map = {
        'fever': """🌡️ **Fever Management:**

✓ Rest and sleep well
✓ Drink plenty of water (2-3 liters)
✓ Use cool compress on forehead
✓ Take paracetamol (500mg) if needed
✓ Light clothing

⚠️ **See doctor if:**
- Fever > 103°F / 39.4°C
- Lasts > 3 days
- Accompanied by rash
- Severe headache

🏥 Need hospital? Type: `hospitals [area]`""",

        'cough': """🤧 **Cough Management:**

✓ Stay hydrated
✓ Use honey and warm water
✓ Get plenty of rest
✓ Use cough syrup if needed
✓ Avoid cold foods

⚠️ **See doctor if:**
- Cough > 2 weeks
- Coughing blood
- Severe chest pain
- Difficulty breathing

🏥 Need hospital? Type: `hospitals [area]`""",

        'cold': """❄️ **Cold Management:**

✓ Rest (6-8 hours sleep)
✓ Warm fluids (tea, soup)
✓ Gargle salt water
✓ Vitamin C rich foods
✓ Steam inhalation

⚠️ **See doctor if:**
- Symptoms don't improve in 7-10 days
- Develop high fever
- Severe congestion

🏥 Need hospital? Type: `hospitals [area]`""",

        'headache': """🤕 **Headache Management:**

✓ Rest in quiet, dark room
✓ Stay hydrated
✓ Cold compress
✓ Take paracetamol (500mg)
✓ Avoid bright lights

⚠️ **See doctor if:**
- Severe and sudden
- Accompanied by fever/vomiting
- Neck stiffness
- Vision changes

🏥 Need hospital? Type: `hospitals [area]`""",

        'pain': """💊 **Pain Management:**

✓ Rest the affected area
✓ Ice pack for swelling
✓ Elevation if needed
✓ Take pain reliever
✓ Gentle stretching

⚠️ **Seek emergency if:**
- Chest pain
- Severe abdominal pain
- Pain after injury

🏥 Need hospital? Type: `hospitals [area]`"""
    }
    
    response = "I understand you're not feeling well.\n\n"
    
    # Match symptoms
    found = False
    for symptom, advice in advice_map.items():
        if symptom in text:
            response = advice
            found = True
            break
    
    if not found:
        response = """💊 **General Health Advice:**

✓ Rest well
✓ Drink plenty of water
✓ Healthy diet
✓ Monitor symptoms
✓ See doctor if symptoms persist

🏥 Need hospital? Type: `hospitals [area]`"""
    
    await update.message.reply_text(response, parse_mode='Markdown')

# ==================== MAIN ====================

async def main():
    """Start the bot"""
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("areas", areas))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot Started! Polling for messages...")
    print("🏥 Healthcare Bot is running!")
    
    # Start polling
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
