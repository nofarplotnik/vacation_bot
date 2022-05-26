import psycopg2
import psycopg2.extras
import http.client

DB_HOST = "ec2-34-247-172-149.eu-west-1.compute.amazonaws.com"
DB_NAME = "dfc2tovhpfhq7h"
DB_USER = "wtmczgcnaqpgeg"
DB_PASS = "385932472b51f4f13f9a373e8b41309f4432b409039fa5246fbc7ed5485c945e"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, bot
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

MONTHDEF, CONTINENTDEF, VACTYPEDEF, VACDATADEF, HOTEL, HOTELDETAILS = range(6)

def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['מעולה', 'גרוע']]
    update.message.reply_text(  'שים לב להתחלה מחדש לחץ /start '
                                '\n'
                                'לסיום לחץ /cancel ' ''
                                ' \n')
    update.message.reply_text(
        'היי אני בוט חופשות, נעים מאוד להכיר ! \n'
        'אני כאן בכדי לעזור למצוא את החופשה המתאימה ביותר. מה שלומך היום ? '
        '  ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='מעולה או גרוע?'
        ),
    )

    return MONTHDEF

def monthdef(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if update.message.text == "מעולה":
        update.message.reply_text(
            'תענוג לשמוע, יאללה ממשיכים!',
        )
    elif update.message.text == "גרוע":
        update.message.reply_text(
            'מצטער לשמוע, החופשה שאתאים בטוח תשפר את מצב הרוח!',
        )
    reply_keyboard = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']]
    update.message.reply_text(
         "באיזה חודש החופשה המתוכננת? (ספרות בלבד)",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='הכנס חודש כמספר'
        ),
    )

    return CONTINENTDEF

def continentdef(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global monthpy, monthCheckInOut
    monthpy=update.message.text
    if monthpy == '1':
        monthpy = 'ינואר'
        monthCheckInOut = "01"
    if monthpy == '2':
        monthpy = 'פברואר'
        monthCheckInOut = "02"
    if monthpy == '3':
        monthpy = 'מרץ'
        monthCheckInOut = "03"
    if monthpy == '4':
        monthpy = 'אפריל'
        monthCheckInOut = "04"
    if monthpy == '5':
        monthpy = 'מאי'
        monthCheckInOut = "05"
    if monthpy == '6':
        monthpy = 'יוני'
        monthCheckInOut = "06"
    if monthpy == '7':
        monthpy = 'יולי'
        monthCheckInOut = "07"
    if monthpy == '8':
        monthpy = 'אוגוסט'
        monthCheckInOut = "08"
    if monthpy == '9':
        monthpy = 'ספטמבר'
        monthCheckInOut = "09"
    if monthpy == '10':
        monthpy = 'אוקטובר'
        monthCheckInOut = "10"
    if monthpy == '11':
        monthpy = 'נובמבר'
        monthCheckInOut = "11"
    if monthpy == '12':
        monthpy = 'דצמבר'
        monthCheckInOut = "12"
    reply_keyboard = [['אירופה', 'אסיה', 'אפריקה', 'אמריקה', 'אוסטרליה']]
    update.message.reply_text(
                'באיזו יבשת תרצה לנפוש?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='הכנס יבשת'
        ),
    )

    return VACTYPEDEF

