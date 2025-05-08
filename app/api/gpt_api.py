import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class GPT:
    def __init__(self, design_data: dict):
        self.client = OpenAI()
        self.design_data = design_data
        self.service = str(design_data.get("service")).title()
        self.campaign = str(design_data.get("campaign"))
        self.city = str(design_data.get("city")).title()
        self.state = str(design_data.get("state").capitalize()).title()
        self.language = design_data.get("language")
        self.key_phrase = str(design_data.get("key_phrase")).title()
        # self.links = design_data.get("links")
        self.meta = design_data.get("meta")
        self.SYSTEM_MESSAGE = f"As a system, you can provide relevant SEO and marketing information. Always respond in {self.language}. Include the name of the city and the company only once in the entire response."
        self.ASSISTANT_MESSAGE = "As an assistant, I can help answer your SEO and marketing questions, providing useful information and tips. Include the name of the city and the company only once in the entire response."

    def create_message(self, role, content):
        return {"role": role, "content": content}

    def title_seo(self):
        system_message = self.create_message("system", self.SYSTEM_MESSAGE)
        assistant_message = self.create_message("assistant", self.ASSISTANT_MESSAGE)
        system_message2 = self.create_message(
            "system",
            "don't include your opinion or any explanation of the content generated, I just want the phrase",
        )
        user_message = self.create_message(
            "user",
            (
                f"""Generate a shot and optimized title that follows these rules:
             - The title should NOT contain ":".
             - The format must strictly be:
               '{self.key_phrase}, {self.state} | [three random services spared with a comma] +'
             - Randomly select up to *three services* from the following list: {self.meta}, ensuring they do NOT include any repair-related services.
             - Keep the title *short and optimized for SEO*
             - Ensure proper that all the words Start with a capital letter."""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [system_message2, system_message, assistant_message, user_message],
        ).replace('"', "")

    def generate_response(self, model, messages, temperature=1):
        response = self.client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )
        res = response.choices[0].message.content
        clean_response = (
            res.replace("'", " ")
            .replace("\n", " ")
            .replace("```html", " ")
            .replace("```", " ")
        )
        return clean_response


###########################################################################################################################
########################################################################################################################
################################################-------------------------####################################################
#############################-----------------------------------------------------------#################################
########################--------------------- PROMPS DE PLANTILLAS DE SERVICIO --------------###################################
#########################-------------------------------------------------------------------####################################
################################-----------------------------------------------------##########################################
#############################################################################################################################################################################################################################################################
###############################################################################################################################
    

    def spa_services_coulping_introduction_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a introduction description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/www.fda.gov\/medical-devices\/aesthetic-cosmetic-devices\/non-invasive-body-contouring-technologies\" target=\"_blank\" rel=\"noopener\">FDA<\/a>
