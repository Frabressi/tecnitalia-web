"""Sostituisce il footer statico (fallback no-JS) di tutte le pagine HTML con
il markup di footer.html, rispettando rientro e fine riga di ogni file.
Idempotente: rieseguito senza modifiche a footer.html non cambia nulla.

Uso: uv run python tools/aggiorna-footer.py
"""
import re
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
BLOCCO = re.compile(r'(?m)^([ \t]*)<footer id="contatti" class="footer-sec">.*?</footer>', re.S)


def main():
    righe = (RADICE / 'footer.html').read_text(encoding='utf-8').strip().splitlines()
    pagine = sorted(RADICE.glob('*.html')) + sorted(RADICE.glob('news/*.html')) + sorted(RADICE.glob('progetti/*.html'))
    cambiate = trovate = 0
    for p in pagine:
        if p.name == 'footer.html':
            continue
        testo = p.read_bytes().decode('utf-8')
        if not BLOCCO.search(testo):
            continue
        trovate += 1
        eol = '\r\n' if '\r\n' in testo else '\n'

        def sostituisci(m):
            rientro = m.group(1)
            return eol.join((rientro + r) if r.strip() else '' for r in righe)

        nuovo = BLOCCO.sub(sostituisci, testo)
        if nuovo != testo:
            p.write_bytes(nuovo.encode('utf-8'))
            cambiate += 1
    print(f'Pagine con footer: {trovate}, aggiornate: {cambiate}')


if __name__ == '__main__':
    main()
