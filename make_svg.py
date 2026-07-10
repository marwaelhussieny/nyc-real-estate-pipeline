svg_content = '''<svg width="100%" viewBox="0 0 680 320" xmlns="http://www.w3.org/2000/svg" role="img">
<title>NYC real estate pipeline architecture</title>
<desc>A CSV source feeds an Airflow-orchestrated pipeline of extract, transform, quality gate, and load steps, which writes into an AWS RDS Postgres database.</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#73726c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>
<rect width="680" height="320" fill="#ffffff"/>
<g fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5">
<rect x="60" y="10" width="130" height="44" rx="8"/>
</g>
<text x="125" y="32" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">NYC DOF CSV</text>
<line x1="125" y1="54" x2="125" y2="113" stroke="#73726c" stroke-width="1.5" marker-end="url(#arrow)"/>
<rect x="40" y="85" width="600" height="112" rx="16" fill="none" stroke="#888780" stroke-width="0.5" stroke-dasharray="4 4"/>
<text x="56" y="100" font-family="sans-serif" font-size="12" fill="#5F5E5A">Airflow weekly schedule</text>
<g fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5">
<rect x="60" y="115" width="130" height="56" rx="8"/>
</g>
<text x="125" y="133" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#04342C">Extract</text>
<text x="125" y="151" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#0F6E56">Reads raw CSV</text>
<line x1="190" y1="143" x2="208" y2="143" stroke="#73726c" stroke-width="1.5" marker-end="url(#arrow)"/>
<g fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5">
<rect x="210" y="115" width="130" height="56" rx="8"/>
</g>
<text x="275" y="133" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#04342C">Transform</text>
<text x="275" y="151" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#0F6E56">Cleans raw CSV</text>
<line x1="340" y1="143" x2="358" y2="143" stroke="#73726c" stroke-width="1.5" marker-end="url(#arrow)"/>
<g fill="#FAEEDA" stroke="#854F0B" stroke-width="0.5">
<rect x="360" y="115" width="130" height="56" rx="8"/>
</g>
<text x="425" y="133" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#412402">Quality gate</text>
<text x="425" y="151" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#854F0B">5 named checks</text>
<line x1="490" y1="143" x2="508" y2="143" stroke="#73726c" stroke-width="1.5" marker-end="url(#arrow)"/>
<g fill="#E1F5EE" stroke="#0F6E56" stroke-width="0.5">
<rect x="510" y="115" width="130" height="56" rx="8"/>
</g>
<text x="575" y="133" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#04342C">Load</text>
<text x="575" y="151" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#0F6E56">Staging swap</text>
<line x1="575" y1="171" x2="565" y2="228" stroke="#73726c" stroke-width="1.5" marker-end="url(#arrow)"/>
<g fill="#F1EFE8" stroke="#5F5E5A" stroke-width="0.5">
<rect x="460" y="230" width="200" height="56" rx="8"/>
</g>
<text x="560" y="248" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="14" font-weight="500" fill="#2C2C2A">AWS RDS Postgres</text>
<text x="560" y="266" text-anchor="middle" dominant-baseline="central" font-family="sans-serif" font-size="12" fill="#5F5E5A">db.t3.micro, via Terraform</text>
</svg>'''
with open('docs/architecture.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)
print("SVG written successfully")