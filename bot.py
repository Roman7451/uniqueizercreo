import os
import uuid
import telebot
import random
from random import randint
import zipfile
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO

# Вставьте ниже токен бота
bot = telebot.TeleBot("<6488073582:AAFD6MbpEMaJgRL1Zj1dBCxSKpSIa8AGEH4>")


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🖼 Уникализировать картинку")
    bot.send_message(message.chat.id, "👋 Добро пожаловать в бот для уникализации картинок от команды Усатого Арбитражника!\n\n"
                                      "🚀 В будущем мы будем дорабатывать этот проект и добавлять много полезных функций!\n\n"
                                      "⚠️ Прежде чем начать подпишись на YouTube канал автора - https://www.youtube.com/@usaffiliate\n\n"
                                      "📣 Также, подпишись на Telegram канал автора - @mustage_affiliate\n\n"
                                      "💬 А если у тебя нет друзей, тебе грустно и одиноко или же у тебя у тебя есть вопросы на которые тебе нужны ответы, то мы будем рады видеть тебя в нашем telegram чате - https://t.me/+eMzWlE9neiY2ZjEy\n\n"
                                      "⬇️ Чтобы уникализировать изображение просто нажми на кнопку ниже.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "🖼 Уникализировать картинку")
def unique_image(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "📝 Введите количество уникальных копий изображения (максимум 10):")
    bot.register_next_step_handler(message, lambda message: get_num_copies(message, chat_id))


def get_num_copies(message, chat_id):
    try:
        num_copies = int(message.text)
        if num_copies > 10 or num_copies <= 0:
            bot.send_message(chat_id, "📝 Можно сделать максимум 10 копий. Введите число <= 10:")
            bot.register_next_step_handler(message, lambda message: get_num_copies(message, chat_id))
        else:
            bot.send_message(chat_id, "📲 Пришлите в чат изображение (со сжатием, т.е. не файлом, т.е. \"Быстрым способом\") которое должно быть уникализировано:")
            bot.register_next_step_handler(message, lambda message: uniqueize_image(message, num_copies))
    except Exception as e:
        bot.send_message(chat_id, "🚫 Произошла ошибка: {}".format(e))
        return send_main_menu(chat_id)


def uniqueize_image(message, num_copies):
    try:
        chat_id = message.chat.id
        # Check if the file size is larger than 5 MB
        if message.photo[-1].file_size > 5 * 1024 * 1024:
            bot.send_message(chat_id,
                             "К сожалению, размер файла изображения не может быть больше 5 МБ. Пожалуйста, повторите попытку с меньшим изображением.")
            return send_main_menu(chat_id)
        file_id = message.photo[-1].file_id
        file = bot.get_file(file_id)
        downloaded_file = bot.download_file(file.file_path)

        # Convert downloaded file to a PIL image
        image = Image.open(BytesIO(downloaded_file))

        # Apply median filter to the image
        image = image.filter(ImageFilter.MedianFilter(size=1))

        # Add noise to the image
        pixels = image.load()
        width, height = image.size
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]
                pixels[i, j] = (r + randint(-10, 10), g + randint(-10, 10), b + randint(-10, 10))

        images = []
        # Create a copy of the image
        temp_image = image.copy()

        # Remove EXIF data (if present)
        exif_data = temp_image.getexif()
        if exif_data:
            temp_image.info.pop("exif")

        # Randomly adjust brightness, contrast, sharpness, and saturation
        brightness = random.uniform(-0.025, 0.025)
        contrast = random.uniform(-0.025, 0.025)
        sharpness = random.uniform(-0.025, 0.025)
        saturation = random.uniform(-0.025, 0.025)
        temp_image = ImageEnhance.Brightness(temp_image).enhance(1 + brightness)
        temp_image = ImageEnhance.Contrast(temp_image).enhance(1 + contrast)
        temp_image = ImageEnhance.Sharpness(temp_image).enhance(1 + sharpness)
        temp_image = ImageEnhance.Color(temp_image).enhance(1 + saturation)

        # Randomly resize the image
        scale = random.uniform(0.95, 1.05)
        new_width = int(temp_image.width * scale)
        new_height = int(temp_image.height * scale)
        temp_image = temp_image.resize((new_width, new_height), resample=Image.BICUBIC)

        # Save the modified image as a PNG file
        temp_filename = f"{uuid.uuid4()}.png"
        temp_image.save(temp_filename, format="PNG")
        images.append(temp_filename)

        # Create the remaining copies of the image
        for i in range(1, num_copies):
            temp_image = image.copy()
            if exif_data:
                temp_image.info.pop("exif")
            brightness = random.uniform(-0.025, 0.025)
            contrast = random.uniform(-0.025, 0.025)
            sharpness = random.uniform(-0.025, 0.025)
            saturation = random.uniform(-0.025, 0.025)
            temp_image = ImageEnhance.Brightness(temp_image).enhance(1 + brightness)
            temp_image = ImageEnhance.Contrast(temp_image).enhance(1 + contrast)
            temp_image = ImageEnhance.Sharpness(temp_image).enhance(1 + sharpness)
            temp_image = ImageEnhance.Color(temp_image).enhance(1 + saturation)
            scale = random.uniform(0.95, 1.05)
            new_width = int(temp_image.width * scale)
            new_height = int(temp_image.height * scale)
            temp_image = temp_image.resize((new_width, new_height), resample=Image.BICUBIC)
            temp_filename = f"{uuid.uuid4()}.png"
            temp_image.save(temp_filename, format="PNG")
            images.append(temp_filename)

        # Create a zip file and add the images to it
        zip_filename = f"{uuid.uuid4()}.zip"
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename in images:
                zip_file.write(filename)

        # Send the zip file to the user
        with open(zip_filename, "rb") as zip_file:
            bot.send_document(chat_id, zip_file)
            bot.send_message(chat_id,
                             "Нужны нормальные креосы? @mustage_portfolio - сдлаем все в лучшем виде!\n\n"
                             "Нужны нормальные аккаунты для facebook? Пиши @usaffiliate")

        # Delete the temporary files
        for filename in images:
            os.remove(filename)
        os.remove(zip_filename)
    except Exception as e:
        bot.send_message(chat_id, "🚫 Произошла ошибка: {}".format(e))
        return send_main_menu(chat_id)


def send_main_menu(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🖼 Уникализировать картинку")
    bot.send_message(chat_id, "Чем я еще могу помочь? Посмотри на кнопки ниже и тыкай туда, куда нужно 😄", reply_markup=markup)


bot.polling()
