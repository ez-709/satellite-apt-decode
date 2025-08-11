import asyncio
import numpy as np
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
import matplotlib
matplotlib.use('Agg')  # Устанавливаем backend без GUI
import matplotlib.pyplot as plt
import os

# === ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЯ ===
def generate_parabola_image(filename="parabola.png"):
    """Генерирует изображение параболы"""
    x = np.linspace(-10, 10, 400)
    y = x**2
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', linewidth=2, label='y = x²')
    plt.grid(True, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('График параболы y = x²')
    plt.legend()
    
    plt.savefig(filename, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    return filename

# Создаем изображение
PARABOLA_IMAGE_PATH = generate_parabola_image()

# === КЛАВИАТУРЫ ===
def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1) Редактировать текст", callback_data="edit_text")],
        [InlineKeyboardButton(text="2) Редактировать текст и фото", callback_data="edit_text_photo")],
        [InlineKeyboardButton(text="3) Редактировать фото", callback_data="edit_photo")],
        [InlineKeyboardButton(text="4) Убрать фото", callback_data="remove_photo")]
    ])

def get_back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад", callback_data="back_to_main")]
    ])

# === ХЕНДЛЕРЫ ===
router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Главное меню:", reply_markup=get_main_menu())

@router.callback_query(F.data == "edit_text")
async def edit_text(callback: CallbackQuery):
    # Если в сообщении есть фото, нужно заменить его на текст
    if callback.message.photo:
        await callback.message.delete()
        new_message = await callback.message.answer(
            "📝 Отредактированный текст без фото",
            reply_markup=get_back_menu()
        )
    else:
        await callback.message.edit_text(
            "📝 Отредактированный текст без фото",
            reply_markup=get_back_menu()
        )
    await callback.answer()

@router.callback_query(F.data == "edit_text_photo")
async def edit_text_photo(callback: CallbackQuery):
    photo = FSInputFile(PARABOLA_IMAGE_PATH)
    
    if callback.message.photo:
        # Если уже есть фото, редактируем медиа
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption="📊 Текст с фото параболы"
            ),
            reply_markup=get_back_menu()
        )
    else:
        # Если нет фото, удаляем старое сообщение и отправляем новое с фото
        await callback.message.delete()
        new_message = await callback.message.answer_photo(
            photo=photo,
            caption="📊 Текст с фото параболы",
            reply_markup=get_back_menu()
        )
    
    await callback.answer()

@router.callback_query(F.data == "edit_photo")
async def edit_photo(callback: CallbackQuery):
    photo = FSInputFile(PARABOLA_IMAGE_PATH)
    
    if callback.message.photo:
        # Если уже есть фото, редактируем медиа
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption="Только фото параболы"
            ),
            reply_markup=get_back_menu()
        )
    else:
        # Если нет фото, удаляем старое сообщение и отправляем новое с фото
        await callback.message.delete()
        new_message = await callback.message.answer_photo(
            photo=photo,
            caption="Только фото параболы",
            reply_markup=get_back_menu()
        )
    
    await callback.answer()

@router.callback_query(F.data == "remove_photo")
async def remove_photo(callback: CallbackQuery):
    # Проверяем, есть ли фото в текущем сообщении
    if callback.message.photo:
        await callback.message.delete()
        new_message = await callback.message.answer(
            "❌ Фото убрано. Теперь только текст.",
            reply_markup=get_back_menu()
        )
    else:
        await callback.message.edit_text(
            "ℹ️ В этом сообщении нет фото для удаления.",
            reply_markup=get_back_menu()
        )
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    # Удаляем текущее сообщение и отправляем новое с главным меню
    await callback.message.delete()
    new_message = await callback.message.answer(
        "Главное меню:",
        reply_markup=get_main_menu()
    )
    await callback.answer()

# === ЗАПУСК БОТА ===
async def main():
    # Замените 'YOUR_BOT_TOKEN' на токен вашего бота
    bot = Bot(token="8463357588:AAGbFiS3AklYo-gPIlHCpcAAVZYZALpkFwY")
    dp = Dispatcher()
    
    dp.include_router(router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())