# Guia de Contribuição — Advocacia do Século XXI

Obrigado pelo interesse em contribuir! Este projeto é comunitário e toda contribuição é bem-vinda. 🎉

## Como Contribuir

### 1. Reportar Bugs

Abra uma [issue](https://github.com/roberthkairo-code/advocacia-seculo-xxi/issues) com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Logs de erro (se houver)

### 2. Sugerir Funcionalidades

Abra uma issue com a tag `enhancement` descrevendo:
- O problema que a funcionalidade resolve
- Comportamento esperado
- Exemplos de uso

### 3. Contribuir com Código

#### Setup do Ambiente de Desenvolvimento

```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/advocacia-seculo-xxi.git
cd advocacia-seculo-xxi

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instale as dependências de desenvolvimento
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves de API
```

#### Fluxo de Trabalho

```bash
# Crie uma branch para sua feature
git checkout -b feature/nome-da-feature

# Faça suas alterações
# Escreva/atualize testes
# Execute os testes
pytest tests/

# Commit seguindo Conventional Commits
git commit -m "feat: adiciona conector para TJSP"
git commit -m "fix: corrige cálculo de prazo em feriados"
git commit -m "docs: atualiza instruções de setup"

# Push e abra um Pull Request
git push origin feature/nome-da-feature
```

#### Padrões de Código

- Siga o [PEP 8](https://pep8.org/) para Python
- Use type hints em todas as funções
- Docstrings obrigatórias em classes e funções públicas
- Cobertura de testes mínima de 80%

```python
def calcular_prazo(data_inicio: datetime, dias: int, tipo: str = "uteis") -> datetime:
    """
        Calcula prazo processual conforme o CPC.

            Args:
                    data_inicio: Data de início do prazo
                            dias: Número de dias do prazo
                                    tipo: "uteis" para dias úteis ou "corridos" para dias corridos

                                        Returns:
                                                datetime: Data de vencimento do prazo

                                                    Raises:
                                                            ValueError: Se o tipo de prazo não for válido
                                                                """
                                                                    ...
                                                                    ```

                                                                    ## Áreas Prioritárias

                                                                    ### 🔌 Novos Conectores para Tribunais

                                                                    Cada tribunal precisa de um conector em `integrations/legal_systems/`. Veja `integrations/legal_systems/pje.py` como referência.

                                                                    Tribunais prioritários:
                                                                    - [ ] TJSP (Tribunal de Justiça de São Paulo)
                                                                    - [ ] TJRJ (Tribunal de Justiça do Rio de Janeiro)
                                                                    - [ ] TJMG (Tribunal de Justiça de Minas Gerais)
                                                                    - [ ] e-SAJ
                                                                    - [ ] Projudi

                                                                    ### 🧪 Testes Automatizados

                                                                    - Testes unitários para `core/deadline_calculator.py`
                                                                    - Testes de integração para conectores jurídicos
                                                                    - Mocks para APIs externas (Microsoft Graph, WhatsApp)

                                                                    ### 📖 Documentação

                                                                    - Tutoriais em português para cada funcionalidade
                                                                    - Exemplos de uso com casos reais (anonimizados)
                                                                    - Documentação da API REST

                                                                    ### 🌐 Expansão Internacional

                                                                    - Adaptação para sistemas jurídicos de outros países latino-americanos
                                                                    - Suporte a Argentina (PJN), Chile, Colômbia

                                                                    ## Estrutura do Projeto

                                                                    ```
                                                                    advocacia-seculo-xxi/
                                                                    ├── core/                    # Lógica central do sistema
                                                                    │   ├── claude_agent.py      # Agente de IA principal
                                                                    │   ├── document_parser.py   # Análise de documentos jurídicos
                                                                    │   └── deadline_calculator.py # Cálculo de prazos (CPC)
                                                                    ├── integrations/            # Conectores externos
                                                                    │   ├── microsoft/           # Microsoft Graph API
                                                                    │   ├── whatsapp/            # Notificações WhatsApp
                                                                    │   └── legal_systems/       # Sistemas jurídicos brasileiros
                                                                    ├── api/                     # Servidor REST
                                                                    ├── tests/                   # Testes automatizados
                                                                    └── docs/                    # Documentação
                                                                    ```

                                                                    ## Convenções de Commit

                                                                    Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

                                                                    | Tipo | Uso |
                                                                    |------|-----|
                                                                    | `feat` | Nova funcionalidade |
                                                                    | `fix` | Correção de bug |
                                                                    | `docs` | Documentação |
                                                                    | `test` | Testes |
                                                                    | `refactor` | Refatoração sem mudança de comportamento |
                                                                    | `chore` | Tarefas de manutenção |

                                                                    ## Código de Conduta

                                                                    Este projeto segue o [Contributor Covenant](https://www.contributor-covenant.org/). Trate todos com respeito e profissionalismo.

                                                                    ## Dúvidas?

                                                                    Abra uma issue com a tag `question` ou entre em contato via GitHub Discussions.

                                                                    ---

                                                                    **Juntos, democratizamos o acesso à tecnologia jurídica no Brasil. 🇧🇷⚖️**
