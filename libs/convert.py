import requests
import json
from geopy.distance import geodesic

URL_GET_ADDRESS_FROM_CEP = "https://www.cepaberto.com/api/v3/cep?cep={}"
CEP_TEST = "81670040"

def get_coordinates(cep):
    try:
        url = URL_GET_ADDRESS_FROM_CEP.format(cep)
        headers = {"Authorization": f'Token token={"7431ae0004d4dfe1da7e0c3e7d815cfb"}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            json_response = response.json()
            
            return {
                "latitude": float(json_response["latitude"]),
                "longitude": float(json_response["longitude"]),
            }
        
        elif response.status_code == 400:
            print("CEP inválido")
            return None
        
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)