def vactypedef(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global continentpy
    continentpy = update.message.text
    if ((continentpy=='אוסטרליה' and monthpy=='ינואר') or (continentpy=='אמריקה' and monthpy=='ינואר') or (continentpy=='אוסטרליה' and monthpy=='פברואר') or  (continentpy=='אמריקה' and monthpy=='פברואר')
       or    (continentpy=='אמריקה' and monthpy=='מרץ' )  or  (continentpy=='אוסטרליה' and monthpy=='אפריל' )  or    (continentpy=='אמריקה' and monthpy=='אפריל' )  or    (continentpy=='אסיה' and monthpy=='אפריל' )  or    (continentpy=='אמריקה' and monthpy=='מאי' )
            or    (continentpy=='אוסטרליה' and monthpy=='אוגוסט' )  or    (continentpy=='אמריקה' and monthpy=='אוגוסט' )   or    (continentpy=='אמריקה' and monthpy=='ספטמבר' )
            or (continentpy == 'אוסטרליה' and monthpy == 'אוקטובר')   or    (continentpy=='אמריקה' and monthpy=='אוקטובר' )   or    (continentpy=='אוסטרליה' and monthpy=='נובמבר' )   or    (continentpy=='אמריקה' and monthpy=='נובמבר' )
            or (continentpy == 'אוסטרליה' and monthpy == 'דצמבר')   or    (continentpy=='אמריקה' and monthpy=='דצמבר' ) or    (continentpy=='אסיה' and monthpy=='פברואר' ) or (continentpy == 'אסיה' and monthpy == 'אוגוסט')):
        reply_keyboard = [['בטן-גב', 'עירוני']]

    if  ((continentpy=='אירופה' and monthpy=='מרץ')):
         reply_keyboard = [[ 'עירוני', 'סקי']]

    elif   (continentpy=='אסיה' and monthpy=='יולי' )   or    (continentpy=='אסיה' and monthpy=='יוני' ) :
        reply_keyboard = [['בטן-גב', 'סקי']]

    elif ((continentpy == 'אפריקה' and monthpy == 'מרץ') or  (continentpy=='אפריקה' and monthpy=='ינואר')  or (continentpy == 'אפריקה' and monthpy == 'פברואר')   or    (continentpy=='אפריקה' and monthpy=='אפריל' )  or    (continentpy=='אפריקה' and monthpy=='מאי' ) or (continentpy == 'אמריקה' and monthpy == 'יוני')  or    (continentpy=='אוסטרליה' and monthpy=='יולי')  or (continentpy=='אפריקה' and monthpy=='יולי' )   or    (continentpy=='אפריקה' and monthpy=='אוגוסט' )   or    (continentpy=='אוסטרליה' and monthpy=='ספטמבר' ) or (continentpy == 'אפריקה' and monthpy == 'ספטמבר')   or    (continentpy=='אפריקה' and monthpy=='אוקטובר' )   or    (continentpy=='אפריקה' and monthpy=='נובמבר' ) or (continentpy == 'אפריקה' and monthpy == 'דצמבר')
          or    (continentpy=='אוסטרליה' and monthpy=='יוני' )   or    (continentpy=='אפריקה' and monthpy=='יוני' )):
        reply_keyboard = [['בטן-גב']]

    elif ((continentpy=='אוסטרליה' and monthpy=='מרץ')  or    (continentpy=='אוסטרליה' and monthpy=='מאי' )) :
        reply_keyboard = [['עירוני']]

    elif ((continentpy=='אמריקה' and monthpy=='יולי')) :
        update.message.reply_text("לצערי לא מצאתי חופשות לנתונים שבחרת, אנא נסה לשנות את נתוני החופשה /tryAgain")

    else:
        reply_keyboard = [['בטן-גב', 'עירוני', 'סקי']]

    update.message.reply_text(
        'על איזה סוג חופשה חלמת?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='הכנס סגנון חופשה'
        ),
    )

    return VACDATADEF

def vacdatadef(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global vaction_type_py
    vaction_type_py = update.message.text
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            t=continentpy
            v=monthpy
            g=vaction_type_py
            cur.execute("SELECT cityHE FROM City \
            INNER JOIN Country1 \
            ON Country1.countryName = City.countryName \
            INNER JOIN Vacation \
            ON Vacation.city = cityName \
            INNER JOIN continent_he \
            ON continent_he.continentname = Country1.continentname \
            INNER JOIN vacmonth_he \
            ON vacmonth_he.vacmonth = Vacation.vacmonth \
            INNER JOIN vacationtype_he \
            ON vacationtype_he.vactype = Vacation.vactype  WHERE continenthe ='%s' AND vacmonthhe ='%s' AND vacation_type_he ='%s' " % (continentpy,monthpy ,vaction_type_py),conn)
            global my_results
            my_results = cur.fetchall()
    if len(my_results)==0:
        update.message.reply_text("לצערי לא מצאתי חופשות לנתונים שבחרת, אנא נסה לשנות את נתוני החופשה /tryAgain")
    else:
        a=""
        j=0
        for i in my_results:
            if j==0:
                a=a+str(i[0])
            else:
                a=a+ ", " + str(i[0])
            j=j+1
        conn.commit()
        if len(my_results)==1:
            update.message.reply_text("נמצא היעד החלומי עבורך: \n" + a  )
        else:
            update.message.reply_text("מצאתי מספר יעדים חלומיים לחופשה בשבילך: \n" + a  )
        user = update.message.from_user
        reply_keyboard = [['אשמח', 'בפעם אחרת']]
        update.message.reply_text(
         'שאתאים לך מלון?',
         reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='אשמח או בפעם אחרת?'
        ),
        )

        return HOTEL

hotelCity = "1"

