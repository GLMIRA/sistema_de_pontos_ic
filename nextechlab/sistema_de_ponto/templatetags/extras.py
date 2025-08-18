from sistema_de_ponto.models import RegistroPonto, User
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from collections import defaultdict
from datetime import date, datetime
from django import template
import json

register = template.Library()


@register.filter
def get_item(mapping, key):
    """
    Retorna mapping[key] de forma tolerante:
      - tenta mapping.get(key)
      - se key for string 'YYYY-MM-DD' tenta converter para date
      - se ainda não achar, tenta o contrário (key date -> str)
    """
    try:
        # Se for um objeto com .get (dicionário), tenta direto
        if hasattr(mapping, "get"):
            # tenta direto
            val = mapping.get(key)
            if val is not None:
                return val
        # tenta indexador
        try:
            return mapping[key]
        except Exception:
            pass

        # Se key é string no formato YYYY-MM-DD, tenta converter para date
        if isinstance(key, str):
            try:
                kdate = datetime.strptime(key, "%Y-%m-%d").date()
                if hasattr(mapping, "get"):
                    return mapping.get(kdate)
                return mapping.get(kdate) if hasattr(mapping, "get") else mapping[kdate]
            except Exception:
                pass

        # Se key é date e mapeamento tem chaves string YYYY-MM-DD
        if isinstance(key, (date, datetime)):
            kstr = key.strftime("%Y-%m-%d")
            try:
                return mapping.get(kstr) if hasattr(mapping, "get") else mapping[kstr]
            except Exception:
                pass

    except Exception:
        pass

    return None


@register.filter
def hours_to_hm(total_hours):
    """Formata float de horas para 'Xh Ym' (ex.: 2.5 -> '2h 30m')."""
    try:
        if total_hours is None:
            return "0h 0m"
        # aceitar string numérica também
        th = float(total_hours)
        horas = int(th)
        minutos = int(round((th - horas) * 60))
        return f"{horas}h {minutos}m"
    except Exception:
        return str(total_hours)


@register.filter
def date_to_key(value):
    """Converte date/datetime para 'YYYY-MM-DD' (útil para ids e valores de select)."""
    try:
        if hasattr(value, "date"):
            value = value.date()
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        # se for string já no formato, retorna como está
        return str(value)
    except Exception:
        return str(value)


@register.filter
def badge_class(tipo):
    """Retorna uma classe CSS baseada no tipo (entrada/saida)."""
    try:
        t = (tipo or "").lower()
        if t == "entrada":
            return "badge-success"
        if t == "saida" or t == "saída":
            return "badge-danger"
    except Exception:
        pass
    return "badge-secondary"


@register.simple_tag
def get_todos_registros():
    """
    Retorna todos os registros de ponto, ordenados por data/hora desc.
    """
    return RegistroPonto.objects.select_related("aluno").order_by("-data_hora")


@register.simple_tag
def get_total_alunos():
    """
    Retorna total de alunos únicos que têm registros.
    """
    aluno_ids = RegistroPonto.objects.values_list("aluno_id", flat=True).distinct()
    return len(aluno_ids)


@register.simple_tag
def get_total_horas_geral():
    """
    Calcula total de horas batidas por todos os alunos.
    """
    registros = RegistroPonto.objects.select_related("aluno").order_by(
        "aluno", "data_hora"
    )
    por_aluno = defaultdict(list)
    total_horas = 0.0

    for r in registros:
        por_aluno[r.aluno].append(r)

    for aluno, regs in por_aluno.items():
        entradas = [r.data_hora for r in regs if r.tipo == "entrada"]
        saidas = [r.data_hora for r in regs if r.tipo == "saida"]
        for e, s in zip(entradas, saidas):
            total_horas += (s - e).total_seconds() / 3600.0

    return round(total_horas, 2)


register.simple_tag


def get_total_horas_por_aluno(aluno):
    """
    Calcula total de horas batidas por um aluno específico.
    """
    registros = RegistroPonto.objects.filter(aluno=aluno).order_by("data_hora")
    entradas = [r.data_hora for r in registros if r.tipo == "entrada"]
    saidas = [r.data_hora for r in registros if r.tipo == "saida"]

    total_horas = 0.0
    for e, s in zip(entradas, saidas):
        total_horas += (s - e).total_seconds() / 3600.0

    return round(total_horas, 2)


@register.simple_tag
def get_total_registros_por_aluno(aluno):
    """
    Retorna a quantidade de registros de ponto de um aluno específico.
    """
    return RegistroPonto.objects.filter(aluno=aluno).count()


@register.filter
def to_json(value):
    """
    Converte um valor Python para JSON de forma segura para usar no template.
    """
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except:
        return "{}"


@register.filter
def get_aluno_data(dados_por_aluno, aluno_id):
    """
    Filtro específico para pegar dados do aluno
    """
    try:
        print(f"DEBUG get_aluno_data: Buscando aluno_id '{aluno_id}'")
        print(f"DEBUG get_aluno_data: Tipo dados: {type(dados_por_aluno)}")
        print(
            f"DEBUG get_aluno_data: Chaves: {list(dados_por_aluno.keys()) if hasattr(dados_por_aluno, 'keys') else 'N/A'}"
        )

        if not dados_por_aluno:
            return None

        # Tenta várias formas de acessar
        chave_str = str(aluno_id)

        # Método 1: get com string
        if hasattr(dados_por_aluno, "get"):
            result = dados_por_aluno.get(chave_str)
            if result:
                print(f"DEBUG: Encontrado com get('{chave_str}')")
                return result

        # Método 2: indexação direta
        try:
            result = dados_por_aluno[chave_str]
            print(f"DEBUG: Encontrado com ['{chave_str}']")
            return result
        except:
            pass

        print(f"DEBUG get_aluno_data: Não encontrado para '{chave_str}'")
        return None

    except Exception as e:
        print(f"DEBUG get_aluno_data: Erro: {e}")
        return None


@register.filter
def to_json(value):
    """
    Converte um valor Python para JSON de forma segura para usar no template.
    """
    try:
        return json.dumps(value, ensure_ascii=False, default=str, indent=2)
    except Exception as e:
        print(f"Erro ao converter para JSON: {e}")
        return "{}"
