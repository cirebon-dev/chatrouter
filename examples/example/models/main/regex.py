# -*-coding:utf8;-*-
from models.main import chatbot
import pytz
from datetime import datetime
from typing import Any


@chatbot.add_command(
    "jam\??$|tampilkan jam!?$|jam berapa\??$|jam berapa sekarang\??$|sekarang jam\??$|sekarang jam berapa\??$",
    regex=True,
)
def tampil_jam() -> str:
    tz = pytz.timezone("Asia/Jakarta")
    dt = datetime.now(tz)
    return dt.strftime(
        "Sekarang jam %H lebih %M menit dan %S detik (waktu Indonesia barat)"
    )


@chatbot.add_command(
    "tanggal\??$|tampilkan tanggal!?$|tanggal berapa\??$|tanggal berapa sekarang\??$|sekarang tanggal\??$|sekarang tanggal berapa\??$",
    regex=True,
)
def tampil_tanggal() -> str:
    tz = pytz.timezone("Asia/Jakarta")
    dt = datetime.now(tz)
    return dt.strftime("Sekarang tanggal %d, bulan %m dan tahun %Y.")


@chatbot.add_command(
    "hari\??$|hari ini\??$|tampilkan hari!?$|hari apa\??$|hari apa sekarang\??$|sekarang hari apa\??$",
    regex=True,
)
def tampil_hari(*args: Any) -> str:
    tz = pytz.timezone("Asia/Jakarta")
    dt = datetime.now(tz)
    day = dt.weekday()
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    return f"Hari ini hari {hari[day]}."
