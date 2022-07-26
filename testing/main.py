from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import time

cluster = MongoClient("mongodb+srv://zhar:zhar@cluster0.e99t7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)

# Connect to the database
db = cluster["foodbuzz"]

# Connect to the collection
users = db["users"]
orders = db["orders"]
items = db["items"]

# Create the application
app = Flask(__name__)

# Create the routes
@app.route("/", methods=["get", "post"])
def reply():
    # Get the message from the request
    text = request.form.get("message")
    
    # Get the user's contact from the request
    number = request.form.get("sender")

    # Response to the user
    res = {"reply": ""}

    # Check if the user is saved in the database
    user = users.find_one({"number": number})

    # Ayam Geprek Original
    original = items.find_one({"_id" : ObjectId("62ad3dd590bac48b85930fcb")})
    name_original = original["item_name"]
    link_original = original["photo"]
    jumlah_original = original["quantity"]
    harga_original = original["harga"]

    # Paket Gold
    gold = items.find_one({"_id" : ObjectId("62ad3e2a90bac48b85930fcc")})
    name_gold= gold["item_name"]
    link_gold= gold["photo"]
    jumlah_gold = gold["quantity"]
    harga_gold = gold["harga"]

    # Paket Silver
    silver = items.find_one({"_id" : ObjectId("62ad3e5590bac48b85930fcd")})
    name_silver= silver["item_name"]
    link_silver= silver["photo"]
    jumlah_silver = silver["quantity"]
    harga_silver = silver["harga"]

    # Paket Bronze
    bronze = items.find_one({"_id" : ObjectId("62ad3e9790bac48b85930fce")})
    name_bronze= bronze["item_name"]
    link_bronze= bronze["photo"]
    jumlah_bronze = bronze["quantity"]
    harga_bronze = bronze["harga"]

    # Teh Manis
    teh_manis = items.find_one({"_id" : ObjectId("62ad40a890bac48b85930fd3")})
    name_teh_manis = teh_manis["item_name"]
    link_teh_manis = teh_manis["photo"]
    jumlah_teh_manis = teh_manis["quantity"]
    harga_teh_manis = teh_manis["harga"]

    # Teh Tarik
    teh_tarik = items.find_one({"_id" : ObjectId("62ad40cd90bac48b85930fd4")})
    name_teh_tarik = teh_tarik["item_name"]
    link_teh_tarik = teh_tarik["photo"]
    jumlah_teh_tarik = teh_tarik["quantity"]
    harga_teh_tarik = teh_tarik["harga"]

    # Thai Tea
    thai_tea = items.find_one({"_id" : ObjectId("62ad40ef90bac48b85930fd5")})
    name_thai_tea = thai_tea["item_name"]
    link_thai_tea = thai_tea["photo"]
    jumlah_thai_tea = thai_tea["quantity"]
    harga_thai_tea = thai_tea["harga"]

    # If the user is not saved in the database
    # FORM INPUT KALAU USERS PERTAMA KALI CHAT SAMA BOT
    if bool(user) == False:
        # Ask the user to register first
        res["reply"] += '\n\n' + ("Intro\n\nSebelum melanjutkan isikan data Anda berikut ini. \n\nNama: \nNomor WhatsApp: \nAlamat: ")
        res["reply"] += '\n\n' + ("*Catatan:*\nFormat yang Anda digunakan pastikan sesuai.\n\n*Contoh:*\nNama: Asep Mulyana\nNomor WhatsApp: 081123456789\nAlamat: Jl. Raya Bogor KM.5, Bogor")

        # Save the user's contact in the database        
        users.insert_one({"number": number, "status": "before_main", "cart" : []})

    # WELCOMING MESSAGE
    elif user["status"] == "before_main":
        # Check first if the user's new
        if "Nama: " in text and "Nomor WhatsApp: " in text and "Alamat: " in text:
            # Get the user's name, address, and No.WhatsApp from the request
            name = text[text.index('Nama: ') + len('Nama: '):text.index('\nNomor WhatsApp: ')]
            noWhatsApp = text[text.index('Nomor WhatsApp: ') + len('Nomor WhatsApp: '):text.index('\nAlamat: ')]
            address = text[text.index('Alamat: ') + len('Alamat: '):]

            # Welcome the user
            res["reply"] += '\n' + ("Intro\n\nHalo, terima kasih telah menghubungi Ayam Geprek FoodBuzz.id\nSelanjutnya, Anda dapat memilih salah satu menu di bawah ini:"
                        "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan menu* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                        "Untuk mendapatkan *alamat penjual*")
            res["reply"] += '\n\n' + ("Jika respon yang diberikan lambat, silahkan kirim pesan yang sama sebanyak 2 atau 3 kali\n"
                        "Hal ini mungkin terjadi karena koneksi buruk atau server yang sedang lambat")

            # Update the user's data in the database
            users.update_one({"number": number}, {"$set": {"status": "main", "name": name, "noWhatsApp": noWhatsApp, "address": address, "cart": []}})
        else:
            res["reply"] += '\n' + ("Intro\n\nHarap menggunakan format yang sesuai.\n\n*Contoh:*\nNama: Asep Mulyana\nNomor WhatsApp: 081123456789\nAlamat: Jl. Raya Bogor KM.5, Bogor")

    # RESPON PILIHAN DARI WELCOMING MESSAGE
    elif user["status"] == "main":
        try:
            # Get the user's choice from the request
            option = int(text)
        except:
            # If the user's choice is not an integer
            res["reply"] += '\n' + ("Intro\n\nHarap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan menu* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
            return str(res)

        # Process for every user's choice
        if option == 1: # Pemesanan Produk
            res["reply"] += '\n' + (
                f"Intro / Menu\n\nAnda dapat memilih pilihan menu yang tersedia:\n\n1️⃣ *Ayam Geprek Original* \n Tanpa Nasi \n Harga: {formatrupiah(harga_original)}\n\n"
                f"2️⃣ *Paket Gold* \n Tersedia: Sambal Korek, Cikur, dan Daun Jeruk \n Harga: {formatrupiah(harga_gold)} \n\n"
                f"3️⃣ *Paket Silver* \n Tersedia: Sambal terasi, buto ijo, dan daun matah \n Harga: {formatrupiah(harga_silver)} \n\n"
                f"4️⃣ *Paket Bronze* \n Tersedia: Sambal teri dan saus keju \n Harga: {formatrupiah(harga_bronze)} \n\n"
                "5️⃣ *Minuman* \n Tersedia: Teh manis, Teh tarik, dan Thai tea \n\n 0️⃣ *Kembali*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
        elif option == 2: # Kontak Penjual
            res["reply"] += '\n' + (
                "Intro / Kontak Penjual\n\nAnda bisa menghubungi kami melalui.\nemail: foodbuzz@gmail.com\nno telp: +6281542346842 (Admin)") 
        elif option == 3: # Jam Kerja
            res["reply"] += '\n' + ("Intro / Jam Kerja\n\nKami siap melayani anda setiap hari hari pada pukul 07.00 - 21.00 WIB")
        elif option == 4: # Alamat Penjual
            res["reply"] += '\n' + (
                "Intro / Alamat\n\nJl. Ciwaruga No.50, Ciwaruga, Kec. Parongpong, Kabupaten Bandung Barat, Jawa Barat 40559")
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Intro\n\nHarap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan menu* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")

    # UDAH MILIH PAKET, MINUMAN, ATAU KEMBALI TERUS DIKEMANAIN
    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            # If the user's choice is not an integer
            res["reply"] += '\n' + ("Intro\n\nHarap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan menu* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
            return str(res)

        # KALAU MILIH KEMBALI
        if option == 0: # Kembali
            res["reply"] += '\n' + ("Intro\n\nHalo, terima kasih telah menghubungi Ayam Geprek FoodBuzz.id\nSelanjutnya, Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan menu* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
            res["reply"] += '\n\n' + ("Jika respon yang diberikan lambat, silahkan kirim pesan yang sama sebanyak 2 atau 3 kali\n"
                    "Hal ini mungkin terjadi karena koneksi buruk atau server yang sedang lambat")

            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})

        # KALAU MILIH ORIGINAL
        elif option == 1: # Original

            # Connecting to Form_original
            users.update_one(
                {"number": number}, {"$set": {"status": "form_original"}})
        
        # KALAU MILIH GOLD
        elif option == 2: #Gold
            # Response message
            res["reply"] += '\n' + ("Intro / Menu / Paket Gold\n\nPaket Gold tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                      f"1️⃣ *Sambal Korek - stok: {jumlah_gold['Sambal_Korek']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"2️⃣ *Sambal Cikur - stok: {jumlah_gold['Sambal_Cikur']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"3️⃣ *Daun Jeruk - stok: {jumlah_gold['Daun_Jeruk']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"0️⃣ *Kembali*")

            # Connection to Form_gold
            users.update_one(
                {"number": number}, {"$set": {"status": "form_gold"}})
        
        # KALAU MILIH SILVER
        elif option == 3: #Silver
            # Response message
            res["reply"] += '\n' + ("Intro / Menu / Paket Silver\n\nPaket Silver tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                        f"1️⃣ *Sambal Terasi - stok: {jumlah_silver['Sambal_Terasi']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                        f"2️⃣ *Sambal Buto Ijo - stok: {jumlah_silver['Sambal_Buto_Ijo']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                        f"3️⃣ *Daun Matah - stok: {jumlah_silver['Daun_Matah']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                        f"0️⃣ *Kembali*")
            
            # Connection to Form_silver
            users.update_one(
                {"number": number}, {"$set": {"status": "form_silver"}})
        
        # KALAU MILIH BRONZE
        elif option == 4: #Bronze
            # Response message
            res["reply"] += '\n' + ("Intro / Menu / Paket Bronze\n\nPaket Bronze tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                        f"1️⃣ *Sambal Teri - stok: {jumlah_bronze['Sambal_Teri']}* \n Harga: {formatrupiah(harga_bronze)} \n\n"
                                        f"2️⃣ *Sambal Saus Keju - stok: {jumlah_bronze['Sambal_Saus_Keju']}* \n Harga: {formatrupiah(harga_bronze)} \n\n"
                                        f"0️⃣ *Kembali*")

            # Connection to Form_bronze
            users.update_one(
                {"number": number}, {"$set": {"status": "form_bronze"}})
            
        # KALAU MILIH MINUMAN
        elif option == 5: #Minuman
            # Response message
            res["reply"] += '\n' + ("Intro / Menu / Paket Minuman\n\nPaket Minuman tersedia dengan berbagai macam minuman")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu minuman yang teresedia di bawah ini: \n\nKetik\n\n"
                                        f"1️⃣ *{name_teh_manis} - stok: {jumlah_teh_manis}* \n Harga: {formatrupiah(harga_teh_manis)} \n\n"
                                        f"2️⃣ *{name_teh_tarik} - stok: {jumlah_teh_tarik}* \n Harga: {formatrupiah(harga_teh_tarik)} \n\n"
                                        f"3️⃣ *{name_thai_tea} - stok: {jumlah_thai_tea}* \n Harga: {formatrupiah(harga_thai_tea)} \n\n"
                                        f"0️⃣ *Kembali*")

            # Connection to Form_minuman
            users.update_one(
                {"number": number}, {"$set": {"status": "form_minuman"}})

        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Intro / Menu\n\nHarap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + (
                f"Anda dapat memilih pilihan menu yang tersedia:\n\n1️⃣ *Ayam Geprek Original* \n Tanpa Nasi \n Harga: {harga_original}\n\n"
                f"2️⃣ *Paket Gold* \n Tersedia: Sambal Korek, Cikur, dan Daun Jeruk \n Harga: {harga_gold} \n\n"
                f"3️⃣ *Paket Silver* \n Tersedia: Sambal terasi, buto ijo, dan daun matah \n Harga: {harga_silver} \n\n"
                f"4️⃣ *Paket Bronze* \n Tersedia: Sambal teri dan saus keju \n Harga: {harga_bronze} \n\n"
                "5️⃣ *Minuman* \n Tersedia: Teh manis, Teh tarik, dan Thai tea \n\n 0️⃣ *Kembali*")

    elif user["status"] == "form_gold":
        try:
            option = int(text)
        except:
            # If the user's choice is not an integer
            # Response message
            res["reply"] += '\n' + ("Intro / Menu / Paket Gold\n\nPaket Gold tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                      f"1️⃣ *Sambal Korek - stok: {jumlah_gold['Sambal_Korek']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"2️⃣ *Sambal Cikur - stok: {jumlah_gold['Sambal_Cikur']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"3️⃣ *Daun Jeruk - stok: {jumlah_gold['Daun_Jeruk']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"0️⃣ *Kembali*")
            return str(res)

        # KALAU MILIH KEMBALI
        if option == 0: 
            res["reply"] += '\n' + (
                f"Intro / Menu\n\nAnda dapat memilih pilihan menu yang tersedia:\n\n1️⃣ *Ayam Geprek Original* \n Tanpa Nasi \n Harga: {harga_original}\n\n"
                f"2️⃣ *Paket Gold* \n Tersedia: Sambal Korek, Cikur, dan Daun Jeruk \n Harga: {harga_gold} \n\n"
                f"3️⃣ *Paket Silver* \n Tersedia: Sambal terasi, buto ijo, dan daun matah \n Harga: {harga_silver} \n\n"
                f"4️⃣ *Paket Bronze* \n Tersedia: Sambal teri dan saus keju \n Harga: {harga_bronze} \n\n"
                "5️⃣ *Minuman* \n Tersedia: Teh manis, Teh tarik, dan Thai tea \n\n 0️⃣ *Kembali*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
            
        # KALAU MILIH SAMBAL KOREK, CIKUR, DAN DAUN JERUK
        elif option == 1 or option == 2 or option == 3:
            # Form the order
            res["reply"] += '\n\n' + ("Intro / Menu / Paket Gold / Pemesanan\n\n*Form Detail Pemesanan* \n Jumlah: ")
            res["reply"] += '\n\n' + ("*Catatan:*\n- Jumlah yang dipesan tidak melebihi stok yang tersedia\n- Format yang Anda digunakan pastikan sesuai.\n\nContoh:\nJumlah: 3 \n")
            
            users.update_one(
                {"number": number}, {"$set": {"status": "pesen_lagi_gak"}})

            # NAMA MENU YANG DIPILIH
            gold = ["Sambal_Korek", "Sambal_Cikur", "Daun_Jeruk"]
            selected = gold[option - 1]
            users.update_one({"number": number}, {"$set": {"item": selected}})

        # MILIH DI LUAR SAMBAL KOREK, CIKUR, DAN DAUN JERUK
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Intro / Menu / Paket Gold\n\nHarap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Paket Gold tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                      f"1️⃣ *Sambal Korek - stok: {jumlah_gold['Sambal_Korek']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"2️⃣ *Sambal Cikur - stok: {jumlah_gold['Sambal_Cikur']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"3️⃣ *Daun Jeruk - stok: {jumlah_gold['Daun_Jeruk']}* \n Harga: {formatrupiah(harga_gold)} \n\n"
                                      f"0️⃣ *Kembali*")

    elif user["status"] == "form_silver":
        try:
            option = int(text)
        except:
            # If the user's choice is not an integer
            # Response message
            res["reply"] += '\n' + ("Intro / Menu / Paket Silver\n\nPaket Silver tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                      f"1️⃣ *Sambal Terasi - stok: {jumlah_silver['Sambal_Terasi']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                      f"2️⃣ *Sambal Buto Ijo - stok: {jumlah_silver['Sambal_Buto_Ijo']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                      f"3️⃣ *Daun Matah - stok: {jumlah_silver['Daun_Matah']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                      f"0️⃣ *Kembali*")
            return str(res)
        
        # KALAU MILIH KEMBALI
        if option == 0:
            res["reply"] += '\n' + (
                f"Intro / Menu\n\nAnda dapat memilih pilihan menu yang tersedia:\n\n1️⃣ *Ayam Geprek Original* \n Tanpa Nasi \n Harga: {harga_original}\n\n"
                f"2️⃣ *Paket Gold* \n Tersedia: Sambal Korek, Cikur, dan Daun Jeruk \n Harga: {harga_gold} \n\n"
                f"3️⃣ *Paket Silver* \n Tersedia: Sambal terasi, buto ijo, dan daun matah \n Harga: {harga_silver} \n\n"
                f"4️⃣ *Paket Bronze* \n Tersedia: Sambal teri dan saus keju \n Harga: {harga_bronze} \n\n"
                "5️⃣ *Minuman* \n Tersedia: Teh manis, Teh tarik, dan Thai tea \n\n 0️⃣ *Kembali*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
        
        # KALAU MILIH SAMBAL TERASI, BUTO IJO, DAN MATAH
        elif option == 1 or option == 2 or option == 3:
            # Form the order
            res["reply"] += '\n\n' + ("Intro / Menu / Paket Silver / Pemesanan\n\n*Form Detail Pemesanan* \n Jumlah: ")
            res["reply"] += '\n\n' + ("*Catatan:*\n- Jumlah yang dipesan tidak melebihi stok yang tersedia\n- Format yang Anda digunakan pastikan sesuai.\n\nContoh:\nJumlah: 3 \n")
            
            users.update_one(
                {"number": number}, {"$set": {"status": "pesen_lagi_gak"}})
            
            # NAMA MENU YANG DIPILIH
            silver = ["Sambal_Terasi", "Sambal_Buto_Ijo", "Daun_Matah"]
            selected = silver[option - 1]
            users.update_one({"number": number}, {"$set": {"item": selected}})

        # MILIH DI LUAR TUMBLER STAIN, KACA, MOTIF, DAN KUSTOM
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Intro / Menu / Paket Silver\n\nHarap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Paket Silver tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                        f"1️⃣ *Sambal Terasi - stok: {jumlah_silver['Sambal_Terasi']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                        f"2️⃣ *Sambal Buto Ijo - stok: {jumlah_silver['Sambal_Buto_Ijo']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                        f"3️⃣ *Daun Matah - stok: {jumlah_silver['Daun_Matah']}* \n Harga: {formatrupiah(harga_silver)} \n\n"
                                        f"0️⃣ *Kembali*")

    elif user["status"] == "form_bronze":
        try:
            option = int(text)
        except:
            # If the user's choice is not an integer
            # Response message
            res["reply"] += '\n' + ("Intro / Menu / Paket Bronze\n\nPaket Bronze tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                      f"1️⃣ *Sambal Teri - stok: {jumlah_bronze['Sambal_Teri']}* \n Harga: {formatrupiah(harga_bronze)} \n\n"
                                      f"2️⃣ *Sambal Saus Keju - stok: {jumlah_bronze['Sambal_Saus_Keju']}* \n Harga: {formatrupiah(harga_bronze)} \n\n"
                                      f"0️⃣ *Kembali*")
            return str(res)
        
        # KALAU MILIH KEMBALI
        if option == 0:
            res["reply"] += '\n' + (
                f"Intro / Menu\n\nAnda dapat memilih pilihan menu yang tersedia:\n\n1️⃣ *Ayam Geprek Original* \n Tanpa Nasi \n Harga: {harga_original}\n\n"
                f"2️⃣ *Paket Gold* \n Tersedia: Sambal Korek, Cikur, dan Daun Jeruk \n Harga: {harga_gold} \n\n"
                f"3️⃣ *Paket Silver* \n Tersedia: Sambal terasi, buto ijo, dan matah \n Harga: {harga_silver} \n\n"
                f"4️⃣ *Paket Bronze* \n Tersedia: Sambal teri dan saus keju \n Harga: {harga_bronze} \n\n"
                "5️⃣ *Minuman* \n Tersedia: Teh manis, Teh tarik, dan Thai tea \n\n 0️⃣ *Kembali*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})

        # KALAU MILIH SAMBAL TERI DAN SAUS KEJU
        elif option == 1 or option == 2:
            # Form the order
            res["reply"] += '\n\n' + ("Intro / Menu / Paket Bronze / Pemesanan\n\n*Form Detail Pemesanan* \n Jumlah: ")
            res["reply"] += '\n\n' + ("*Catatan:*\n- Jumlah yang dipesan tidak melebihi stok yang tersedia\n- Format yang Anda digunakan pastikan sesuai.\n\nContoh:\nJumlah: 3 \n")
            
            users.update_one(
                {"number": number}, {"$set": {"status": "pesen_lagi_gak"}})
            
            # NAMA MENU YANG DIPILIH
            bronze = ["Sambal_Teri", "Sambal_Saus_Keju"]
            selected = bronze[option - 1]
            users.update_one({"number": number}, {"$set": {"item": selected}})
        
        # MILIH DI LUAR SAMBAL TERI DAN SAUS KEJU
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Intro / Menu / Paket Bronze\n\nHarap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Paket Bronze tersedia dengan berbagai macam sambal")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu menu yang tersedia di bawah ini: \n\nKetik\n\n"
                                        f"1️⃣ *Sambal Teri - stok: {jumlah_bronze['Sambal_Teri']}* \n Harga: {formatrupiah(harga_bronze)} \n\n"
                                        f"2️⃣ *Sambal Saus Keju - stok: {jumlah_bronze['Sambal_Saus_Keju']}* \n Harga: {formatrupiah(harga_bronze)} \n\n"
                                        f"0️⃣ *Kembali*")

    elif user["status"] == "form_minuman":
        try:
            option = int(text)
        except:
            # If the user's choice is not an integer
            # Response message
            res["reply"] += '\n' + ("Intro / Menu / Paket Minuman\n\nPaket Minuman tersedia dengan berbagai macam minuman")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu minuman yang teresedia di bawah ini: \n\nKetik\n\n"
                                        f"1️⃣ *{name_teh_manis} - stok: {jumlah_teh_manis}* \n Harga: {formatrupiah(harga_teh_manis)} \n\n"
                                        f"2️⃣ *{name_teh_tarik} - stok: {jumlah_teh_tarik}* \n Harga: {formatrupiah(harga_teh_tarik)} \n\n"
                                        f"3️⃣ *{name_thai_tea} - stok: {jumlah_thai_tea}* \n Harga: {formatrupiah(harga_thai_tea)} \n\n"
                                        f"0️⃣ *Kembali*")
            return str(res)
        
        # KALAU MILIH KEMBALI
        if option == 0:
            res["reply"] += '\n' + (
                f"Intro / Menu\n\nAnda dapat memilih pilihan menu yang tersedia:\n\n1️⃣ *Ayam Geprek Original* \n Tanpa Nasi \n Harga: {harga_original}\n\n"
                f"2️⃣ *Paket Gold* \n Tersedia: Sambal Korek, Cikur, dan Daun Jeruk \n Harga: {harga_gold} \n\n"
                f"3️⃣ *Paket Silver* \n Tersedia: Sambal terasi, buto ijo, dan daun matah \n Harga: {harga_silver} \n\n"
                f"4️⃣ *Paket Bronze* \n Tersedia: Sambal teri dan saus keju \n Harga: {harga_bronze} \n\n"
                "5️⃣ *Minuman* \n Tersedia: Teh manis, Teh tarik, dan Thai tea \n\n 0️⃣ *Kembali*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
        
        # KALAU MILIH TEH MANIS, TEH TARIK, ATAU THAI TEA
        elif option == 1 or option == 2 or option == 3:
            # Form the order
            res["reply"] += '\n\n' + ("Intro / Menu / Paket Minuman / Pemesanan\n\n*Form Detail Pemesanan* \n Jumlah: ")
            res["reply"] += '\n\n' + ("*Catatan:*\n- Jumlah yang dipesan tidak melebihi stok yang tersedia\n- Format yang Anda digunakan pastikan sesuai.\n\nContoh:\nJumlah: 3 \n")
            
            users.update_one(
                {"number": number}, {"$set": {"status": "pesen_lagi_gak"}})
            
            # NAMA MENU YANG DIPILIH
            teh_manis = ["Teh Manis", "Teh Tarik", "Thai Tea"]
            selected = teh_manis[option - 1]
            users.update_one({"number": number}, {"$set": {"item": selected}})
        
        # MILIH DI LUAR TEH MANIS, TEH TARIK, ATAU THAI TEA
        else:
            # if the input is exclude the available choice
            res["reply"] += '\n' + ("Intro / Menu / Paket Minuman\n\nHarap memasukkan sesuai dengan pilihan yang tersedia\n")
            res["reply"] += '\n' + ("Paket Minuman tersedia dengan berbagai macam minuman")
            res["reply"] += '\n\n' + (f"Anda dapat memilih salah satu minuman yang teresedia di bawah ini: \n\nKetik\n\n"
                                        f"1️⃣ *{name_teh_manis} - stok: {jumlah_teh_manis}* \n Harga: {formatrupiah(harga_teh_manis)} \n\n"
                                        f"2️⃣ *{name_teh_tarik} - stok: {jumlah_teh_tarik}* \n Harga: {formatrupiah(harga_teh_tarik)} \n\n"
                                        f"3️⃣ *{name_thai_tea} - stok: {jumlah_thai_tea}* \n Harga: {formatrupiah(harga_thai_tea)} \n\n"
                                        f"0️⃣ *Kembali*")

    # PEMROSESAN FORM INPUTAN PELANGGAN
    elif user["status"] == "pesen_lagi_gak":
        if "Jumlah: " in text:
            jumlah_pesanan = text[text.index('Jumlah: ') + len('Jumlah: ')]
            
            item_selected = users.find_one({"number": number})["item"]

            # MASUKIN CART
            users.update_one({"number": number}, {"$push": {"cart": {"item_name": item_selected, "jumlah": jumlah_pesanan}}})

            # NGECEK NONE ATAU TIDAK
            cart_updated = users.find_one({"cart": {"$elemMatch": {"item_name": item_selected, "jumlah": jumlah_pesanan}}})
        
        # PESEN LAGI NGGAK
        cart = cart_updated["cart"]
        print(cart)

        item_selected = users.find_one({"number": number})["item"]
        
        n = 1
        res["reply"] += '\n' + ("Intro / Menu / Pilih Paket / Pemesanan / Keranjang\n\nPilihan menarik! 😉")
        res["reply"] += '\n\n' + ("Pesanan  Anda: ")

        # MENGHITUNG KESELURUHAN HARGA PESANAN
        total_harga = 0

        # MENGHITUNG JUMLAH PESANAN YANG DIPESAN
        jumlah_pesanan_pushed = 0
        
        for item in cart:
            total_harga_per_item = 0
            # Paket Gold
            if item["item_name"] == "Sambal_Korek" or item["item_name"] == "Sambal_Cikur" or item["item_name"] == "Daun_Jeruk":
                # GET JUMLAH PESANAN
                jumlah_pesanan = int(item["jumlah"])
                jumlah_pesanan_pushed += jumlah_pesanan

                # MENJUMLAHKAN HARGA PESANAN (Harga sambal korek, sambal cikur, dan daun jeruk sama)
                total_harga += jumlah_pesanan * harga_gold
                total_harga_per_item += jumlah_pesanan * harga_gold
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['jumlah']} - {formatrupiah(total_harga_per_item)}*")

                # PENGURANGAN STOK BERDASARKAN JENIS SAMBAL
                if item["item_name"] == "Sambal_Korek":
                    items.update_one({"item_name": "Paket Gold"}, {"$inc": {"quantity.Sambal_Korek": -jumlah_pesanan}})
                elif item["item_name"] == "Sambal_Cikur":
                    items.update_one({"item_name": "Paket Gold"}, {"$inc": {"quantity.Sambal_Cikur": -jumlah_pesanan}})
                elif item["item_name"] == "Daun_Jeruk":
                    items.update_one({"item_name": "Paket Gold"}, {"$inc": {"quantity.Daun_Jeruk": -jumlah_pesanan}})
                
                # MASUKIN KE ORDERS ITEMS
                orders.update_one({"number": number}, {"$push": {"items": {"item_name": item_selected, "detail_data": {"jumlah": item["jumlah"], "harga": total_harga_per_item}}}})
            
            # Paket Silver
            elif item["item_name"] == "Sambal_Terasi" or item["item_name"] == "Sambal_Buto_Ijo" or item["item_name"] == "Daun_Matah":
                # GET JUMLAH PESANAN
                jumlah_pesanan = int(item["jumlah"])
                jumlah_pesanan_pushed += jumlah_pesanan

                # MENJUMLAHKAN HARGA PESANAN (Harga sambal terasi, sambal buto ijo, dan daun matah sama)
                total_harga += jumlah_pesanan * harga_silver
                total_harga_per_item += jumlah_pesanan * harga_silver
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['jumlah']} - {formatrupiah(total_harga_per_item)}*")

                # PENGURANGAN STOK BERDASARKAN JENIS SAMBAL
                if item["item_name"] == "Sambal_Terasi":
                    items.update_one({"item_name": "Paket Silver"}, {"$inc": {"quantity.Sambal_Terasi": -jumlah_pesanan}})
                elif item["item_name"] == "Sambal_Buto_Ijo":
                    items.update_one({"item_name": "Paket Silver"}, {"$inc": {"quantity.Sambal_Buto_Ijo": -jumlah_pesanan}})
                elif item["item_name"] == "Daun_Matah":
                    items.update_one({"item_name": "Paket Silver"}, {"$inc": {"quantity.Daun_Matah": -jumlah_pesanan}})
                
                # MASUKIN KE ORDERS ITEMS
                orders.update_one({"number": number}, {"$push": {"items": {"item_name": item_selected, "detail_data": {"jumlah": item["jumlah"], "harga": total_harga_per_item}}}})

            # Paket Bronze
            elif item["item_name"] == "Sambal_Teri" or item["item_name"] == "Sambal_Saus_Keju":
                # GET JUMLAH PESANAN
                jumlah_pesanan = int(item["jumlah"])
                jumlah_pesanan_pushed += jumlah_pesanan

                # MENJUMLAHKAN HARGA PESANAN (Harga sambal teri, sambal saus keju sama)
                total_harga += jumlah_pesanan * harga_bronze
                total_harga_per_item += jumlah_pesanan * harga_bronze
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['jumlah']} - {formatrupiah(total_harga_per_item)}*")

                # PENGURANGAN STOK BERDASARKAN JENIS SAMBAL
                if item["item_name"] == "Sambal_Teri":
                    items.update_one({"item_name": "Paket Bronze"}, {"$inc": {"quantity.Sambal_Teri": -jumlah_pesanan}})
                elif item["item_name"] == "Sambal_Saus_Keju":
                    items.update_one({"item_name": "Paket Bronze"}, {"$inc": {"quantity.Sambal_Saus_Keju": -jumlah_pesanan}})
                
                # MASUKIN KE ORDERS ITEMS
                orders.update_one({"number": number}, {"$push": {"items": {"item_name": item_selected, "detail_data": {"jumlah": item["jumlah"], "harga": total_harga_per_item}}}})
            
            # Teh Manis
            elif item["item_name"] == "Teh Manis":
                # GET JUMLAH PESANAN
                jumlah_pesanan = int(item["jumlah"])
                jumlah_pesanan_pushed += jumlah_pesanan

                # MENJUMLAHKAN HARGA
                total_harga += jumlah_pesanan * harga_teh_manis
                total_harga_per_item += jumlah_pesanan * harga_teh_manis
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['jumlah']} - {formatrupiah(total_harga_per_item)}*")

                # PENGURANGAN STOK BERDASARKAN JENIS TEH MANIS
                items.update_one({"item_name": "Teh Manis"}, {"$inc": {"quantity": -jumlah_pesanan}})

                # MASUKIN KE ORDERS ITEMS
                orders.update_one({"number": number}, {"$push": {"items": {"item_name": item_selected, "detail_data": {"jumlah": item["jumlah"], "harga": total_harga_per_item}}}})

            # Teh Tarik
            elif item["item_name"] == "Teh Tarik":
                # GET JUMLAH PESANAN
                jumlah_pesanan = int(item["jumlah"])
                jumlah_pesanan_pushed += jumlah_pesanan

                # MENJUMLAHKAN HARGA
                total_harga += jumlah_pesanan * harga_teh_tarik
                total_harga_per_item += jumlah_pesanan * harga_teh_tarik
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['jumlah']} - {formatrupiah(total_harga_per_item)}*")

                # PENGURANGAN STOK BERDASARKAN JENIS TEH TARIK
                items.update_one({"item_name": "Teh Tarik"}, {"$inc": {"quantity": -jumlah_pesanan}})

                # MASUKIN KE ORDERS ITEMS
                orders.update_one({"number": number}, {"$push": {"items": {"item_name": item_selected, "detail_data": {"jumlah": item["jumlah"], "harga": total_harga_per_item}}}})

            # Thai Tea
            elif item["item_name"] == "Thai Tea":
                # GET JUMLAH PESANAN
                jumlah_pesanan = int(item["jumlah"])
                jumlah_pesanan_pushed += jumlah_pesanan

                # MENJUMLAHKAN HARGA
                total_harga += jumlah_pesanan * harga_thai_tea
                total_harga_per_item += jumlah_pesanan * harga_thai_tea
                res["reply"] += '\n' + (f"*{n}. {item['item_name']} - {item['jumlah']} - {formatrupiah(total_harga_per_item)}*")

                # PENGURANGAN STOK BERDASARKAN JENIS THAI TEA
                items.update_one({"item_name": "Thai Tea"}, {"$inc": {"quantity": -jumlah_pesanan}})

                # MASUKIN KE ORDERS ITEMS
                orders.update_one({"number": number}, {"$push": {"items": {"item_name": item_selected, "detail_data": {"jumlah": item["jumlah"], "harga": total_harga_per_item}}}})

            n += 1
        
        res["reply"] += '\n\n' + (f"Harga total : *{formatrupiah(total_harga)}*")

        # CHECK IS THERE REPORT FIELD  ORDERS COLLECTION
        # if orders.find_one({"report": { "$exists": True }}):
            # INCREMENT REPORT FIELD
            # orders.update_one({"number": number}, {"$inc": {"report": {"total_profit": total_harga, "total_sell": jumlah_pesanan_pushed, "average_profit": total_harga / jumlah_pesanan_pushed}}})
        # else:
            # CREATE REPORT FIELD
        orders.update_one({"number": number}, {"$set": {"report": {"total_profit": total_harga, "total_sell": jumlah_pesanan_pushed, "average_profit": total_harga / jumlah_pesanan_pushed}}})

        res["reply"] += '\n\n' + ("Apakah anda ingin memesan yang lain?\n")
        res["reply"] += '\n' + ("1️⃣ Ya, saya ingin memesan lagi menu lainnya \n2️⃣ Tidak, sudah cukup")      

        users.update_one(
                {"number": number}, {"$set": {"status": "pending"}})

    elif user["status"] == "pending":
        try:
            option = int(text)
        except:
            res["reply"] += '\n\n' + ("Apakah anda ingin memesan yang lain?")
            res["reply"] += '\n' + ("1️⃣ Ya, saya ingin memesan lagi menu lainnya \n2️⃣ Tidak, sudah cukup")   
            return str(res)
        
        if option == 1:
            res["reply"] += '\n' + (
                f"Intro / Menu\n\nAnda dapat memilih pilihan menu yang tersedia:\n\n1️⃣ *Ayam Geprek Original* \n Tanpa Nasi \n Harga: {harga_original}\n\n"
                f"2️⃣ *Paket Gold* \n Tersedia: Sambal Korek, Cikur, dan Daun Jeruk \n Harga: {harga_gold} \n\n"
                f"3️⃣ *Paket Silver* \n Tersedia: Sambal terasi, buto ijo, dan daun matah \n Harga: {harga_silver} \n\n"
                f"4️⃣ *Paket Bronze* \n Tersedia: Sambal teri dan saus keju \n Harga: {harga_bronze} \n\n"
                "5️⃣ *Minuman* \n Tersedia: Teh manis, Teh tarik, dan Thai tea \n\n 0️⃣ *Kembali*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
        elif option == 2:
            users.update_one(
                {"number": number}, {"$set": {"status": "form_bayar"}})

            res["reply"] += '\n\n' + ("Intro / Menu / Pilih Paket / Pemesanan / Keranjang / Form Data\n\n*Form Detail Pengiriman* \nAlamat Penerima: \nNama Penerima: \nTelp. Penerima:")
            res["reply"] += '\n\n' + ("*Catatan:*\nFormat yang Anda digunakan pastikan sesuai.\n\nContoh:\nAlamat Penerima: Jln. Mars no.15, Kecamatan Padasuka\nNama Penerima: Asep Mulyana\nTelp. Penerima: 0851-4235-2321\n")

    elif user["status"] == "form_bayar":
        if "Alamat Penerima: " in text and "Nama Penerima: " in text and "Telp. Penerima: " in text:
            alamat_penerima = text[text.index('Alamat Penerima: ') + len('Alamat Penerima: '):text.index('\nNama Penerima: ')]
            nama_penerima = text[text.index('Nama Penerima: ') + len('Nama Penerima: '):text.index('\nTelp. Penerima: ')]
            telp_penerima = text[text.index('Telp. Penerima: ') + len('Telp. Penerima: '):]

        # MASUKIN WAKTU PAID
        orders.update_one({"number": number}, {"$set": {"paid_timestamp": datetime.now()}})

        # MASUKIN KE ORDERS RECEIVER IDENTITY
        orders.update_one({"number": number}, {"$set": {"recevier_identity": {"name": nama_penerima, "telp": telp_penerima, "address": alamat_penerima}}})

        res["reply"] += "\n" +  "Intro / Menu / Pilih Paket / Pemesanan / Keranjang / Form Data / Checkout\n\nTerima kasih telah berbelanja Ayam Geprek FoodBuzz! 😊"
        res["reply"] += "\n" +  "Pesanan dapat dibayarkan melalui transfer bank ke rekening berikut:\n"
        res["reply"] += "\n" +  "*Bank Mandiri:*"
        res["reply"] += "\n" +  "No. Rekening: 0987654321"
        res["reply"] += "\n" +  "a.n. PT FoodBuzz.id\n"

        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})
        users.update_one({"number": number}, {"$unset": {"item": ""}})

    elif user["status"] == "ordered":
        # Welcome the user
        res["reply"] += '\n' + ("Intro / \n\nHalo, terima kasih telah menghubungi Ayam Geprek FoodBuzz.id\nSelanjutnya, Anda dapat memilih salah satu menu di bawah ini:"
                    "\n\n*Ketik*\n\n 1️⃣ Untuk *memesan menu* \n 2️⃣ Untuk mengetahui *kontak penjual*\n 3️⃣ Untuk melihat *jam kerja* \n 4️⃣ "
                    "Untuk mendapatkan *alamat penjual*")
        res["reply"] += '\n\n' + ("Jika respon yang diberikan lambat, silahkan kirim pesan yang sama sebanyak 2 atau 3 kali\n"
                "Hal ini mungkin terjadi karena koneksi buruk atau server yang sedang lambat")

        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})
    return str(res)

# Ref : http://pemrograman-sederhana.blogspot.com/2014/09/membuat-format-rupiah-di-bahasa_33.html 
def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3 :
        return 'Rp' + y     
    else :
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + '.' + p

if __name__ == "__main__":
    app.run(port=5000)