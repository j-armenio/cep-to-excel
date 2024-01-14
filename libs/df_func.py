import pandas as pd

import libs.auxx as auxx
import libs.convert as convert

OUTPUT_FILE = "out.xlsx"
BIRTHDAY_TAG = "DATA DE NASCIMENTO  "
SUBSCRIPTION_DATE_TAG = "DATA DE INSCRIÇÃO"
TX_TAG = "Data de tx"
DEATH_DATE_TAG = "DATA_ÓBITO"
HEADER_COLOR = "#EEECE1"

def test(df):
    # criar duas colunas novas
    df["RWI"] = ""
    df["ERROR"] = ""

    df.to_excel("test.xlsx", index=False)

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
    lat = coords["latitude"]
    lng = coords["longitude"]

    for i in range(len(coords_df)):
        df_lat = coords_df["latitude"][i]
        df_lng = coords_df["longitude"][i]

        if i == 0: # primeira iteração
            min_distance = auxx.get_distance(lat, lng, df_lat, df_lng)
            rwi = coords_df["rwi"][i]
            error = coords_df["error"][i]

        else:
            distance = auxx.get_distance(lat, lng, df_lat, df_lng)

            if distance < min_distance:
                min_distance = distance
                rwi = coords_df["rwi"][i]
                error = coords_df["error"][i]

    return {
        "rwi": rwi,
        "error": error
    }

def fix_excel_dates(df):
    df[BIRTHDAY_TAG] = pd.to_datetime(df[BIRTHDAY_TAG]).dt.strftime('%d/%m/%Y')
    df[SUBSCRIPTION_DATE_TAG] = pd.to_datetime(df[SUBSCRIPTION_DATE_TAG]).dt.strftime('%d/%m/%Y')
    df[TX_TAG] = pd.to_datetime(df[TX_TAG]).dt.strftime('%d/%m/%Y')
    df[DEATH_DATE_TAG] = pd.to_datetime(df[DEATH_DATE_TAG]).dt.strftime('%d/%m/%Y')

def fix_excel_styles(df): 
    writer = pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    worksheet = writer.sheets['Sheet1']

    header_format = writer.book.add_format({ # Cor do cabeçalho
        'bold': False,
        'fg_color': HEADER_COLOR,
        'border': 1,
        'align': 'center'
    })

    for i, col in enumerate(df.columns): # Ajuste automaticamente a largura das colunas
        worksheet.write(0, i, col, header_format)
        
        # print("i:", i, "col:", col)
        column_len = df[col].astype(str).str.len().max()
        column_len = max(column_len, len(col)) + 2
        # print("column_len:", column_len)
        worksheet.set_column(i, i, column_len)

    writer.close()

# Preenche a tabela de CEPs com o RWI e o erro
def complete_df_with_rwi(coords_df, cep_df):
    cep_list = cep_df["CEP"].dropna().tolist()

    # tirar o "-" do cep
    for i in range(len(cep_list)):
        cep_list[i] = cep_list[i].replace("-", "")
    
    j = 0
    for cep in cep_list:
        j += 1
        print(j)
        coords = convert.get_coordinates(cep) # pega a coordenada do cep atual

        data = find_closest_data(coords, coords_df) # data contem rwi e error do cep atual
        print(data)

        # inserir rwi e error na cep_df nas colunas RWI e ERROR
        # inserir um "-" depois do 5º digito do cep, antes do 6º
        cep_format = cep[:5] + "-" + cep[5:]

        cep_df.loc[cep_df["CEP"] == cep_format, "RWI"] = data["rwi"]
        cep_df.loc[cep_df["CEP"] == cep_format, "ERROR"] = data["error"]

        # if j == 10:
        #    break

    fix_excel_dates(cep_df)

    cep_df.to_excel(OUTPUT_FILE, index=False)

    fix_excel_styles(cep_df)