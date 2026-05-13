"""
  Módulo de análise e extração de dados de documentos jurídicos.

  Suporta OCR de imagens e PDFs, extraindo informações estruturadas
    como número do processo, partes, prazos e tipo de demanda.
      """

      import re
      import io
      import logging
      from dataclasses import dataclass, field
        from typing import Optional
        from pathlib import Path

        import anthropic
        import pytesseract
        from PIL import Image
        import fitz  # PyMuPDF

        logger = logging.getLogger(__name__)


        @dataclass
        class ProcessoInfo:
            """Informações extraídas de um documento processual."""
            numero_processo: Optional[str] = None
                  tribunal: Optional[str] = None
                        vara: Optional[str] = None
                              comarca: Optional[str] = None
                                    autor: Optional[str] = None
                                          reu: Optional[str] = None
                                                tipo_acao: Optional[str] = None
                                                      data_distribuicao: Optional[str] = None
                                                            prazos: list[dict] = field(default_factory=list)
                                                                  intimacoes: list[str] = field(default_factory=list)
                                                                        urgente: bool = False
                                                                              texto_completo: str = ""
                                                                                    confianca: float = 0.0


                                                                                      class DocumentParser:
                                                                                          """
                                                                                          Analisa documentos jurídicos usando OCR e IA (Claude).

                                                                                          Suporta:
    - Imagens (JPG, PNG, TIFF)
          - PDFs (nativos e escaneados)
          - Andamentos processuais
          - Intimações e despachos
          """

          # Padrão CNJ para número de processo: NNNNNNN-DD.AAAA.J.TT.OOOO
                PADRAO_NUMERO_PROCESSO = re.compile(
                    r'\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}'
                )

                TIPOS_ACAO = [
                    "ação de cobrança", "ação trabalhista", "habeas corpus",
                    "mandado de segurança", "ação civil pública", "execução fiscal",
                    "inventário", "divórcio", "guarda", "alimentos",
                    "indenização por danos morais", "revisional de aluguel",
                ]

                def __init__(self, anthropic_client: Optional[anthropic.Anthropic] = None):
        """
                  Inicializa o parser.

                  Args:
            anthropic_client: Cliente Anthropic (opcional, usa ANTHROPIC_API_KEY do env)
                      """
                      self.client = anthropic_client or anthropic.Anthropic()

                  def parse_imagem(self, caminho: str | Path) -> ProcessoInfo:
        """
                  Extrai informações de uma imagem de documento jurídico.

                  Args:
            caminho: Caminho para a imagem (JPG, PNG, TIFF)

                      Returns:
            ProcessoInfo com os dados extraídos
                      """
                      caminho = Path(caminho)
                      logger.info(f"Processando imagem: {caminho.name}")

                      # OCR com Tesseract
                      imagem = Image.open(caminho)
                      texto_ocr = pytesseract.image_to_string(imagem, lang='por')
                      logger.debug(f"OCR concluído: {len(texto_ocr)} caracteres")

                      return self._analisar_com_claude(texto_ocr)

                  def parse_pdf(self, caminho: str | Path) -> ProcessoInfo:
        """
                  Extrai informações de um PDF (nativo ou escaneado).

                  Args:
            caminho: Caminho para o arquivo PDF

                      Returns:
            ProcessoInfo com os dados extraídos
                      """
                      caminho = Path(caminho)
                      logger.info(f"Processando PDF: {caminho.name}")

                      doc = fitz.open(str(caminho))
                      texto_completo = []

                      for num_pagina, pagina in enumerate(doc):
                          # Tenta extrair texto nativo
                          texto = pagina.get_text()

                          if not texto.strip():
                              # PDF escaneado — usa OCR
                              logger.debug(f"Página {num_pagina + 1} sem texto nativo, usando OCR")
                              mat = fitz.Matrix(2, 2)  # Resolução 2x para melhor OCR
                              clip = pagina.get_pixmap(matrix=mat)
                              img_bytes = clip.tobytes("png")
                              imagem = Image.open(io.BytesIO(img_bytes))
                              texto = pytesseract.image_to_string(imagem, lang='por')

                          texto_completo.append(texto)

                      doc.close()
                      texto_final = "\n\n".join(texto_completo)
                      logger.debug(f"PDF processado: {len(texto_final)} caracteres")

                      return self._analisar_com_claude(texto_final)

                  def parse_texto(self, texto: str) -> ProcessoInfo:
        """
                  Extrai informações de texto já processado.

                  Args:
            texto: Texto do documento jurídico

                      Returns:
                          ProcessoInfo com os dados extraídos
                      """
                      return self._analisar_com_claude(texto)

                  def _analisar_com_claude(self, texto: str) -> ProcessoInfo:
        """
                  Usa Claude para análise semântica do texto jurídico.

                  Args:
                      texto: Texto extraído do documento

                                Returns:
                                    ProcessoInfo com os dados estruturados
                                """
                                # Pré-extração por regex para número do processo
                                numeros_encontrados = self.PADRAO_NUMERO_PROCESSO.findall(texto)
                                numero_processo_regex = numeros_encontrados[0] if numeros_encontrados else None

                                prompt = f"""Analise o seguinte texto de documento jurídico brasileiro e extraia as informações estruturadas.

                        TEXTO DO DOCUMENTO:
                      {texto[:4000]}  # Limite para evitar tokens excessivos

                        Extraia e retorne em formato JSON:
{{
    "numero_processo": "número no formato CNJ (NNNNNNN-DD.AAAA.J.TT.OOOO) ou null",
    "tribunal": "nome do tribunal ou null",
    "vara": "número/nome da vara ou null",
    "comarca": "cidade/comarca ou null",
    "autor": "nome do autor/requerente ou null",
    "reu": "nome do réu/requerido ou null",
    "tipo_acao": "tipo da ação ou demanda ou null",
    "data_distribuicao": "data no formato YYYY-MM-DD ou null",
    "prazos": [
      {{
              "descricao": "descrição do prazo",
              "data_vencimento": "YYYY-MM-DD ou null",
              "dias_restantes": número ou null,
              "tipo": "contestacao|recurso|manifestacao|audiencia|outro"
      }}
        ],
        "intimacoes": ["lista de intimações ou determinações encontradas"],
            "urgente": true/false,
    "confianca": 0.0 a 1.0
}}

Responda APENAS com o JSON, sem texto adicional."""

          try:
              resposta = self.client.messages.create(
                  model="claude-opus-4-5",
                  max_tokens=1024,
                  messages=[{"role": "user", "content": prompt}]
              )

              import json
              dados = json.loads(resposta.content[0].text)

              # Usa regex como fallback para número do processo
              if not dados.get("numero_processo") and numero_processo_regex:
                  dados["numero_processo"] = numero_processo_regex

              return ProcessoInfo(
                  numero_processo=dados.get("numero_processo"),
                  tribunal=dados.get("tribunal"),
                  vara=dados.get("vara"),
                  comarca=dados.get("comarca"),
                  autor=dados.get("autor"),
                  reu=dados.get("reu"),
                  tipo_acao=dados.get("tipo_acao"),
                  data_distribuicao=dados.get("data_distribuicao"),
                  prazos=dados.get("prazos", []),
                  intimacoes=dados.get("intimacoes", []),
                  urgente=dados.get("urgente", False),
                  texto_completo=texto,
                  confianca=dados.get("confianca", 0.5),
              )

          except Exception as e:
              logger.error(f"Erro ao analisar com Claude: {e}")
              # Retorna o que foi extraído por regex
              return ProcessoInfo(
                  numero_processo=numero_processo_regex,
                  texto_completo=texto,
                  confianca=0.1,
              )

      def extrair_numero_processo(self, texto: str) -> Optional[str]:
        """
                  Extrai número do processo no padrão CNJ do texto.

                  Args:
                      texto: Texto para busca

                  Returns:
            Número do processo ou None
                      """
                      match = self.PADRAO_NUMERO_PROCESSO.search(texto)
                      return match.group(0) if match else None
