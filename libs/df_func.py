import pandas as pd

import libs.auxx as auxx
import libs.convert as convert

# Lê o arquivo e retorna um dataframe
def read_file(file_name):
    if file_name.endswith(".csv"):
        df = pd.read_csv(file_name)
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(file_name)
    else:
        print("Formato de arquivo inválido")
        exit()
    return df

# percorre a tabela de coordenadas e retorna o rwi e error da coordenada mais próxima
def find_closest_data(coords, coords_df):
    curr_lat = coords["lat"]
    curr_lng = coords["lng"] # PAREI AQUI!!!!!!!!!!!

# Preenche a tabela de CEPs com o RWI e o erro
def complete_df_with_rwi(coords_df, cep_df):
    cep_list = cep_df["CEP"].dropna().tolist()

    for i in range(len(cep_list)):
        cep_list[i] = cep_list[i].replace("-", "")
    
    for cep in cep_list:
        coords = convert.get_coordinates(cep)

        rwi = find_closest_data(coords, coords_df) # PAREI AQUI!!!!!!!!!!!