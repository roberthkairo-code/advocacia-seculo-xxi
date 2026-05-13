"""
core/claude_agent.py
Agente principal que usa Claude para processar documentos jurídicos
e coordenar todas as integrações do ecossistema.
"""

import anthropic
from typing import Optional
from loguru import logger
from pydantic import BaseModel


class ProcessoInfo(BaseModel):
      """Informações extraídas de um processo judicial."""
      numero_processo: Optional[str] = None
      partes: Optional[dict] = None
      comarca: Optional[str] = None
      vara: Optional[str] = None
      prazos: Optional[list] = None
      tipo_acao: Optional[str] = None
      urgencia: Optional[str] = None
      proximas_acoes: Optional[list] = None
      resumo: Optional[str] = None


class ClaudeAgent:
      """
          Agente principal do sistema.
              Usa Claude para:
                  - Analisar documentos e extrair informações processuais
                      - Redigir peças jurídicas
                          - Sugerir estratégias processuais
                              - Coordenar as demais integrações
                                  """

    SYSTEM_PROMPT = """
        Você é um assistente jurídico especializado no direito brasileiro.
            Sua função é auxiliar advogados a:
                1. Analisar documentos e processos judiciais
                    2. Extrair informações relevantes (prazos, partes, comarca, etc.)
                        3. Redigir peças processuais de alta qualidade
                            4. Identificar pontos críticos e urgentes
                                5. Sugerir as próximas ações a serem tomadas

                                    Seja preciso, objetivo e use linguagem jurídica adequada.
                                        Sempre respeite os prazos do CPC (Código de Processo Civil).
                                            Responda sempre em português do Brasil.
                                                """

    def __init__(self, api_key: str, model: str = "claude-opus-4-5"):
              self.client = anthropic.Anthropic(api_key=api_key)
              self.model = model
              logger.info(f"ClaudeAgent inicializado com modelo: {model}")

    def analisar_documento(self, texto_documento: str) -> ProcessoInfo:
              """Analisa um documento processual e extrai informações estruturadas."""
              logger.info("Analisando documento processual...")

        prompt = f"""
                Analise o seguinte documento/andamento processual e extraia as informações
                        em formato JSON estruturado:

                                DOCUMENTO:
                                        {texto_documento}

                                                Retorne um JSON com os campos:
                                                        - numero_processo: string ou null
                                                                - partes: {{"autor": string, "reu": string}} ou null
                                                                        - comarca: string ou null
                                                                                - vara: string ou null
                                                                                        - prazos: lista de {{"descricao": string, "data": string, "dias_restantes": int}}
                                                                                                - tipo_acao: string ou null
                                                                                                        - urgencia: "alta", "media" ou "baixa"
        - proximas_acoes: lista de strings com ações recomendadas
                - resumo: string com resumo do documento

                        Responda APENAS com o JSON, sem texto adicional.
                                """

        response = self.client.messages.create(
                      model=self.model,
                      max_tokens=2000,
                      system=self.SYSTEM_PROMPT,
                      messages=[{"role": "user", "content": prompt}]
        )

        import json
        data = json.loads(response.content[0].text)
        return ProcessoInfo(**data)

    def redigir_peca(self,
                                          tipo_peca: str,
                                          processo_info: ProcessoInfo,
                                          instrucoes_adicionais: str = "") -> str:
                                                    """Redige uma peça jurídica baseada nas informações do processo."""
                                                    logger.info(f"Redigindo peça: {tipo_peca}")

        prompt = f"""
                Redija uma {tipo_peca} completa e profissional com base nas seguintes
                        informações processuais:

                                INFORMAÇÕES DO PROCESSO:
                                        {processo_info.model_dump_json(indent=2)}

                                                INSTRUÇÕES ADICIONAIS DO ADVOGADO:
                                                        {instrucoes_adicionais}

                                                                A peça deve seguir:
                                                                        - Estrutura jurídica brasileira padrão
                                                                                - Linguagem formal e técnica
                                                                                        - Fundamentação legal adequada
                                                                                                - Pedidos claros e objetivos
                                                                                                        """

        response = self.client.messages.create(
                      model=self.model,
                      max_tokens=8000,
                      system=self.SYSTEM_PROMPT,
                      messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def resumir_andamentos(self, andamentos: list[str]) -> str:
              """Resume múltiplos andamentos processuais de forma clara."""
              andamentos_texto = "\n".join(f"- {a}" for a in andamentos)

        response = self.client.messages.create(
                      model=self.model,
                      max_tokens=1000,
                      system=self.SYSTEM_PROMPT,
                      messages=[{
                                        "role": "user",
                                        "content": f"Resuma os seguintes andamentos processuais de forma clara e objetiva:\n{andamentos_texto}"
                      }]
        )

        return response.content[0].text
