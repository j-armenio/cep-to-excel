from libs import lib_dfl

TEST_COORDS_FILE = "tests/relative_wealth_index_copia.csv"
TEST_CEP_FILE = "tests/DADOS_PESQUISA_COPIA.xlsx"

#coords_file_name = input("Tabela de cordenadas: ")
#cep_file_name = input("Tabela de ceps: ")

try:
    #coords_df = df_func.read_file(coords_file_name)
    #cep_df = df_func.read_file(cep_file_name)

    coords_df = lib_dfl.read_file(TEST_COORDS_FILE)
    cep_df = lib_dfl.read_file(TEST_CEP_FILE)    
except FileNotFoundError:
    print("Arquivo não encontrado")
    exit()

# Função que copia os rwi equivalentes aos ceps no cep_df
lib_dfl.copy_rwi_to_cep_df(coords_df, cep_df)

# Formata as datas do cep_df que são quebradas no processo
lib_dfl.fix_excel_dates(cep_df)

# Salva o arquivo
cep_df.to_excel(lib_dfl.OUTPUT_FILE, index=False)

# Arruma os tamanhos e estilos das colunas
lib_dfl.fix_excel_styles(cep_df)

print("Arquivo salvo com sucesso")