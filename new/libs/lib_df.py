import pandas as pd
import libs.lib_api as lib_api
import libs.lib_coords as aux

OUTPUT_FILE = "out.xlsx"
ENROLLMENT_LABEL = "DATA DE INSCRIÇÃO"
TX_DATE_LABEL = "Data de tx"
DEATH_DATE_LABEL = "DATA_ÓBITO"
HEADER_COLOR = "#EEECE1"

def test():
    response = lib_api.get_coordinates("86802540")
    print(response)


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
        # print(cep + " - " + str(coords["latitude"]) + "," + str(coords["longitude"]))

        # Caso a API não encontre o CEP, inseri -1 no RWI e ERROR
        if (coords == None):
            cep_format = cep[:5] + "-" + cep[5:]
            cep_df.loc[cep_df["CEP"] == cep_format, "RWI"] = -1
            cep_df.loc[cep_df["CEP"] == cep_format, "ERROR"] = -1
            continue

        # data contem rwi e error do cep atual
        data = aux.find_closest_data(coords, coords_df)
        # print(str(data["rwi"]), str(data["error"]))
        
        # inserir um "-" depois do 5º digito do cep, antes do 6º
        cep_format = cep[:5] + "-" + cep[5:]

        # inserir rwi e error na cep_df nas colunas RWI e ERROR
        cep_df.loc[cep_df["CEP"] == cep_format, "RWI"] = data["rwi"]
        cep_df.loc[cep_df["CEP"] == cep_format, "ERROR"] = data["error"]

def fix_excel_dates(df):
    df[ENROLLMENT_LABEL] = pd.to_datetime(df[ENROLLMENT_LABEL]).dt.strftime('%d/%m/%Y')
    df[TX_DATE_LABEL] = pd.to_datetime(df[TX_DATE_LABEL]).dt.strftime('%d/%m/%Y')
    df[DEATH_DATE_LABEL] = pd.to_datetime(df[DEATH_DATE_LABEL]).dt.strftime('%d/%m/%Y')

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