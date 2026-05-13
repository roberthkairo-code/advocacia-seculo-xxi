"""
Calculadora de prazos processuais conforme o Código de Processo Civil (CPC/2015).

Implementa:
- Contagem de dias úteis e corridos
- Exclusão de feriados nacionais e estaduais
- Suspensão de prazos (recesso forense, Covid, etc.)
- Prazos especiais por tipo de ação
"""

import logging
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class TipoPrazo(str, Enum):
      """Tipos de prazo processual conforme o CPC."""
      UTEIS = "uteis"          # Art. 219 CPC - regra geral
    CORRIDOS = "corridos"    # Exceções expressas na lei
    HORA = "hora"            # Prazos em horas (habeas corpus)


class TipoAto(str, Enum):
      """Tipos de ato processual com seus respectivos prazos."""
      CONTESTACAO = "contestacao"          # 15 dias úteis (art. 335 CPC)
    RECURSO_APELACAO = "apelacao"        # 15 dias úteis (art. 1003 CPC)
    RECURSO_AGRAVO = "agravo"            # 15 dias úteis (art. 1003 CPC)
    RECURSO_EMBARGOS = "embargos"        # 5 dias úteis (art. 1023 CPC)
    RECURSO_ESPECIAL = "resp"            # 15 dias úteis (art. 1003 CPC)
    MANIFESTACAO = "manifestacao"        # 15 dias úteis (regra geral)
    REPLICA = "replica"                  # 15 dias úteis (art. 350 CPC)
    IMPUGNACAO = "impugnacao"            # 15 dias úteis (art. 525 CPC)
    HABEAS_CORPUS = "habeas_corpus"      # Urgente - sem prazo para impetrar
    MANDADO_SEGURANCA = "ms"             # 120 dias corridos (art. 23 Lei 12.016)


# Prazos padrão por tipo de ato (em dias úteis, salvo indicação)
PRAZOS_PADRAO: dict[TipoAto, tuple[int, TipoPrazo]] = {
      TipoAto.CONTESTACAO: (15, TipoPrazo.UTEIS),
      TipoAto.RECURSO_APELACAO: (15, TipoPrazo.UTEIS),
      TipoAto.RECURSO_AGRAVO: (15, TipoPrazo.UTEIS),
      TipoAto.RECURSO_EMBARGOS: (5, TipoPrazo.UTEIS),
      TipoAto.RECURSO_ESPECIAL: (15, TipoPrazo.UTEIS),
      TipoAto.MANIFESTACAO: (15, TipoPrazo.UTEIS),
      TipoAto.REPLICA: (15, TipoPrazo.UTEIS),
      TipoAto.IMPUGNACAO: (15, TipoPrazo.UTEIS),
      TipoAto.MANDADO_SEGURANCA: (120, TipoPrazo.CORRIDOS),
}

# Feriados nacionais fixos (dia, mês)
FERIADOS_NACIONAIS_FIXOS = {
      (1, 1),   # Confraternização Universal
    (21, 4),  # Tiradentes
    (1, 5),   # Dia do Trabalho
    (7, 9),   # Independência do Brasil
    (12, 10), # Nossa Senhora Aparecida
    (2, 11),  # Finados
    (15, 11), # Proclamação da República
    (20, 11), # Consciência Negra (desde 2024 - Lei 14.759/2023)
    (25, 12), # Natal
}

# Recesso forense (art. 220 CPC) - 20/12 a 20/01 (suspensão, não feriado)
INICIO_RECESSO = (20, 12)  # (dia, mês)
FIM_RECESSO = (20, 1)      # (dia, mês)


class DeadlineCalculator:
      """
          Calcula prazos processuais conforme o CPC/2015.

              Exemplo de uso:
                      calc = DeadlineCalculator()
                              vencimento = calc.calcular(
                                          data_inicio=date(2025, 3, 10),
                                                      tipo_ato=TipoAto.CONTESTACAO
                                                              )
                                                                      print(f"Prazo de contestação: {vencimento}")
                                                                          """

    def __init__(self, feriados_estaduais: Optional[list[date]] = None):
              """
                      Inicializa a calculadora.

                              Args:
                                          feriados_estaduais: Lista de feriados estaduais/municipais adicionais
                                                  """
              self.feriados_estaduais = feriados_estaduais or []

    def calcular(
              self,
              data_inicio: date,
              tipo_ato: TipoAto,
              dias_personalizados: Optional[int] = None,
              tipo_prazo_personalizado: Optional[TipoPrazo] = None,
              excluir_recesso: bool = True,
    ) -> date:
              """
                      Calcula a data de vencimento do prazo processual.

                              Args:
                                          data_inicio: Data de início da contagem (intimação/publicação)
                                                      tipo_ato: Tipo do ato processual
                                                                  dias_personalizados: Sobrescreve o número de dias padrão
                                                                              tipo_prazo_personalizado: Sobrescreve o tipo de prazo padrão
                                                                                          excluir_recesso: Se deve excluir o recesso forense (art. 220 CPC)

                                                                                                  Returns:
                                                                                                              Data de vencimento do prazo
                                                                                                              
                                                                                                                      Raises:
                                                                                                                                  ValueError: Se o tipo de ato não tiver prazo definido
                                                                                                                                          """
              if tipo_ato not in PRAZOS_PADRAO:
                            raise ValueError(f"Prazo não definido para o ato: {tipo_ato}")

              dias_padrao, tipo_padrao = PRAZOS_PADRAO[tipo_ato]
              dias = dias_personalizados or dias_padrao
              tipo = tipo_prazo_personalizado or tipo_padrao

        # Art. 224 CPC: prazo começa no primeiro dia útil após a intimação
              data_inicio_contagem = self._proximo_dia_util(data_inicio + timedelta(days=1))

        if tipo == TipoPrazo.CORRIDOS:
                      vencimento = self._calcular_dias_corridos(
                                        data_inicio_contagem, dias, excluir_recesso
                      )
