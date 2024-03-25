# cep-to-excel

## São recebidas duas tabelas excel:
    - Uma contendo várias informações de pacientes, entre elas o CEP, T_CEP;
    - Outra que contem a latitude, longitude e rwi, T_RWI;

## OBJETIVO:
    Incluir na tabela de pacientes uma coluna que contém o rwi desse paciente.
    * rwi = um indice que representa a qualidade de vida monetária de uma pessoa com base de onde ela mora *

## PROCESSO:
    1. Receber ambas tabelas e converte-lás em dataframes usando o pandas;
    2. Extrair uma lista de CEPs da T_CEP;
    3. Iterar na lista, e para cada CEP:
        3.1. Converter o CEP em coordenada usando o geopy;
        3.2. Encontrar qual a coordenada mais próxima da coordenada equivalente, usando lat e long da T_RWI;
        3.3. Inserir o 'RWI' encontrado e seu 'Error' na T_CEP;
    4. Transformar o df em excel.
    5. Arrumar formatações do excel.