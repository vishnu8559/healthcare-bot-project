from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import sqlite3
import math

# Conversation states
WAITING_FOR_SYMPTOM, ASKING_HOSPITAL, WAITING_FOR_LOCATION = range(3)

# Haversine distance calculation
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Get hospitals from database
def get_hospitals_by_area(area):
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.execute("SELECT name, address, phone FROM hospitals WHERE area LIKE ?", (f'%{area}%',))
    results = cursor.fetchall()
    conn.close()
    return results

def get_nearby_hospitals(user_lat, user_lon, n=5):
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.execute("SELECT name, address, phone, lat, lon FROM hospitals WHERE lat IS NOT NULL AND lon IS NOT NULL")
    hospitals = cursor.fetchall()
    conn.close()
    
    if not hospitals:
        return []
    
    hospitals_with_dist = []
    for h in hospitals:
        name, address, phone, lat, lon = h
        distance = haversine(user_lat, user_lon, lat, lon)
        hospitals_with_dist.append((name, address, phone, distance))
    
    hospitals_with_dist.sort(key=lambda x: x[3])
    return hospitals_with_dist[:n]

# Health advice based on symptoms
def get_health_advice(symptom):
    symptom_lower = symptom.lower()
    
    if 'fever' in symptom_lower:
        return "I'm sorry to hear you have a fever. Rest well and stay hydrated. Monitor your temperature regularly."
    elif 'headache' in symptom_lower or 'head' in symptom_lower:
        return "Headaches can be tough! Try to rest in a quiet, dark room and stay hydrated."
    elif 'cough' in symptom_lower or 'cold' in symptom_lower:
        return "Take care of yourself! Rest, drink warm fluids, and avoid cold air."
    elif 'stomach' in symptom_lower or 'pain' in symptom_lower:
        return "I understand you're not feeling well. Try to rest and avoid heavy meals for now."
    elif 'chest' in symptom_lower or 'breath' in symptom_lower:
        return "Please take this seriously. Rest and avoid any strenuous activity."
    else:
        return "I hope you feel better soon. Make sure to rest and take care of yourself."

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm your healthcare assistant. 😊\n\n"
        "How are you feeling today? Tell me your symptoms.\n"
        "(For example: 'I have a fever' or 'I have a headache')"
    )
    return WAITING_FOR_SYMPTOM

# Handle symptom input
async def handle_symptom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symptom = update.message.text
    context.user_data['symptom'] = symptom
    
    # Give health advice
    advice = get_health_advice(symptom)
    
    # Ask if they want to find a hospital
    keyboard = [
        [KeyboardButton("Yes, find hospitals 🏥")],
        [KeyboardButton("No, thank you")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        f"{advice}\n\n"
        "Would you like me to help you find nearby hospitals?",
        reply_markup=reply_markup
    )
    
    return ASKING_HOSPITAL

# Handle hospital choice
async def handle_hospital_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text.lower()
    
    if 'yes' in response or 'find' in response:
        # Ask for location
        location_button = KeyboardButton("📍 Share My Location", request_location=True)
        keyboard = [[location_button], [KeyboardButton("Or type area name")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "Great! I can help you find hospitals.\n\n"
            "Please share your location or type your area name:",
            reply_markup=reply_markup
        )
        return WAITING_FOR_LOCATION
    else:
        await update.message.reply_text(
            "Alright! Take care and feel better soon. 🙏\n\n"
            "If you need help anytime, just type /start",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

# Handle location sharing
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    user_lat = location.latitude
    user_lon = location.longitude
    
    hospitals = get_nearby_hospitals(user_lat, user_lon, 5)
    
    if hospitals:
        msg = "🏥 *Here are the nearest hospitals:*\n\n"
        for i, (name, address, phone, distance) in enumerate(hospitals, 1):
            msg += f"{i}. *{name}*\n"
            msg += f"   📍 {address}\n"
            msg += f"   📞 {phone}\n"
            msg += f"   📏 {distance:.2f} km away\n\n"
        msg += "Stay safe and get well soon! 💙"
    else:
        msg = "I couldn't find hospitals with location data in the system yet.\nPlease type your area name instead."
        return WAITING_FOR_LOCATION
    
    await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Handle area text input
async def handle_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    area = update.message.text
    
    # Skip if user clicked "Or type area name" button
    if area.lower() == "or type area name":
        await update.message.reply_text("Please type your area name (e.g., Warangal, Kukatpally):")
        return WAITING_FOR_LOCATION
    
    hospitals = get_hospitals_by_area(area)
    
    if hospitals:
        msg = f"🏥 *Hospitals in {area}:*\n\n"
        for i, (name, address, phone) in enumerate(hospitals, 1):
            msg += f"{i}. *{name}*\n"
            msg += f"   📍 {address}\n"
            msg += f"   📞 {phone}\n\n"
        msg += "Take care and feel better soon! 💙"
    else:
        msg = f"Sorry, I couldn't find hospitals in '{area}'.\nTry another area name or share your location."
        return WAITING_FOR_LOCATION
    
    await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Cancel conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "No problem! Stay healthy. Type /start if you need help again.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Main
if __name__ == '__main__':
    TOKEN = "8279777997:AAGKbKWpJt2fxzxlGK9SDuWvMTn4-wsub8c"  # Replace with your actual token
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_FOR_SYMPTOM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_symptom)],
            ASKING_HOSPITAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hospital_choice)],
            WAITING_FOR_LOCATION: [
                MessageHandler(filters.LOCATION, handle_location),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_area)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    app.add_handler(conv_handler)
    
    print("🤖 Healthcare Bot is running...")
    print("Open Telegram and chat with your bot!")
    app.run_polling()