def hotel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if update.message.text == "אשמח":
        if len(my_results) == 1:
            hotelCity = my_results[0][0]
            update.message.reply_text(
                'באיזו עיר מהרשימה שהוצעה לבצע את החיפוש?',
                reply_markup=ReplyKeyboardRemove(),
            )

        else:
            update.message.reply_text(
                'באיזו עיר מהרשימה שהוצעה לבצע את החיפוש?',
                reply_markup=ReplyKeyboardRemove(),
            )

        return HOTELDETAILS
    elif update.message.text == "בפעם אחרת":
        update.message.reply_text(
            'אנחנו מחכים לך ;)',
            reply_markup=ReplyKeyboardRemove(),
        )

    return ConversationHandler.END

def hoteldetails(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    b = ""
    if hotelCity == "1":
        for i in my_results:
            if i[0]==update.message.text:
               b = i[0]
        if len(b)==0:
            update.message.reply_text(
                'משהו השתבש, הכנס את שם העיר כפי שמופיע מעלה',
            )

            return HOTELDETAILS
    else:
       b = hotelCity
    update.message.reply_text(
        'תהליך זה יקח מספר רגעים :) כ- 2 דקות',
        reply_markup=ReplyKeyboardRemove(),
    )
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT cityname FROM City WHERE cityhe ='%s'" % (b),conn)
            conn.commit()
            cityEnglish = cur.fetchall()
    conn = http.client.HTTPSConnection("hotel-price-aggregator.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Host': 'hotel-price-aggregator.p.rapidapi.com',
        'X-RapidAPI-Key': 'd49cb50581msh39ca9981d2c0ba7p1f1b53jsn4ae5bab71ed3'
  }

    cityGlobal = cityEnglish[0][0]
    a = cityGlobal
    if " " in cityGlobal:
        cityGlobal = cityGlobal.replace(" ", "%20")
    searchCity = "/search?q=" + cityGlobal + '"'
    conn.request("GET", searchCity, headers=headers)
    res = conn.getresponse()
    data = res.read()
    hotelInCity = data.decode("utf-8")
    hotelInCityArray = hotelInCity.split('name')
    relevantHotels = ""
    strr = 'city":"' + a
    for i in hotelInCityArray:
        if i == 0:
            i = 1
        if strr in i:
            relevantHotels = relevantHotels + " #" + i
    if len(relevantHotels)==0:
        update.message.reply_text(
            'לצערי לא מצאתי מידע לגבי מלונות ביעד ובחודש שנבחרו',
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    #  relevantHotelsSplit = relevantHotels.split('hotelId":"')
    relevantHotelsSplit = relevantHotels.split('#')
    finalHotels = {}
    id = ""
    nameHotel = ""
    k = 1
    i=0
    s=0
    for p in range(1,len(relevantHotelsSplit)):
        s=0
        namesplit=relevantHotelsSplit[p].split('"shortName":"')
        idsplit = relevantHotelsSplit[p].split('hotelId":"')
        while namesplit[1][s] != '"':
            nameHotel = nameHotel + namesplit[1][s]
            s = s + 1
        s=0
        while idsplit[1][s] != '"':
            id = id + idsplit[1][s]
            s = s + 1

        if id != "" and nameHotel != "":
            finalHotels[k] = {'Name': nameHotel, 'id': id}
            id = ""
            nameHotel = ""
            k = k + 1

    conn = http.client.HTTPSConnection("hotel-price-aggregator.p.rapidapi.com")
    for i in range(1, len(finalHotels) + 1):
        currentHotel = finalHotels[i]['id']
        if monthCheckInOut=='07' or monthCheckInOut=='08' or monthCheckInOut=='09' or monthCheckInOut=='10' or monthCheckInOut=='11' or monthCheckInOut=='12':
            payload = "{\r\n    \"hotelId\": \"" + currentHotel + "\",\r\n    \"checkIn\": \"2022-" + monthCheckInOut + "-01\",\r\n    \"checkOut\": \"2022-" + monthCheckInOut + "-02\"\r\n}"
        else:
            payload = "{\r\n    \"hotelId\": \"" + currentHotel + "\",\r\n    \"checkIn\": \"2023-" + monthCheckInOut + "-01\",\r\n    \"checkOut\": \"2023-" + monthCheckInOut + "-02\"\r\n}"

        headers = {
            'content-type': "application/json",
            'X-RapidAPI-Host': "hotel-price-aggregator.p.rapidapi.com",
            'X-RapidAPI-Key': 'd49cb50581msh39ca9981d2c0ba7p1f1b53jsn4ae5bab71ed3'
        }
        conn.request("POST", "/rates", payload, headers)
        res = conn.getresponse()
        data = res.read()
        if data.decode("utf-8").find('"rate"') == -1:
            finalHotels[i]['provider'] = 'None'
        else:
            providerHotelsSplit = data.decode("utf-8").split('provider":"')
            nameProvider = ""
            j = 0
            while providerHotelsSplit[1][j] != '"':
                nameProvider = nameProvider + providerHotelsSplit[1][j]
                j = j + 1
            finalHotels[i]['provider'] = nameProvider
            rateHotelsSplit = providerHotelsSplit[1].split('rate":"')
            rate = ""
            j = 0
            while rateHotelsSplit[1][j] != '"':
                rate = rate + rateHotelsSplit[1][j]
                j = j + 1
            rate = int(rate)
            taxHotelsSplit = rateHotelsSplit[1].split('"taxes":"')
            tax = ""
            j = 0
            while taxHotelsSplit[1][j] != '"':
                tax = tax + taxHotelsSplit[1][j]
                j = j + 1
            tax = int(tax)
            finalHotels[i]['price'] = rate + tax
    resFinalHotels=""
    countFinalHotels=0
    enterFor=1
    for i in range(1, len(finalHotels)+1):
        if finalHotels[i]['provider'] != 'None':
            countFinalHotels=countFinalHotels+1
    if countFinalHotels==0:
        flag=1
        if len(finalHotels)==2:
            resFinalHotels = resFinalHotels + "מצאתי עבורך מלון ב" + b  + ":" + "\n\n" + \
                             finalHotels[flag]['Name'] + "\n"

        else:
            resFinalHotels = resFinalHotels + "מצאתי עבורך מספר מלונות ב" + b  + ":" + "\n\n"
            while flag!=4 and flag!=len(finalHotels):
                resFinalHotels = resFinalHotels + finalHotels[flag]['Name'] + "\n\n"
                flag=flag+1

    else:
        if countFinalHotels==1:
            for i in range(1, len(finalHotels)+1):
                if finalHotels[i]['provider'] != 'None':
                    resFinalHotels = resFinalHotels + "מצאתי עבורך מלון ב" + b + " בחודש " + monthpy + ":" + "\n\n" + finalHotels[i]['Name'] + "\n" + str(finalHotels[i]['price']) + " דולר מחיר משוער ללילה כולל מיסים" + "\n" + "באתר " + finalHotels[i]['provider']
        else:
            flag=0
            for i in range(1, len(finalHotels)+1):
                if finalHotels[i]['provider'] != 'None':
                    flag=flag+1
                    if flag==4:
                        break
                    if enterFor==1:
                        resFinalHotels = resFinalHotels + "מצאתי עבורך מספר מלונות ב" + b + " בחודש " + monthpy + ":" + "\n\n"
                        resFinalHotels = resFinalHotels + finalHotels[i]['Name'] + "\n" + str(finalHotels[i]['price']) + " דולר מחיר משוער ללילה כולל מיסים" + "\n" + "באתר " + finalHotels[i]['provider'] + "\n\n"
                    else:
                        resFinalHotels = resFinalHotels + finalHotels[i]['Name'] + "\n" + str(finalHotels[i]['price']) + " דולר מחיר משוער ללילה כולל מיסים" + "\n" + "באתר " + finalHotels[i]['provider'] + "\n\n"
                    enterFor=0
    update.message.reply_text(
            resFinalHotels,
            reply_markup=ReplyKeyboardRemove(),
    )
    update.message.reply_text(
        'חופשה מהנה להתראות!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    update.message.reply_text(
        'חופשה מהנה להתראות!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    updater = Updater("5173317208:AAF-orwKwLcml3lTSqMow9jL_cKH5pyJ3G4")
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MONTHDEF: [MessageHandler(Filters.regex('^(מעולה|גרוע)$'), monthdef)],
            CONTINENTDEF: [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8|9|10|11|12)$'), continentdef)],
            VACTYPEDEF: [MessageHandler(Filters.regex('^(אירופה|אסיה|אפריקה|אמריקה|אוסטרליה)$'), vactypedef), CommandHandler('tryAgain', monthdef)],
            VACDATADEF: [MessageHandler(Filters.regex('^(סקי|עירוני|בטן-גב)$'), vacdatadef),CommandHandler('tryAgain', monthdef)],
            HOTEL: [MessageHandler(Filters.regex('^(בפעם אחרת|אשמח)$'), hotel)],
            HOTELDETAILS: [MessageHandler(Filters.text & ~Filters.command, hoteldetails)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
