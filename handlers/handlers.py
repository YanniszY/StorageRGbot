from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import kb
from states.state import User
from database.db import insert_file, execute_query

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет, выбери опцию из меню!", reply_markup=kb.main)

@router.callback_query(F.data == "add")
async def add_func(callback_query: CallbackQuery):
    await callback_query.message.answer("Я поддерживаю документы, видео, фото, кружки, голосовые. Отправь мне файл")

@router.message(F.document)
async def get_id_doc(message: Message):
    document_id = message.document.file_id
    await message.answer(f"Ваш документ ID: {document_id}")
    insert_file(document_id, "document")

@router.message(F.photo)
async def get_id_photo(message: Message):
    photo_id = message.photo[-1].file_id
    await message.answer(f"Ваше фото ID: {photo_id}")
    insert_file(photo_id, "photo")

@router.message(F.audio)
async def get_id_audio(message: Message):
    audio_id = message.audio.file_id
    await message.answer(f"Ваше аудио ID: {audio_id}")
    insert_file(audio_id, "audio")

@router.message(F.voice)
async def get_id_voice(message: Message):
    voice_id = message.voice.file_id
    await message.answer(f"Ваш ID голосового сообщения: {voice_id}")
    insert_file(voice_id, "voice")

@router.message(F.video_note)
async def get_id_video_note(message: Message):
    video_note_id = message.video_note.file_id
    await message.answer(f"ID вашего кружка: {video_note_id}")
    insert_file(video_note_id, "video_note")

@router.callback_query(F.data == 'get')
async def ask_for_file_id(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите ID файла:")
    await state.set_state(User.user_file_id)

@router.message(User.user_file_id)
async def get_user_file(message: Message, state: FSMContext):
    user_file_id = message.text
    file_type = execute_query("SELECT file_type FROM file_id WHERE text = ?", (user_file_id,))

    if file_type:
        file_type = file_type[0][0]
        if file_type == "photo":
            await message.answer_photo(user_file_id)
        elif file_type == "video":
            await message.answer_video(user_file_id)
        elif file_type == "document":
            await message.answer_document(user_file_id)
        elif file_type == "audio":
            await message.answer_audio(user_file_id)
        elif file_type == "voice":
            await message.answer_voice(user_file_id)
        elif file_type == "video_note":
            await message.answer_video_note(user_file_id)
        else:
            await message.answer("Неизвестный тип файла.")
    else:
        await message.answer("Файл с таким ID не найден.")

    await state.clear()

@router.callback_query(F.data == 'list')
async def list_files(callback_query: CallbackQuery):
    files = execute_query("SELECT text, file_type FROM file_id")

    if not files:
        await callback_query.message.answer("Нет файлов для отправки.")
        return

    for file_id, file_type in files:
        try:
            if file_type == 'photo':
                await callback_query.message.answer_photo(photo=file_id)
            elif file_type == 'document':
                await callback_query.message.answer_document(document=file_id)
            elif file_type == 'audio':
                await callback_query.message.answer_audio(audio=file_id)
            elif file_type == 'video':
                await callback_query.message.answer_video(video=file_id)
        except TelegramAPIError as e:
            await callback_query.message.answer(f"Ошибка при отправке файла: {e}")

    await callback_query.answer()
