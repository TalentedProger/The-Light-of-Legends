from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from proverbs_service import get_random_image_id, get_image_path, get_text_for_image
from app import keyboards  as kb

router = Router()

@router.message(F.text == "Пословицы 📝")
async def send_random_proverb(message: Message):
    img_id = get_random_image_id()
    img_path = get_image_path(img_id)
    caption = "Адыгская пословица"
    await message.answer_photo(
        photo=FSInputFile(img_path),
        caption=caption,
        reply_markup=kb.get_proverbs_keyboard(img_id)
    )

@router.callback_query(F.data == "next_proverb")
async def next_proverb(callback: CallbackQuery):
    current_img_id = callback.message.reply_markup.inline_keyboard[1][0].callback_data.split(":")[1]
    new_img_id = get_random_image_id(exclude=current_img_id)
    img_path = get_image_path(new_img_id)
    caption = "Адыгская пословица"
    await callback.message.edit_media(
        media={"type": "photo", "media": FSInputFile(img_path), "caption": caption},
        reply_markup=kb.get_proverbs_keyboard(new_img_id)
    )
    await callback.answer("Следующая пословица")

@router.callback_query(F.data.startswith("copy_proverb:"))
async def copy_proverb_text(callback: CallbackQuery):
    img_id = callback.data.split(":")[1]
    text = get_text_for_image(img_id)
    await callback.message.edit_caption(caption=text, reply_markup=kb.get_proverbs_keyboard(img_id))
    await callback.answer("Текст скопирован")

@router.callback_query(F.data == "exit_proverb_mode")
async def exit_proverb(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("Режим пословиц закрыт")