<a href=\"https:\/\/elitechicagospa.com\/coolsculpting-in-chicago\/\" target=\"_blank\" rel=\"noopener\">CoolSculpting ELITE<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  
    

    def spa_services_cta_title(self, original_title, words=10):
        user_message = self.create_message(
            "user",
            (
               f"""Write a title for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

you can take the original text as a reference.
Original text: {original_title}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_cta_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_cta_imgdesc(self, original_desc, words=150):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")

    def spa_services_coulping_cta1_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description of call to action for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/www.fda.gov\/medical-devices\/aesthetic-cosmetic-devices\/non-invasive-body-contouring-technologies\" target=\"_blank\" rel=\"noopener\">FDA<\/a>


you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_coulping_cta3_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description of call to action for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/coolsculpting-in-chicago\/\" target=\"_blank\" rel=\"noopener\">CoolSculpting at Elite Chicago<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_coulping_cta4_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description of call to action for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/coolsculpting-in-chicago\/\">CoolSculpting in Chicago<\/a>
<a href=\"https:\/\/elitechicagospa.com\/coolsculpting-in-chicago\/\" target=\"_blank\">CoolSculpting Elite<\/a>
<a href=\"https:\/\/www.chicago.gov\/city\/en.html\" target=\"_blank\">Chicago<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_introduction_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a introduction description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def faq_services(self):
            system_message = self.create_message("system", self.SYSTEM_MESSAGE)
            user_message = self.create_message(
            "user",
            (
            f"""Generate one Frequently Asked Question (FAQ) and its answer for the company {self.campaign} with services in {self.service} in the city of {self.city}, {self.state}.
            The question should feel natural and address common client concerns such as safety, comfort, effectiveness, results, or services preparation.
            Avoid common topics like pricing, scheduling, or cancellation policies. Mention "{self.city}" only if it sounds natural and relevant.
            Do not include the company name.
            Use this format:
            Q: [question]
            A: [answer]
            Tone: warm, professional, and reassuring. Do not include any extra commentary — only the Q and A.
            give me the answer in the language: {self.language}"""
            ),
            )
            return self.generate_response(
            "gpt-3.5-turbo", [system_message, user_message]
            ).replace('"', "")

################################### BOTOX ########################################################################

    def spa_services_botox_cta3_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/botox-chicago\/\" target=\"_blank\" rel=\"noopener\">Botox in Chicago<\/a>


you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  
    
    def spa_services_botox_cta5_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/botox-chicago\/\" target=\"_blank\">BOTOX&nbsp; treatments&nbsp;<\/a>
<a href=\"https:\/\/elitechicagospa.com\/botox-chicago\/\" target=\"_blank\">BOTOX&nbsp; in Chicago&nbsp;<\/a>
you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_botox_youtube_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
            f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
            Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
            Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
            For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

            Please include the following hyperlinks somewhere in the text:
            <a href="https://elitechicagospa.com/botox-chicago/" target="_blank" rel="noopener">Botox in Chicago</a>

            At the end of your description, include a gentle call to action that invites users to subscribe or visit the YouTube channel to learn more, explore behind-the-scenes content, or get helpful tips related to the service.

            Original text: {original_desc}
            give me the answer in the language: {self.language}
            """

            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  
    
    def spa_services_map_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
                f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
                Your version should maintain the same spirit: uplifting, confident, and action-oriented. Emphasize the benefits of accessing this service locally in {self.city}, and make the reader feel connected to their area. Mention how having nearby services improves convenience, response time, or personalization. The tone should remain natural, easy to read, and suitable for a broad audience. Don't include quotation marks in your answer.
                For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.
                This section appears next to a city map, so make sure to reference the visual context—encouraging readers to locate their area on the map or visualize proximity.
                Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.

                Please include the following hyperlinks somewhere in the text:
                <a href="https://www.chicago.gov/city/en.html" target="_blank" rel="noopener">Chicago</a>
                <a href="https://elitechicagospa.com/botox-chicago/" target="_blank" rel="noopener">Botox treatments in Chicago</a>

                At the end of your description, include a gentle call to action that invites users to subscribe or visit the YouTube channel to learn more, explore behind-the-scenes content, or get helpful tips related to the service.

                Original text: {original_desc}
                give me the answer in the language: {self.language}
                """
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_conclusion_title(self, original_title, words=10):
        user_message = self.create_message(
            "user",
            (
               f"""Write a conclusion title for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

you can take the original text as a reference.
Original text: {original_title}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_conclusion_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a conclusion description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "") 
    
############################################## FACIALS ########################################################

    def spa_services_facials_introduction_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a introduction description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a style=\"font-size: 17px; background-color: #ffffff;\" href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" rel=\"noopener\">Facial treatments<\/a>
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" rel=\"noopener\">Hydrafacial<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_facials_cta1_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" style=\"font-size: 17px; background-color: rgb(255, 255, 255);\">Facials in Chicago<\/a>
<a href=\"https:\/\/elitechicagospa.com\/\" target=\"_blank\" rel=\"noopener\">Med Spa Chicago<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "") 

    def spa_services_facials_cta3_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a style=\"font-size: 17px; background-color: #ffffff;\" href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" rel=\"noopener\">HydraFacial<\/a>
<a style=\"font-size: 17px; background-color: #ffffff;\" href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" rel=\"noopener\">HydraFacial<\/a>
you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "") 

    def spa_services_facials_cta4_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\"> best facials in Chicago<\/a>
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\">microneedling<\/a>
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\">HydraFacial<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "") 
    
    def spa_services_facials_cta6_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" rel=\"noopener\">facial treatment in Chicago\u00a0<\/a>
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" rel=\"noopener\">hydrate<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "") 
    def spa_services_facials_conclusion_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a text of conclusion for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a style=\"font-weight: bold;\" href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" rel=\"noopener\"> facial in Chicago<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "") 

    def spa_services_facials_text_subtitle(self, original_desc, words=150):
        user_message = self.create_message(
            "user",
            (
               f"""Write a text of conclusion for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\" target=\"_blank\" rel=\"noopener\">facial Chicago<\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "") 

############################### -------------- LASER ----------------- #########################################

    def spa_services_laser_introduction_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a introduction description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:
<a href=\"https:\/\/elitechicagospa.com\/facials-chicago\/\"><strong data-start=\"976\" data-end=\"997\">facial treatments<\/strong> <\/a>
<a href=\"https:\/\/elitechicagospa.com\/laser-hair-removal-in-chicago\/\"><strong data-start=\"1115\" data-end=\"1137\">laser hair removal<\/strong><\/a>

you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_laser_cta4_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
               f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

Please include the following hyperlinks somewhere in the text:


you can take the original text as a reference.
Original text: {original_desc}
give me the answer in the language: {self.language}
"""
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "") 

    def spa_services_laser_youtube_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
            f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
            Your version should maintain the same spirit: uplifting, confident, and action-oriented. The quality of service, materials, professionalism, and efficiency; it should be natural, easy to read, and use language that can be flexible for all audiences. Don't include quotation marks in your answer.
            Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.
            For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.

            At the end of your description, include a gentle call to action that invites users to subscribe or visit the YouTube channel to learn more, explore behind-the-scenes content, or get helpful tips related to the service.

            Original text: {original_desc}
            give me the answer in the language: {self.language}
            """

            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  

    def spa_services_laser_map_desc(self, original_desc, words=40):
        user_message = self.create_message(
            "user",
            (
                f"""Write a description for a page of {self.service} with a company called: {self.campaign} in the city of {self.city}, {self.state}:
                Your version should maintain the same spirit: uplifting, confident, and action-oriented. Emphasize the benefits of accessing this service locally in {self.city}, and make the reader feel connected to their area. Mention how having nearby services improves convenience, response time, or personalization. The tone should remain natural, easy to read, and suitable for a broad audience. Don't include quotation marks in your answer.
                For your answer, take into account the structure and the highlighted texts in the original text, so that you create a similar structure, so that the structure is as similar as possible, but with different content.
                This section appears next to a city map, so make sure to reference the visual context—encouraging readers to locate their area on the map or visualize proximity.
                Avoid clickbait phrases or overused marketing language. Do not include the company name. Keep it within {words} words total.

                Please include the following hyperlinks somewhere in the text:
                <a href=\"https:\/\/www.choosechicago.com\/\" target=\"_blank\" style=\"font-size: 17px; background-color: rgb(255, 255, 255);\">Chicago<\/a>

                At the end of your description, include a gentle call to action that invites users to subscribe or visit the YouTube channel to learn more, explore behind-the-scenes content, or get helpful tips related to the service.

                Original text: {original_desc}
                give me the answer in the language: {self.language}
                """
            ),
        )
        return self.generate_response(
            "gpt-3.5-turbo",
            [self.create_message("system", self.SYSTEM_MESSAGE), user_message],
        ).replace('"', "")  
