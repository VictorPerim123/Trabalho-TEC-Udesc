🧠 Tradutor de Modelos de Máquina de Turing

📘 Descrição
Este projeto implementa um tradutor entre modelos de Máquina de Turing conforme especificado no trabalho da disciplina. O tradutor converte programas entre os dois modelos clássicos:
* Modelo de Sipser (;S) — fita semi-infinita (com início à esquerda)
* Modelo de fita duplamente infinita (;I)

O objetivo é gerar uma máquina equivalente que reconheça a mesma linguagem, mas utilizando o modelo oposto.
A sintaxe utilizada é compatível com o simulador online de Máquinas de Turing disponível em: 👉 http://morphett.info/turing/turing.html

👨‍💻 Autores
Este trabalho foi feito pelos alunos: Victor Alexandre e Gustavo Gonçalves.

⚙️ Funcionalidades
* 🔄 Tradução automática entre modelos (;S ↔ ;I)
* 🧩 Suporte total à sintaxe do simulador do Morphett
* 🧱 Simulação de parede esquerda (Sipser) e deslocamento de fita (Infinita).
* ✅ Compatível com Ubuntu 22.04.4 LTS (64 bits) e Python 3
* 🧾 Saída clara e comentada, pronta para ser executada no simulador online

🗂️ Estrutura dos Arquivos
* tradutor_mt.py → Script principal (tradutor)
* exemplo.in → Exemplo de entrada (modelo de Sipser)
* exemplo.out → Exemplo de saída (modelo duplamente infinito)
* README.md → Este arquivo

🚀 Instruções de Execução
1️⃣ Pré-requisitos
* Python 3 instalado (testado com Python 3.10+)
* Sistema operacional: Ubuntu 22.04.4 LTS (64 bits)

Verifique se o Python está disponível:
python3 --version

2️⃣ Executar o tradutor
No terminal, dentro da pasta do projeto, execute:
python3 tradutor_mt.py <arquivo_entrada.in>

Exemplo:
python3 tradutor_mt.py exemplo.in

O programa detectará automaticamente o modelo (;S ou ;I) e criará um arquivo de saída com a extensão .out, contendo o modelo oposto.

3️⃣ Resultado
Após a execução, será exibida uma mensagem semelhante a:
Traduzindo de Sipser para Fita Duplamente Infinita... Tradução concluída! O resultado foi salvo em 'exemplo.out'

O arquivo .out estará pronto para ser testado no simulador online.

🧪 Testes
Os testes foram realizados no simulador online: 👉 http://morphett.info/turing/turing.html
Tanto a máquina original (.in) quanto a traduzida (.out) reconhecem a mesma linguagem.

📂 Repositório
📎 Link para o repositório público no GitHub: (adicione aqui o link do seu repositório, por exemplo:) https://github.com/seu-usuario/tradutor-mt

👨‍💻 Autores
Este trabalho foi feito pelos alunos: Victor Alexandre e Gustavo Gonçalves.
Professora: Karina Roggia
Universidade do Estado de Santa Catarina (UDESC)

🏁 Licença
Este projeto é de uso educacional e está licenciado sob a licença MIT