else:
              vencimento = self._calcular_dias_uteis(
                                data_inicio_contagem, dias, excluir_recesso
              )

        # Art. 224 §1 CPC: se vencer em dia não útil, prorroga para o próximo útil
          return self._proximo_dia_util(vencimento)

    def calcular_dias_uteis_restantes(self, data_limite: date) -> int:
              """
                      Calcula quantos dias úteis restam até uma data limite.

                              Args:
                                          data_limite: Data de vencimento do prazo

                                                  Returns:
                                                              Número de dias úteis restantes (negativo se vencido)
                                                                      """
              hoje = date.today()
              if hoje > data_limite:
                            return -self._contar_dias_uteis(data_limite, hoje)
                        return self._contar_dias_uteis(hoje, data_limite)

    def is_dia_util(self, data: date) -> bool:
              """
                      Verifica se uma data é dia útil para fins processuais.

                              Args:
                                          data: Data a verificar

                                                  Returns:
                                                              True se é dia útil, False caso contrário
                                                                      """
        # Final de semana
        if data.weekday() >= 5:  # 5=sábado, 6=domingo
                      return False

        # Feriado nacional fixo
        if (data.day, data.month) in FERIADOS_NACIONAIS_FIXOS:
                      return False

        # Feriados nacionais móveis (Carnaval e Corpus Christi calculados por ano)
        if data in self._feriados_moveis(data.year):
                      return False

        # Feriados estaduais/municipais
        if data in self.feriados_estaduais:
                      return False

        return True

    def esta_em_recesso(self, data: date) -> bool:
              """
                      Verifica se uma data está dentro do recesso forense (art. 220 CPC).

                              Recesso: 20 de dezembro a 20 de janeiro do ano seguinte.

                                      Args:
                                                  data: Data a verificar

                                                          Returns:
                                                                      True se está em período de recesso
                                                                              """
        # Período: 20/12 ao final do ano
        if data.month == 12 and data.day >= 20:
                      return True
                  # Período: 1/1 a 20/1 do ano seguinte
                  if data.month == 1 and data.day <= 20:
                                return True
                            return False

    def _calcular_dias_uteis(
              self, data_inicio: date, dias: int, excluir_recesso: bool
    ) -> date:
              """Conta dias úteis a partir de uma data."""
        data_atual = data_inicio
        dias_contados = 0

        while dias_contados < dias:
                      if excluir_recesso and self.esta_em_recesso(data_atual):
                                        data_atual += timedelta(days=1)
                                        continue
                                    if self.is_dia_util(data_atual):
                                                      dias_contados += 1
                                                  data_atual += timedelta(days=1)

        return data_atual - timedelta(days=1)

    def _calcular_dias_corridos(
              self, data_inicio: date, dias: int, excluir_recesso: bool
    ) -> date:
              """Conta dias corridos a partir de uma data."""
        data_atual = data_inicio
        dias_contados = 0

        while dias_contados < dias:
                      if excluir_recesso and self.esta_em_recesso(data_atual):
                                        data_atual += timedelta(days=1)
                                        continue
                                    dias_contados += 1
            data_atual += timedelta(days=1)

        return data_atual - timedelta(days=1)

    def _contar_dias_uteis(self, data_inicio: date, data_fim: date) -> int:
              """Conta dias úteis entre duas datas."""
        contagem = 0
        data_atual = data_inicio
        while data_atual < data_fim:
                      if self.is_dia_util(data_atual):
                                        contagem += 1
                                    data_atual += timedelta(days=1)
        return contagem

    def _proximo_dia_util(self, data: date) -> date:
              """Retorna o próximo dia útil a partir de uma data (inclusive)."""
        while not self.is_dia_util(data):
                      data += timedelta(days=1)
        return data

    def _feriados_moveis(self, ano: int) -> set[date]:
              """
                      Calcula feriados móveis para um determinado ano.

                              Feriados calculados: Carnaval (2 dias), Sexta-Feira Santa, Corpus Christi.

                                      Args:
                                                  ano: Ano para calcular os feriados

                                                          Returns:
                                                                      Conjunto de datas dos feriados móveis
                                                                              """
        # Algoritmo de Meeus/Jones/Butcher para Páscoa
        a = ano % 19
        b = ano // 100
        c = ano % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        mes_pascoa = (h + l - 7 * m + 114) // 31
        dia_pascoa = ((h + l - 7 * m + 114) % 31) + 1
        pascoa = date(ano, mes_pascoa, dia_pascoa)

        return {
                      pascoa - timedelta(days=48),  # Segunda-feira de Carnaval
            pascoa - timedelta(days=47),  # Terça-feira de Carnaval
            pascoa - timedelta(days=2),   # Sexta-Feira Santa
            pascoa + timedelta(days=60),  # Corpus Christi
        }
