from flask import Response, Flask, request, jsonify
import re
import requests
import os
import json
app = Flask(__name__)

def Levii(value):
    if len(value) >= 2:
        return value[2:] + value[:2]
    return value

def Levi_Ai(data):
    for key in ['__csr', '__dyn']:
        if key in data:
            data[key] = Levii(data[key])
    return data

class MetaAI:
    def __init__(self):
        self.base_url = "https://www.meta.ai"
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            'sec-ch-ua-mobile': "?1",
            'sec-ch-ua-platform': "\"Android\"",
            'upgrade-insecure-requests': "1",
            'sec-fetch-site': "none",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'accept-language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.initialize_session()

    def initialize_session(self):
        response = requests.get(self.base_url, headers=self.headers)
        self.am = response.cookies.get_dict().get('datr')
        
        self.token = self._extract_pattern(response.text, r'"token":"(.*?)"')
        self.csrf_token = self._extract_pattern(response.text, r'"abra_csrf":{"value":"(.*?)"', apply_levii=True)
        self.haste_session = self._extract_pattern(response.text, r'"haste_session":"(.*?)"', apply_levii=True)
        self.id_value = self._extract_pattern(response.text, r'"require":\[\["qplTimingsServerJS",null,null,\["(.*?)","tierThree"\]\]', apply_levii=True)
        
        self._get_access_token()

    def _extract_pattern(self, text, pattern, apply_levii=False):
        match = re.search(pattern, text)
        if match:
            value = match.group(1)
            return Levii(value) if apply_levii else value
        return None

    def _get_access_token(self):
        url = "https://www.meta.ai/api/graphql/"
        payload = {
            'av': "0",
            '__user': "0",
            '__a': "1",
            '__req': "c",
            '__hs': self.haste_session,
            'dpr': "1",
            '__ccg': "MODERATE",
            '__rev': "1018999285",
            '__s': ":h7mqcr:kpgbn7",
            '__hsi': self.id_value,
            '__dyn': "7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo1nEhw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D85m1mzXwae4UaEW0Loco5G0zK1swa-0nK3qazo11E2ZwrUdUco9E3Lwr86C1nw4xxW2W5-fwmUaE2Tw",
            '__csr': "gq9mynqG8uhmRqCOuZ28kGJo-HU_Dz946EaE01kKo9o1l8fU4K5ooG0Rqwqo0YeiE0a9EZ0IXhqwcl340R82Fwa-7U1BAag5B6y4aw1kbgKn4wHiiU8CcgbpYgEikk82HxlyqA8xigjw4l4389Q2F5sgUwk6K0ENdDwDgaG8ag11A0zUg-3Ijc0xzonxQ8R2g",
            'lsd': self.token,
            'jazoest': "2979",
            '__spin_r': "1018999285",
            '__spin_b': "trunk",
            '__spin_t': "1734643764",
            '__jssesw': "1",
            'fb_api_caller_class': "RelayModern",
            'fb_api_req_friendly_name': "useAbraAcceptTOSForTempUserMutation",
            'variables': '{"dob":"1900-01-01","icebreaker_type":"TEXT_V2","__relay_internal__pv__AbraFileUploadsrelayprovider":false,"__relay_internal__pv__AbraSurfaceNuxIDrelayprovider":"12177","__relay_internal__pv__AbraQPFileUploadTransparencyDisclaimerTriggerNamerelayprovider":"meta_dot_ai_abra_web_file_upload_transparency_disclaimer","__relay_internal__pv__AbraUpsellsKillswitchrelayprovider":true,"__relay_internal__pv__WebPixelRatiorelayprovider":1,"__relay_internal__pv__AbraIcebreakerImagineFetchCountrelayprovider":20,"__relay_internal__pv__AbraImagineYourselfIcebreakersrelayprovider":false,"__relay_internal__pv__AbraEmuReelsIcebreakersrelayprovider":false,"__relay_internal__pv__AbraQueryFromQPInfrarelayprovider":false}',
            'doc_id': "8806448829408857"
        }
        
        headers = {
            **self.headers,
            'x-fb-friendly-name': "useAbraAcceptTOSForTempUserMutation",
            'x-fb-lsd': self.token,
            'x-asbd-id': "129477",
            'sec-ch-ua-full-version-list': "\"Not-A.Brand\";v=\"99.0.0.0\", \"Chromium\";v=\"124.0.6327.4\"",
            'sec-ch-ua-model': "\"RMX3834\"",
            'sec-ch-prefers-color-scheme': "dark",
            'origin': self.base_url,
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': self.base_url,
            'Cookie': f"datr={self.am}; dpr=1.9562236070632935; abra_csrf={self.csrf_token}; wd=368x695"
        }
        
        payload = Levi_Ai(payload)
        response = requests.post(url, data=payload, headers=headers)
        self.access_token = self._extract_pattern(response.text, r'"access_token":"(.*?)"')

    def chat(self, message):
        url = "https://graph.meta.ai/graphql"
        payload = {
            'av': '0',
            'access_token': self.access_token,
            '__user': '0',
            '__a': '1',
            '__req': 'k',
            '__hs': self.haste_session,
            'dpr': "1",
            '__ccg': "MODERATE",
            '__rev': "1018999285",
            '__s': ":h7mqcr:kpgbn7",
            '__hsi': self.id_value,
            '__dyn': '7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D85m1mzXwae4UaEW0Loco5G0zK1swa-0nK3qazo11E2ZwrUdUco9E3Lwr86C1nw4xxW2W5-fwmUaE2Tw',
            '__csr': 'guTfDGgDJGF7Jdbtpk8HVVGBKWDh8myAi5EaU01kJ8y0nG3-1ayHbxmiE3lG1Fw3MFqw0EKy8jxqAQm0JUCHg3uw5sg1HFRwo2z80lioDCcEigpFqhUC9Bo4cWx9hFgGeDA89BdN01aNd289Q2G862YUtU2w4P4wDgaV60hbw8-4lwTjb4086lZ1u6wINU',
            '__comet_req': '46',
            'lsd': self.token,
            'jazoest': '2952',
            '__spin_r': '1019004711',
            '__spin_b': 'trunk',
            '__spin_t': '1734647505',
            '__jssesw': '1',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useAbraSendMessageMutation',
            'variables': f'{{"message":{{"sensitive_string_value":"{message}"}},"externalConversationId":"8a326ffc-627e-490f-8484-1bfafc5ecef6","offlineThreadingId":"3275639084897897359","icebreaker_type":"TEXT_V2","__relay_internal__pv__AbraFileUploadsrelayprovider":false,"__relay_internal__pv__AbraSurfaceNuxIDrelayprovider":"12177"}}',
            'doc_id': '8817425991675807'
        }
        
        headers = {
            **self.headers,
            'sec-ch-ua-platform-version': "\"14.0.0\"",
            'origin': self.base_url,
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'referer': self.base_url,
            'Cookie': f"datr={self.am}; dpr=1.9562236070632935; abra_csrf={self.csrf_token}; wd=368x695"
        }
        
        payload = Levi_Ai(payload)
        response = requests.post(url, params={'locale': 'user'}, data=payload, headers=headers)
        msg = re.findall(r'"snippet":"(.*?)"', response.text)
        
        if msg:
            return max(msg, key=len).encode("utf-8").decode("unicode-escape", errors="ignore")
        return "No response found"

meta_ai = MetaAI()



@app.route('/ask', methods=['GET'])
def ask():
    message = request.args.get('message')
    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # استدعاء دالة meta_ai.chat() للحصول على الرد
        response = meta_ai.chat(message)

        # إعداد الاستجابة بتنسيق JSON مع دعم UTF-8 للنصوص العربية والإيموجي
        return Response(
            json.dumps({
                "response": response
            }, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
