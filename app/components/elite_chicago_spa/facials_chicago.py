from fastapi import HTTPException

from app.api import GPT
from app.config import local_session
from app.controllers import (
    get_domain,
    load_json_file,
    save_json_file,
)

from app.utilities.utils import choose_random_link

json_file = "app/components/elite_chicago_spa/facials_chicago.json"
links = [
    {
        "url": "https://www.elitechicagospa.com/facials-chicago/",
        "keywords": [
            "facial chicago​", "facials chicago​", "best facial chicago", "chicago facials", 
            "best facial in chicago​", "facial spa chicago il", "best facials chicago", 
            "best facials in chicago", "chicago facial spa", "facials in chicago", 
            "facial in chicago​", "mens facial chicago", "facial chicago near me", 
            "spa facial chicago", "facial chicago il", "facial spas chicago"
        ]
    }
]

url = choose_random_link(links)

class FacialsChicago:
    def __init__(self, options):
        self.options = options
        self.gpt = GPT(self.options)
        self.session = local_session()
        self.local_json = load_json_file(json_file)


    def block_introduction(self):
        try:
            content = self.local_json["content"][1]["elements"][0]["elements"][2]

            content_text = self.gpt.spa_services_introduction_desc(
                content["settings"]["editor"]
            )

            content["settings"]["editor"] = content_text


            save_json_file(json_file, self.local_json, "Introduction Block")

        except Exception as e:
            print("Error en Introduction Block:", str(e))

    def cta1_block(self):
        try:
                title = self.local_json["content"][1]["elements"][0]["elements"][3]
                content = self.local_json["content"][1]["elements"][0]["elements"][4]

                title_text = self.gpt.spa_services_cta_title(title["settings"]["title"])
                content_text = self.gpt.spa_services_facials_cta1_desc(content["settings"]["editor"])

                title["settings"]["title"] = title_text
                content["settings"]["editor"] = content_text

                save_json_file(json_file, self.local_json, "CTA1 Block")

        except Exception as e:
            print("Error en CTA1 Block:", str(e))

    def cta2_block(self):
        try:
                title = self.local_json["content"][3]["elements"][0]
                content = self.local_json["content"][3]["elements"][1]

                title_text = self.gpt.spa_services_cta_title(title["settings"]["title"])
                content_text = self.gpt.spa_services_facials_cta1_desc(content["settings"]["editor"])

                title["settings"]["title"] = title_text
                content["settings"]["editor"] = content_text

                save_json_file(json_file, self.local_json, "CTA2 Block")

        except Exception as e:
            print("Error en CTA2 Block:", str(e))

    def cta3_block(self):
        try:
                title = self.local_json["content"][4]["elements"][0]["elements"][0]
                content = self.local_json["content"][4]["elements"][0]["elements"][1]

                title_text = self.gpt.spa_services_cta_title(title["settings"]["title"])
                content_text = self.gpt.spa_services_facials_cta3_desc(content["settings"]["editor"])

                title["settings"]["title"] = title_text
                content["settings"]["editor"] = content_text


                save_json_file(json_file, self.local_json, "CTA3 Block")

        except Exception as e:
            print("Error en CTA3 Block:", str(e))

    def cta4_block(self):
        try:
                title = self.local_json["content"][5]["elements"][0]["elements"][1]
                content = self.local_json["content"][5]["elements"][0]["elements"][2]

                title_text = self.gpt.spa_services_cta_title(title["settings"]["title"])
                content_text = self.gpt.spa_services_facials_cta4_desc(content["settings"]["editor"])

                title["settings"]["title"] = title_text
                content["settings"]["editor"] = content_text

                save_json_file(json_file, self.local_json, "CTA4 Block")

        except Exception as e:
            print("Error en CTA4 Block:", str(e))
    
    def cta5_block(self):
        try:
                title = self.local_json["content"][6]["elements"][0]["elements"][0]
                subtitle = self.local_json["content"][6]["elements"][0]["elements"][1]
                
                title_text = self.gpt.spa_services_cta_title(title["settings"]["title"])
                subtitle_text = self.gpt.spa_services_cta_title(title["settings"]["title"])

                title["settings"]["title"] = title_text
                subtitle["settings"]["title"] = subtitle_text
                

                save_json_file(json_file, self.local_json, "CTA5 Block")

        except Exception as e:
            print("Error en CTA5 Block:", str(e))

    def cta6_block(self):
        try:
                title = self.local_json["content"][7]["elements"][0]["elements"][0]
                content = self.local_json["content"][7]["elements"][0]["elements"][1]
                title_text = self.gpt.spa_services_cta_title(title["settings"]["title"])
                content_text = self.gpt.spa_services_facials_cta6_desc(content["settings"]["editor"])

                title["settings"]["title"] = title_text
                content["settings"]["editor"] = content_text

                save_json_file(json_file, self.local_json, "CTA6 Block")

        except Exception as e:
            print("Error en CTA6 Block:", str(e))

    def cta7_block(self):
        try:
                title = self.local_json["content"][9]["elements"][0]
                content = self.local_json["content"][9]["elements"][1]
                title_text = self.gpt.spa_services_cta_title(title["settings"]["title"])
                content_text = self.gpt.spa_services_cta_desc(content["settings"]["editor"])

                title["settings"]["title"] = title_text
                content["settings"]["editor"] = content_text

                save_json_file(json_file, self.local_json, "CTA7 Block")

        except Exception as e:
            print("Error en CTA7 Block:", str(e))

    def faq_block(self):
        try:
            faq_element = self.local_json["content"][11]["elements"][0]["elements"][1]

            faq_text = self.gpt.faq_services()
            print(faq_text)

            if isinstance(faq_text, str):
                try:
                    questions = faq_text.split("Q: ")[1:]
                    print(questions)

                    for question in questions:
                        q, a = question.split("A: ")
                        q = q.strip()
                        a = a.strip()

                        new_tab = {
                            "tab_title": q,
                            "tab_content": f"<p>{a}</p>",
                        }

                        faq_element["settings"]["tabs"].append(new_tab)
                except Exception as e:
                    print("Error al obtener las preguntas y respuestas:", str(e))

                save_json_file(json_file, self.local_json, "FAQ Block")
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Error al obtener las preguntas y respuestas",
                )

        except Exception as e:
            print("Error en FAQ Block:", str(e))

    def youtube_block(self):
        try:
                title = self.local_json["content"][12]["elements"][0]["elements"][0]
                content = self.local_json["content"][12]["elements"][1]["elements"][0]["elements"][0]

                title_text = self.gpt.spa_services_cta_title(title["settings"]["title"])
                content_text = self.gpt.spa_services_botox_youtube_desc(content["settings"]["editor"])

                title["settings"]["title"] = title_text
                content["settings"]["editor"] = content_text

                save_json_file(json_file, self.local_json, "Youtube Block")

        except Exception as e:
            print("Error en CTA4 Block:", str(e))

    def text_block(self):
        try:
                content = self.local_json["content"][10]["elements"][0]["elements"][0]
                
                content_text = self.gpt.spa_services_facials_text_subtitle(content["settings"]["editor"])

                content["settings"]["editor"] = content_text

                save_json_file(json_file, self.local_json, "Text Block")

        except Exception as e:
            print("Error en MAP Block:", str(e))

    def conclusion_block(self):
        try:
                title = self.local_json["content"][13]["elements"][0]
                content = self.local_json["content"][13]["elements"][1]

                title_text = self.gpt.spa_services_conclusion_title(title["settings"]["title"])
                content_text = self.gpt.spa_services_facials_conclusion_desc(content["settings"]["editor"])

                title["settings"]["title"] = title_text
                content["settings"]["editor"] = content_text

                save_json_file(json_file, self.local_json, "Conclusion Block")

        except Exception as e:
            print("Error en CTA4 Block:", str(e))