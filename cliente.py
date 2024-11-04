import requests
import pandas as pd
from Levenshtein import distance

try:
    response = requests.get("http://127.0.0.1:8000/fake-names", auth=('user1', 'password1'))
    response.raise_for_status() 
    names = response.json()

    # Calcular distâncias de Levenshtein
    origem_nome = names[0]
    distances = [(name, distance(origem_nome, name)) for name in names[1:]]

    # Organizar DataFrame
    df = pd.DataFrame(distances, columns=["Nome", "Distância para origem"])
    df = df.sort_values(by="Distância para origem")

    print(df)

except requests.exceptions.RequestException as e:
    print(f"Erro ao buscar dados da API: {e}")
