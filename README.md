# GPX Pace Autocorrelation Analysis

Este repositório contém um script em Python desenvolvido para analisar arquivos de rastreamento GPS no formato GPX. O objetivo principal do código é extrair dados de latitude, longitude e tempo, calcular o ritmo (pace) da atividade em intervalos regulares e, por fim, calcular e visualizar a autocorrelação desse ritmo.

## Funcionalidades

O script executa as seguintes operações:

1. **Extração de Dados:** Utiliza expressões regulares para ler arquivos GPX brutos e extrair as tags de latitude, longitude e tempo.
2. **Cálculo de Distância:** Aplica a Fórmula de Haversine para calcular a distância percorrida entre os pontos de coordenadas em metros.
3. **Cálculo de Ritmo (Pace):** Interpola as distâncias e os tempos acumulados para calcular o ritmo do usuário (em minutos por quilômetro) a cada 1 metro percorrido.
4. **Análise de Autocorrelação:** Calcula a função de autocorrelação do vetor de ritmo para identificar padrões, dependências ou a consistência da velocidade ao longo da distância.
5. **Visualização:** Gera um gráfico da função de autocorrelação utilizando a biblioteca Matplotlib, com formatação padronizada para artigos científicos (fonte serifada, marcações internas, etc.).

## Pré-requisitos

Para executar este script, você precisará do Python 3 instalado em sua máquina, juntamente com as seguintes bibliotecas:

* `numpy`
* `matplotlib`

Você pode instalá-las utilizando o gerenciador de pacotes pip:

```bash
pip install numpy matplotlib
```

## Como utilizar

1. **Preparação dos Dados:** 
   O script busca por padrão um arquivo GPX no diretório e com o nome `\data\2026-04-14-135538.gpx`. Certifique-se de ter um arquivo de dados válido nesse caminho ou altere a string correspondente no bloco `with open(...)` para apontar para o seu arquivo GPX.

2. **Execução:**
   Execute o script em seu ambiente Python ou terminal:

   ```bash
   python nome_do_arquivo.py
   ```

3. **Saídas:**
   * **Console:** O script imprimirá o ritmo (pace) médio geral da atividade no console.
   * **Gráfico:** Uma janela do Matplotlib será aberta exibindo o gráfico da função de autocorrelação `A(k)` em relação ao lag `k` (com `k` variando de 0 a 99).

## Estrutura do Código

* `dist(lat1, lon1, lat2, lon2)`: Função que recebe as coordenadas geográficas de dois pontos e retorna a distância entre eles em metros utilizando a fórmula de Haversine.
* `autocorrl(k, e)`: Função que calcula a autocorrelação de um array `e` até um número de lags (defasagens) `k`.
* **Bloco de Leitura e Parsing:** Usa `re.findall` para capturar os dados do GPX sem a necessidade de um parser XML pesado.
* **Bloco de Interpolação:** Usa `np.interp` para padronizar os dados de tempo e distância, permitindo um cálculo de ritmo uniforme.

## Notas Adicionais

* A variável `marks` foi definida com passo de 1, o que significa que o script avalia as métricas a cada 1 metro. 
* O parâmetro `km = 100` passado para a função de autocorrelação define que o algoritmo avaliará as defasagens de 0 até 99 metros. Caso a atividade seja muito longa e você deseje uma visão macro da autocorrelação, recomenda-se ajustar esse valor ou a escala das marcações.
```
