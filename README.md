# Como utilizar a aplicação

1. Clone o repositório com o seguinte comando:
    ```sh
    $ git clone https://github.com/lucascalixtos/FLASK_StarWarsAPI.git
    ```
2. Acesse o diretório clonado:
   ```sh
    $ cd FLASK_StarWarsAPI
    ```
3. Existem duas maneiras de executar a aplicação, via docker ou na sua maquina local
    - Execução via docker
        * Digite o seguinte comando para montar o ambiente da aplicação
             ```sh
            $ docker build -t flasksw .
            ```
        * Para iniciar a aplicação digite:
            ```sh
            $ docker build -t flasksw .
            ```
        * Aguarde a aplicação ser inicializada. Para acessá-la basta acessar o seguinte endereço:
             ```sh
            $ localhost:5000
            ```       
    - Execução local
        * Para a aplicação rodar é necessário ter instalado duas bibliotecas do python, Flask e Requests. Digite os comando abaixo para instalá-las:
             ```sh
            $ pip install flask
            $ pip install requests
            ```
        * Para inicializar a aplicação basta digitar o comando abaixo:
            ```sh
            $ python main.py
            ```  
        * Aguarde a aplicação ser inicializada. Para acessá-la basta acessar o seguinte endereço:
             ```sh
            $ localhost:5000
            ```   
