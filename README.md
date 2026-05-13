# ⚖️ Advocacia do Século XXI

> Open source AI-powered legal ecosystem for Brazilian lawyers — built on Claude.
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
> [![Built with Claude](https://img.shields.io/badge/Built%20with-Claude%20AI-orange)](https://www.anthropic.com)
> [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
> [![Open Source](https://img.shields.io/badge/Open-Source-blue)](https://github.com/roberthkairo-code/advocacia-seculo-xxi)
>
> ---
>
> ## 🇧🇷 O Problema
>
> Advogados brasileiros perdem horas preciosas em tarefas repetitivas: ler andamentos de processos, copiar prazos para o calendário, redigir petições do zero, acompanhar múltiplos sistemas jurídicos e responder clientes sobre o status dos casos.
>
> **Advocacia do Século XXI** resolve tudo isso com IA — usando Claude como cérebro central.
>
> ---
>
> ## 🚀 Funcionalidades
>
> ### 📄 Leitura Inteligente de Documentos
> - OCR de recortes de processos (imagens e PDFs)
> - - Extração automática de: número do processo, partes, comarca, prazos e intimações
>   - - Classificação do tipo de demanda e urgência
>    
>     - ### ✍️ Redação Automatizada de Peças
>     - - Claude lê o processo, entende o contexto e redige a petição
>       - - Suporte a: contestações, recursos, petições simples, manifestações
>         - - O advogado apenas revisa e assina — economia de até 80% do tempo
>          
>           - ### 📅 Agenda Inteligente de Prazos
>           - - Integração com **Microsoft Outlook Calendar**
>             - - Criação automática de eventos com alertas antecipados
>               - - Cálculo de prazos processuais conforme o CPC
>                
>                 - ### ✅ Gestão de Tarefas
>                 - - Integração com **Microsoft To Do**
>                   - - Criação automática de tarefas por processo
>                     - - Priorização inteligente por urgência e prazo
>                      
>                       - ### 📲 Notificações via WhatsApp
>                       - - Alertas automáticos de andamentos processuais
>                         - - Notificações de prazos se aproximando
>                           - - Resumo diário da agenda jurídica
>                            
>                             - ### ⚖️ Conectores para Sistemas Jurídicos
>                             - Arquitetura modular — cada sistema é um conector independente:
>                             - - ✅ PJe (Processo Judicial Eletrônico)
>                               - - ✅ SAJ (Sistema de Automação da Justiça)
>                                 - - ✅ Themis
>                                   - - 🔜 e-SAJ
>                                     - - 🔜 Projudi
>                                       - - 🔜 TJSP, TJRJ, TJMG (tribunais estaduais)
>                                        
>                                         - ---
>
> ## 🏗️ Arquitetura
>
> ```
> advocacia-seculo-xxi/
> ├── core/
> │   ├── claude_agent.py        # Agente principal (Claude API)
> │   ├── document_parser.py     # OCR e extração de dados
> │   └── deadline_calculator.py # Cálculo de prazos CPC
> ├── integrations/
> │   ├── microsoft/
> │   │   ├── calendar.py        # Microsoft Graph API - Calendar
> │   │   └── todo.py            # Microsoft Graph API - To Do
> │   ├── whatsapp/
> │   │   └── notifier.py        # WhatsApp via Evolution API
> │   └── legal_systems/
> │       ├── pje.py             # Conector PJe
> │       ├── saj.py             # Conector SAJ
> │       └── themis.py          # Conector Themis
> ├── api/
> │   └── server.py              # API REST principal
> ├── docs/
> │   └── setup.md               # Guia de configuração
> ├── .env.example               # Variáveis de ambiente (modelo)
> ├── requirements.txt
> └── README.md
> ```
>
> ---
>
> ## 🛠️ Stack Tecnológica
>
> | Componente | Tecnologia |
> |---|---|
> | IA Principal | Claude API (Anthropic) |
> | OCR | Tesseract / Google Vision API |
> | Calendário & To Do | Microsoft Graph API |
> | WhatsApp | Evolution API (open source) |
> | Backend | Python / FastAPI |
> | Banco de Dados | SQLite / PostgreSQL |
>
> ---
>
> ## ⚡ Início Rápido
>
> ### Pré-requisitos
> - Python 3.10+
> - - Chave de API da Anthropic (Claude)
>   - - Conta Microsoft 365
>     - - Evolution API configurada (para WhatsApp)
>      
>       - ### Instalação
>      
>       - ```bash
>         # Clone o repositório
>         git clone https://github.com/roberthkairo-code/advocacia-seculo-xxi.git
>         cd advocacia-seculo-xxi
>
>         # Instale as dependências
>         pip install -r requirements.txt
>
>         # Configure as variáveis de ambiente
>         cp .env.example .env
>         # Edite o arquivo .env com suas chaves de API
>
>         # Inicie o servidor
>         python api/server.py
>         ```
>
> ### Configuração do `.env`
>
> ```env
> ANTHROPIC_API_KEY=sua_chave_aqui
> MICROSOFT_CLIENT_ID=seu_client_id
> MICROSOFT_CLIENT_SECRET=seu_secret
> WHATSAPP_API_URL=http://localhost:8080
> WHATSAPP_INSTANCE=sua_instancia
> ```
>
> ---
>
> ## 🤝 Como Contribuir
>
> Contribuições são muito bem-vindas! Este projeto foi criado para ser comunitário.
>
> ```bash
> # 1. Fork o repositório
> # 2. Crie uma branch para sua feature
> git checkout -b feature/novo-conector-tribunal
>
> # 3. Faça suas alterações e commit
> git commit -m "feat: adiciona conector TJSP"
>
> # 4. Abra um Pull Request
> ```
>
> ### Áreas que precisam de contribuidores
> - 🔌 Novos conectores para tribunais estaduais
> - - 🧪 Testes automatizados
>   - - 📖 Documentação e tutoriais
>     - - 🌐 Suporte a outros sistemas jurídicos latino-americanos
>      
>       - ---
>
> ## 📋 Roadmap
>
> - [x] Estrutura base do projeto
> - [ ] - [x] Integração com Claude API
> - [ ] - [ ] OCR de documentos PDF e imagens
> - [ ] - [ ] Conector PJe
> - [ ] - [ ] Conector SAJ
> - [ ] - [ ] Integração Microsoft Calendar
> - [ ] - [ ] Integração Microsoft To Do
> - [ ] - [ ] Notificações WhatsApp
> - [ ] - [ ] Interface web
> - [ ] - [ ] App mobile
>
> - [ ] ---
>
> - [ ] ## 📄 Licença
>
> - [ ] MIT License — veja o arquivo [LICENSE](LICENSE) para detalhes.
>
> - [ ] ---
>
> - [ ] ## 💬 Contato
>
> - [ ] Desenvolvido por [Roberth Kairo](https://github.com/roberthkairo-code) — advogado e desenvolvedor apaixonado por democratizar o acesso à tecnologia jurídica no Brasil.
>
> - [ ] ---
>
> - [ ] > *"A tecnologia não substitui o advogado — ela libera o advogado para ser mais advogado."*
