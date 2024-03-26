import pandas as pd

import libs.lib_api as lib_api
import libs.lib_coords as aux

OUTPUT_FILE = "out.xlsx"
BIRTHDAY_TAG = "DATA DE NASCIMENTO  "
SUBSCRIPTION_DATE_TAG = "DATA DE INSCRIÇÃO"
TX_TAG = "Data de tx"
DEATH_DATE_TAG = "DATA_ÓBITO"
HEADER_COLOR = "#EEECE1"

# Lê o arquivo csv ou excel e retorna um dataframe com os dados
def read_file(file_name):
    if file_name.endswith(".csv"):
        df = pd.read_csv(file_name)
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(file_name)
    else:
        print("Formato de arquivo inválido")
        exit()
    
    return df

def copy_rwi_to_cep_df(coords_df, cep_df):
    cep_list = cep_df["CEP"].dropna().tolist()

    # Remove o "-" de todos os CEPs
    cep_list = [str(cep).replace('-', '') for cep in cep_list]
    
    j = 0
    for cep in cep_list:
        j += 1
        print(j)
        
        # Pega a coordenada do cep atual
        coords = lib_api.get_coordinates(cep)
        print(cep + " - " + str(coords["latitude"]) + "," + str(coords["longitude"]))

        # data contem rwi e error do cep atual
        data = aux.find_closest_data(coords, coords_df)
        print(str(data["rwi"]), str(data["error"]))
        
        # # inserir um "-" depois do 5º digito do cep, antes do 6º
        cep_format = cep[:5] + "-" + cep[5:]

        # inserir rwi e error na cep_df nas colunas RWI e ERROR
        cep_df.loc[cep_df["CEP"] == cep_format, "RWI"] = data["rwi"]
        cep_df.loc[cep_df["CEP"] == cep_format, "ERROR"] = data["error"]

        if j == 5:
            break
