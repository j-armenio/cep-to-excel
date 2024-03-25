from new.libs import lib_dfl

TEST_COORDS_FILE = "tests/relative_wealth_index_copia.csv"
TEST_CEP_FILE = "tests/modelo_busca_copia.xlsx"

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

lib_dfl.cp_rwi_to_cep_df(coords_df, cep_df)
