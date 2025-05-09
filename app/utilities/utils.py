# utils.py
from app.controllers.scheduled_controller import (
    get_scheduled_campaigns,
    delete_scheduled_campaign,
)
import schedule
import json
from datetime import datetime
import random


programming_hour = "15:08"


def change_hour(hour):
    global programming_hour
    programming_hour = hour
    schedule.clear()
    program_daily_jobs(hour)
    print(f"Tareas programadas para la hora {programming_hour}")


def run_jobs(register: dict):
    try:
        result = create_page(
            register["campaign_id"],
            register["services_name"],
            register["city"],
            register["title_seo"],
            register["meta_description"],
            register["state"],
            register["key_phrase"],
            register["total_reviews"],
            register["blocks"],
            register["url"],
        )

        if result["status"] == "ok":
            delete_scheduled_campaign(register["id"])
        else:
            print(result)
            print(f"Error al ejecutar la tarea programada: {result['message']}")
    except Exception as e:
        print(f"Error al ejecutar la tarea programada: {str(e)}")


def date_validation(register: dict):
    actual_date = datetime.now().strftime("%Y-%m-%d")
    return register["date"] == actual_date


def obtain_registers():
    try:
        scheduled = get_scheduled_campaigns()
        scheduled_list = json.loads(scheduled)
        print(f"Registros obtenidos: {len(scheduled_list)}")
        return scheduled_list
    except Exception as e:
        print(f"Error al obtener los registros: {str(e)}")
        return []


def run_scheduled_jobs():
    registers = obtain_registers()
    today_registers = [register for register in registers if date_validation(register)]
    print(f"Registros programados para hoy: {len(today_registers)}")
    for register in today_registers:
        run_jobs(register)


def program_daily_jobs(hour):
    print("Tareas Programadas")
    schedule.every().day.at(hour).do(run_scheduled_jobs)


def choose_random_link(links) -> str:
    link_data = random.choice(links)
    keyword = random.choice(link_data["keywords"])
    return f"{link_data['url']}?keyword={keyword.replace(' ', '+')}"
