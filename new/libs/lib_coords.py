from geopy.distance import geodesic

# Retorna a distância entre dois pontos em km
def get_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

# Percorre a tabela de coordenadas e retorna o rwi e error da coordenada mais próxima
def find_closest_data(coords, coords_df):
    lat = coords["latitude"]
    lng = coords["longitude"]

    for i in range(len(coords_df)):
        df_lat = coords_df["latitude"][i]
        df_lng = coords_df["longitude"][i]

        if i == 0: # primeira iteração
            min_distance = get_distance(lat, lng, df_lat, df_lng)
            rwi = coords_df["rwi"][i]
            error = coords_df["error"][i]

        else:
            distance = get_distance(lat, lng, df_lat, df_lng)

            if distance < min_distance:
                min_distance = distance
                rwi = coords_df["rwi"][i]
                error = coords_df["error"][i]
                
    print("min_distance: ", min_distance)

    return {
        "rwi": rwi,
        "error": error
    }