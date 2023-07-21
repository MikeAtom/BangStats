## Сканер та менеджер статистики BanG Dream! Girls Band Party.

Інструмент для сканування та аналізу знімків екрану результатів лайвів у грі. Функціонал, який був би корисний у базовій грі, але наразі як є.

![image](https://cdn.discordapp.com/attachments/882697945772855337/1132066295270080623/image.png)

## Особливості
- [x] Сканування знімків екрану та екстракція результатів
- [x] Можливість вручну виправити помилки, якщо вони виникнуть під час сканування
- [x] Перегляд вашої загальної та по пісенної статистики
- [x] Підтримка локалізації

## Installation
1. Завантажте останню версію зі [сторінки релізів](https://github.com/MikeAtom/BangStats/releases)
2. Розпакуйте архів у папку на ваш вибір
3. Встановіть залежності, виконавши команду `pip install -r requirements.txt` у папці, де ви розпакували архів
4. Запустіть програму, виконавши `main.pyw` у папці, де ви розпакували архів

Примітка: Якщо ви плануєте використовувати прискорення за допомогою GPU, вам потрібно мати відеокарту від NVIDIA та встановити pytorch із підтримкою CUDA. Детальніше [тут](https://pytorch.org/get-started/locally/).

## Використання
По-перше, програма не може отримати дані з нікуди. Вам потрібно надати їй знімки екрану з результатами лайвів з гри. Чим більше знімків ви надаєте, тим точніша буде статистика.

1. Помістіть усі знімки у одну папку на ваш вибір.
2. Відкрийте програму та вкажіть папку із знімками.
3. Створіть новий профіль та дайте йому назву.
4. Натисніть кнопку "Сканувати".
5. Дотримуйтесь інструкцій на екрані. Майте на увазі, що процес сканування може зайняти деякий час, залежно від кількості наданих знімків.
6. Після завершення процесу сканування вам потрібно буде вручну виправити будь-які помилки, які можуть виникнути під час процесу сканування. Натисніть кнопку "Пост-обробка" на головному екрані, щоб це зробити.
7. Знову дотримуйтесь інструкцій на екрані.
8. Як усі помилки будуть виправленні, ви можете переглянути свою статистику, натиснувши кнопку "Профіль" на головному екрані :3

## Відомі проблеми та обмеження
- Тестовано лише на Windows, не можу гарантувати, що працюватиме на інших платформах
- Також тестовано лише на знімках на Android, не можу гарантувати, що працюватиме на iOS
- Програма створена з огляду на Endori, тому вона може не працювати належним чином зі знімками з інших серверів

## Власні локалізації
Програма підтримує власні локалізації. Щоб створити одну, вам потрібно створити новий файл у папці `data/lang` та назвати його згідно з мовою, на яку ви хочете перекласти програму. Наприклад, якщо ви хочете перекласти програму на німецьку, вам потрібно створити файл з назвою `de.json`. Файл повинен бути у форматі JSON. Використовуйте надані локалізації як приклад.

## Зворотній зв'язок
Якщо у вас є які-небудь питання, пропозиції або звіти про помилки, не соромтеся зв'язатися зі мною [де завгодно](https://linktr.ee/MikeAtom)