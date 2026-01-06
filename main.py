import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# 1. ТОКЕН ЖӘНЕ БОТТЫ АНЫҚТАУ
API_TOKEN = '7662747196:AAHR1ilcQgL8dyaLQ5G1d9MJCD9ddXyVx5E'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 2. МӘЗІРЛЕРДІ ҚҰРАСТЫРУ
# Басты мәзір (Reply)
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Күндік сабақтар"), KeyboardButton(text="📖 Сөздіктер")],
        [KeyboardButton(text="🎧 Тыңдап үйрену"), KeyboardButton(text="📚 Оқып үйрену")]
    ],
    resize_keyboard=True
)

# Сөздік мәзірі (Inline)
dict_inline_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🍎 Жемістер", callback_data="dict_fruits")],
    [InlineKeyboardButton(text="👨‍👩‍👧 Отбасы", callback_data="dict_family")],
    [InlineKeyboardButton(text="🔢 Сандар", callback_data="dict_numbers")]
])

# Сабақтар мәзірі (Inline)
lessons_inline_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1-сабақ: Әліпби (Дауыстылар)", callback_data="lesson_1")],
    [InlineKeyboardButton(text="2-сабақ: Әліпби (Дауыссыздар)", callback_data="lesson_2")],
    [InlineKeyboardButton(text="3-сабақ: Сәлемдесу", callback_data="lesson_3")]
])

# 3. ХАНДЛЕРЛЕР (ФУНКЦИЯЛАР)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"안녕, {message.from_user.first_name}! 🇰🇷\n@Hangupkz_bot-қа қош келдіңіз!", 
        reply_markup=main_menu
    )

# --- СӨЗДІКТЕР БӨЛІМІ ---
@dp.message(F.text == "📖 Сөздіктер")
async def dictionary_menu(message: types.Message):
    await message.answer("Қай тақырып бойынша сөздікті көргіңіз келеді?", reply_markup=dict_inline_menu)

@dp.callback_query(F.data.startswith("dict_"))
async def process_dict(callback: types.CallbackQuery):
    if callback.data == "dict_fruits":
        text = "🍎 **Жемістер:**\n\n사과 (сагуа) - Алма\n배 (пэ) - Алмұрт\n포도 (пходо) - Жүзім"
    elif callback.data == "dict_family":
        text = "👨‍👩‍👧 **Отбасы:**\n\n아버지 (абоджи) - Әке\n어머니 (омони) - Ана\n동생 (тонсэн) - Қарындас/Іні"
    elif callback.data == "dict_numbers":
        text = "🔢 **Сандар (Корейлік):**\n\n하나 (хана) - 1\n둘 (туль) - 2\n셋 (сет) - 3"
    
    await callback.message.edit_text(text, reply_markup=dict_inline_menu)
    await callback.answer()

# --- САБАҚТАР БӨЛІМІ ---
@dp.message(F.text == "📅 Күндік сабақтар")
async def show_lessons(message: types.Message):
    await message.answer("Қай сабақты оқығыңыз келеді?", reply_markup=lessons_inline_menu)

@dp.callback_query(F.data.startswith("lesson_"))
async def process_lessons(callback: types.CallbackQuery):
    if callback.data == "lesson_1":
        text = (
            "🇰🇷 **1-сабақ: Негізгі дауысты дыбыстар**\n\n"
            "Корей тілінде 10 негізгі дауысты дыбыс бар. Бүгін бесеуін үйренеміз:\n\n"
            "ㅏ — [а]\nㅓ — [о] (ашық)\nㅗ — [о] (тұйық)\nㅜ — [у]\nㅡ — [ы]"
        )
    elif callback.data == "lesson_2":
        text = "🇰🇷 **2-сабақ: Дауыссыз дыбыстар**\n\nБұл сабақ дайындалуда... ⏳"
    elif callback.data == "lesson_3":
        text = "🇰🇷 **3-сабақ: Сәлемдесу**\n\n안녕하세요! - Сәлеметсіз бе!"
    
    await callback.message.edit_text(text, reply_markup=lessons_inline_menu)
    await callback.answer()

# --- БАСҚА БӨЛІМДЕР ---
@dp.message(F.text == "🎧 Тыңдап үйрену")
async def listening(message: types.Message):
    await message.answer("🎧 Тыңдалым сабақтары жақында қосылады!")

@dp.message(F.text == "📚 Оқып үйрену")
async def reading(message: types.Message):
    await message.answer("📚 **Оқылым:**\n저는 студент 입니다. (Мен студентпін)")

# 4. БОТТЫ ІСКЕ ҚОСУ
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())