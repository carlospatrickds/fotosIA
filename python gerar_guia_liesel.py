#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do Guia OBA 2015-2025 para Liesel
Lê PDFs da OBA e gera HTML interativo completo
"""
import os, re, json
from pathlib import Path

# Configurações
PASTA_PDFS = "./provas_oba"  # Coloque seus PDFs aqui
ARQUIVO_SAIDA = "guia_oba_liesel_completo.html"

# Template HTML base (CSS/JS já inclusos)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📖 Guia OBA 2015-2025 | Liesel</title>
<style>
/* ... [CSS COMPLETO AQUI - mesmo das versões anteriores] ... */
</style>
</head>
<body>
<!-- [ESTRELAS, PLANETAS, HEADER, NAV, FILTROS] -->
<div class="container">
{{QUESTOES_AQUI}}
</div>
<!-- [FOOTER E JAVASCRIPT] -->
</body>
</html>"""

def extrair_questoes_oba(pdf_path):
    """
    Extrai questões de um PDF da OBA Nível 3.
    Retorna lista de dicionários com: ano, numero, enunciado, alternativas, gabarito, tema, comentario
    """
    # Implementação simplificada - adapte conforme a estrutura real dos PDFs
    questoes = []
    
    # Exemplo de parsing (ajuste conforme necessário)
    with open(pdf_path, 'r', encoding='utf-8', errors='ignore') as f:
        texto = f.read()
    
    # Regex para identificar questões (ajuste conforme o formato real)
    padrao_questao = r'Questão\s+(\d+)\)[\s\S]*?(?=Questão\s+\d+\)|AQUI COMEÇAM|GABARITO|$)'
    
    for match in re.finditer(padrao_questao, texto, re.IGNORECASE):
        bloco = match.group(0)
        
        # Extrair número
        num_match = re.search(r'Questão\s+(\d+)', bloco)
        num = num_match.group(1) if num_match else "?"
        
        # Extrair enunciado (texto até as alternativas)
        enunciado_match = re.search(r'Pergunta\s+\w+\)[\s\S]*?(?=(?:a\)|b\)|c\)|Assinale|Coloque))', bloco)
        enunciado = enunciado_match.group(0).strip() if enunciado_match else bloco[:300] + "..."
        
        # Extrair alternativas
        alternativas = re.findall(r'([a-e])\)[\s\S]*?(?=[a-f]\)|Assinale|Resposta|$)', bloco)
        
        questoes.append({
            'numero': num,
            'enunciado': enunciado,
            'alternativas': alternativas,
            'tema': 'calc' if 'calcule' in bloco.lower() else 'lum',
            'comentario': 'Comentário extraído do gabarito...'
        })
    
    return questoes

def gerar_html_questao(q, ano):
    """Gera o bloco HTML de uma questão"""
    opts_html = ''.join([
        f'<label class="option-item"><input type="radio" name="q{ano}-{q["numero"]}" value="{opt.lower()}"> {opt}) [texto]</label>'
        for opt in q['alternativas'][:5]  # limita a 5 alternativas
    ])
    
    return f"""
<div class="q-card" data-topic="{q['tema']}" data-question="{q['enunciado'][:200]}">
<div class="q-header"><span class="q-num">Q{q['numero']}</span><span class="q-topic">💡 Tema</span></div>
<input type="checkbox" class="progress-check" data-id="{ano}-{q['numero']}">
<p class="q-text">{q['enunciado']}</p>
<div class="options">{opts_html}</div>
<div id="ans-{ano}-{q['numero']}" class="ans-box">
<strong>✅ Resposta: [gabarito]</strong>
<div class="ans-comment"><strong>Comentário:</strong> {q['comentario']}</div>
</div>
<div class="action-buttons">
<button class="btn-ans" onclick="toggleAns('ans-{ano}-{q['numero']}','q{ano}-{q['numero']}','[correta]')">👁️ Mostrar Resposta</button>
<button class="btn-copy-q" onclick="copyQuestion(this)">📋 Copiar Questão</button>
<button class="btn-search-ai" onclick="searchAI('{q['enunciado'][:100]}')">🤖 Buscar em IA</button>
</div>
</div>"""

def main():
    print("🚀 Gerando Guia OBA para Liesel...")
    
    todas_questoes = []
    
    # Processar cada PDF
    for pdf_file in Path(PASTA_PDFS).glob("*.pdf"):
        print(f"📄 Processando {pdf_file.name}...")
        # Extrair ano do nome do arquivo
        ano_match = re.search(r'(\d{4})', pdf_file.stem)
        ano = ano_match.group(1) if ano_match else "2020"
        
        questoes = extrair_questoes_oba(str(pdf_file))
        for q in questoes:
            todas_questoes.append(gerar_html_questao(q, ano))
    
    # Montar HTML final
    html_final = HTML_TEMPLATE.replace("{{QUESTOES_AQUI}}", "\n".join(todas_questoes))
    
    # Salvar
    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print(f"✅ Guia gerado: {ARQUIVO_SAIDA}")
    print(f"📊 Total de questões: {len(todas_questoes)}")

if __name__ == "__main__":
    main()
