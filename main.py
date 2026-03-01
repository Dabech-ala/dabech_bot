import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8643947663:AAEViQoN2SGmX1q43CsI31Wj5O5nC_mhT4c'
PAIRS = ["GOLD (XAU/USD)", "EUR/USD", "GBP/USD", "USD/JPY"]
stats = {"win": 0, "loss": 0}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = "مرحبا بيك مع بوت دباش لادارة مخاطر راس المال والربح الحقيقي المربح والمريح 👑"
    keyboard = [[InlineKeyboardButton(f"{p} 🔥" if random.random() > 0.5 else p, callback_data=f"p_{p}")] for p in PAIRS]
    if update.message:
        await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith("p_"):
        pair = query.data.split("_")[1]
        arrow = random.choice(["⬆️ صعود", "⬇️ هبوط"])
        await query.edit_message_text(f"{arrow}") 
        await asyncio.sleep(5) 
        keys = [[InlineKeyboardButton("✅ ربحت", callback_data="r_w"), InlineKeyboardButton("❌ خسرت", callback_data="r_l")]]
        await query.edit_message_text(f"🏁 النتيجة ({pair})؟", reply_markup=InlineKeyboardMarkup(keys))
    elif query.data.startswith("r_"):
        res = query.data.split("_")[1]
        if res == "w": stats["win"] += 1
        else: stats["loss"] += 1
        report = f"📊 **جدول الحساب:**\n✅ ربح: {stats['win']}\n❌ خسارة: {stats['loss']}"
        keys = [[InlineKeyboardButton("🎯 إشارة جديدة", callback_data="back")], [InlineKeyboardButton("🔄 تغيير الزوج", callback_data="back")]]
        await query.edit_message_text(report, reply_markup=InlineKeyboardMarkup(keys), parse_mode='Markdown')
    elif query.data == "back": await start(update, context)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle))
    app.run_polling(drop_pending_updates=True)
