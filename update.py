from pathlib import Path
import re, json
p=Path('/mnt/data/v5work/projekti.html')
s=p.read_text()
# Add richer gallery CSS overrides before </style>
css='''\n    .stage{margin-top:68px}.stage-head{max-width:900px;margin-bottom:28px}.stage-head h3{font-size:clamp(1.7rem,3vw,2.35rem);line-height:1.2;margin:0 0 10px}.stage-head p{margin:0;color:#626262;max-width:850px}.gallery.clean{grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:28px}.gallery.clean figure{grid-column:span 1!important;background:#fff;cursor:zoom-in;border:1px solid #e7e7e3;box-shadow:0 8px 28px rgba(0,0,0,.055);display:flex;flex-direction:column}.gallery.clean figure:nth-child(1){grid-column:span 2!important}.gallery.clean img,.gallery.clean figure:nth-child(1) img{height:390px;object-fit:cover;opacity:1;transition:transform .45s ease}.gallery.clean figure:hover img{transform:scale(1.025)}.gallery.clean .caption{position:static;padding:17px 18px 4px;background:#fff;color:#151515;font-size:1.02rem;line-height:1.35}.gallery.clean .photo-text{padding:0 18px 20px;color:#666;font-size:.92rem;line-height:1.65}.gallery.clean .photo-text p{margin:7px 0 0}.stage-copy{margin-top:28px;background:#fff;border-left:4px solid var(--gold);padding:24px 28px;box-shadow:0 8px 28px rgba(0,0,0,.045)}.stage-copy h4{margin:0 0 8px;font-size:1.3rem}.stage-copy p{margin:0;color:#5f5f5f}.project-intro-note{margin-top:55px;max-width:900px}.project-intro-note h3{font-size:1.75rem;margin:0 0 10px}.project-intro-note p{color:#5c5c5c}.lightbox img{max-width:min(1200px,94vw);max-height:78vh}.lightbox-caption{bottom:14px;line-height:1.45}\n    @media(max-width:900px){.gallery.clean{grid-template-columns:repeat(2,minmax(0,1fr))}.gallery.clean figure:nth-child(1){grid-column:span 2!important}.gallery.clean img,.gallery.clean figure:nth-child(1) img{height:360px}}\n    @media(max-width:600px){.gallery.clean{grid-template-columns:1fr;gap:16px}.gallery.clean figure:nth-child(1){grid-column:span 1!important}.gallery.clean img,.gallery.clean figure:nth-child(1) img{height:330px}.stage{margin-top:48px}.stage-copy{padding:20px 21px}}\n'''
s=s.replace('  </style>\n  <script type="application/ld+json">',''+css+'  </style>\n  <script type="application/ld+json">',1)

cards = {
'vanjski': [
('assets/projekt-stambeni-naslovna.png','Stambeni objekt – pregled projekta','Širi prezentacijski pogled na stambeni objekt u fazi izgradnje, s vidljivom nosivom konstrukcijom, građevinskim otvorima, balkonima i vanjskom stolarijom.','Stambena gradnja i organizacija izvedbe'),
('assets/projekt-stambeni-01.jpg','Roh-bau i nosiva konstrukcija','Fotografija prikazuje objekt u roh-bau fazi, s armiranobetonskim elementima, zidovima i međukatnim konstrukcijama koji definiraju osnovnu geometriju budućeg prostora.','Roh-bau radovi i konstrukcija'),
('assets/projekt-stambeni-02.jpg','Instalacijske trase na vanjskim zidovima','Na bočnoj fasadi vidljive su pripremljene instalacijske trase i izvodi koji se izvode i usklađuju prije završnog zatvaranja zidnih slojeva.','Priprema instalacija'),
('assets/projekt-stambeni-03.jpg','Balkoni, otvori i vanjska stolarija','Pogled na etaže objekta pokazuje izvedene balkonske ploče, građevinske otvore i ugrađenu vanjsku stolariju tijekom srednje faze gradnje.','Građevinski otvori i stolarija'),
('assets/projekt-stambeni-04.jpg','Hidroizolacijska zaštita donjih zona','Na donjim dijelovima objekta vidljiva je izvedena zaštitna obrada uz zonu kontakta konstrukcije sa zemljom, kao dio pripreme za daljnje slojeve zaštite objekta.','Hidroizolacijski radovi'),
('assets/projekt-stambeni-05.jpg','Vanjska stolarija i građevinski detalji','Detalj pročelja s ugrađenim prozorima i vratima pokazuje kako se vanjska stolarija uklapa u građevinske otvore prije završne obrade fasadnih površina.','Vanjska stolarija'),
('assets/projekt-stambeni-06.jpg','Gradilište i širi pogled na objekt','Širi pogled prikazuje odnos objekta prema terenu, pristup gradilištu i organizaciju prostora tijekom izvođenja građevinskih radova.','Organizacija gradilišta'),
],
'instalacije': [
('assets/projekt-stambeni/07-elektroinstalacije-pregradni-zid.jpg','Elektroinstalacije u pregradnom zidu','Vidljivi su metalna podkonstrukcija pregradnog zida i crvene instalacijske cijevi s pripremljenim mjestima za buduće elektro elemente.','Elektroinstalacijska priprema'),
('assets/projekt-stambeni/10-elektroizvodi-strop.jpg','Priprema elektroizvoda u prostoru','Na stropu i zidovima vidljivi su pripremljeni izvodi instalacija, postavljeni prije završnog bojanja i ugradnje završne opreme.','Elektroinstalacije'),
('assets/projekt-stambeni/14-elektroizvodi-zid.jpg','Zidni izvodi za električne instalacije','Fotografija prikazuje ugrađene instalacijske kutije i izvode u obrađenom zidu, spremne za završnu montažu prekidača, utičnica i druge opreme.','Zidni elektroizvodi'),
('assets/projekt-stambeni/17-vodovodne-instalacije.jpg','Priprema instalacijskih vodova','U prostoru su vidljivi vodovi uz zid i pod te pripremljene trase koje se uklapaju u daljnje zatvaranje i završnu obradu instalacijskih zona.','Instalacijska priprema'),
('assets/projekt-stambeni/18-elektroinstalacije-soba.jpg','Elektroinstalacije u stambenoj jedinici','Razvedeni vodovi i pripremljene pozicije pokazuju fazu u kojoj se instalacije usklađuju s rasporedom prostorija i budućom završnom opremom.','Elektroinstalacije u interijeru'),
('assets/projekt-stambeni/20-vodovodne-cijevi.jpg','Plave instalacijske cijevi i vertikala','Fotografija prikazuje plave instalacijske cijevi, spojeve i vertikalni vod uz zid. Riječ je o fazi u kojoj se instalacije pripremaju prije konačnog zatvaranja obloga.','Vodovodne instalacije'),
],
'interijer': [
('assets/projekt-stambeni/08-stolarija-pogled.jpg','Velike staklene površine i pogled iz interijera','Velike staklene stijene otvaraju prostor prema okolišu, dok završetak zidova i podova još čeka naredne faze unutarnje obrade.','Vanjska stolarija'),
('assets/projekt-stambeni/09-zidovi-priprema.jpg','Priprema zidnih površina','Prikaz rada na zidnoj površini prije završne obrade. Ravne i pripremljene površine stvaraju osnovu za sljedeće slojeve i završnu dekorativnu obradu.','Priprema zidova'),
('assets/projekt-stambeni/11-boravak-stolarija.jpg','Dnevni prostor s ugrađenom stolarijom','Prostor s velikom staklenom površinom i izlazom prema vanjskoj terasi. Fotografija prikazuje objekt u fazi prije završnog uređenja interijera.','Stambeni interijer'),
('assets/projekt-stambeni/12-kutna-stolarija.jpg','Kutna stolarija i prirodno osvjetljenje','Kutni otvor s velikim staklenim površinama pokazuje način na koji je prostor povezan s vanjskim okolišem i prirodnim svjetlom.','Stolarija i otvori'),
('assets/projekt-stambeni/13-prostor-sa-stolarijom.jpg','Unutarnja obrada uz vanjsku stolariju','U prostoru su vidljivi ugrađeni prozorski elementi, obrađeni zidovi i podloga spremna za nastavak završnih radova.','Završna priprema interijera'),
('assets/projekt-stambeni/15-zavrsna-priprema-zidova.jpg','Zidovi prije završnog bojanja','Površine su pripremljene za završne slojeve, dok se na pojedinim mjestima još vide tragovi prethodnih radnih faza.','Završna obrada zidova'),
('assets/projekt-stambeni/16-unutarnja-stolarija.jpg','Unutarnji otvor i stolarija','Detalj unutarnjeg prostora s ugrađenim vratima i završno obrađenim otvorom. Ovakve faze prethode finalnom uređenju prostorija.','Unutarnja stolarija'),
('assets/projekt-stambeni/19-stepeniste.jpg','Betonsko stubište','Izvedeno unutarnje stubište povezuje etaže objekta i predstavlja osnovu za kasniju završnu oblogu stepenica i uređenje stubišnog prostora.','Građevinski radovi'),
('assets/projekt-stambeni/21-suhomontazni-radovi.jpg','Suhomontažna podkonstrukcija i obloge','Metalna podkonstrukcija i postavljene gipskartonske ploče vidljive su u fazi oblikovanja unutarnjih pregradnih i obložnih površina.','Suhomontažni radovi'),
]
}

def gallery_html(items, label):
    out=[f'<div class="gallery clean" aria-label="{label}">']
    for src,title,desc,tag in items:
        out.append(f'''<figure data-lightbox data-caption="{title}. {desc}"><img src="{src}" alt="{title} – Pro in mont jedan j.d.o.o." loading="lazy"><figcaption class="caption">{title}</figcaption><div class="photo-text"><p>{desc}</p></div></figure>''')
    out.append('</div>')
    return '\n'.join(out)

stages='''<section class="stage" aria-labelledby="stage-vanjski"><div class="stage-head"><div class="eyebrow">Faza 01</div><h3 id="stage-vanjski">Vanjski radovi, konstrukcija i zaštita objekta</h3><p>Prvi dio galerije dokumentira vanjski izgled objekta tijekom izgradnje. Vidljivi su nosivi elementi, zidanje, balkoni, građevinski otvori, vanjska stolarija i zaštitna obrada donjih zona objekta. Fotografije su snimljene u različitim trenucima gradnje kako bi se jasno vidio napredak projekta.</p></div>'''+gallery_html(cards['vanjski'],'Galerija vanjskih građevinskih radova i konstrukcije')+'''<div class="stage-copy"><h4>Kako se faze nadovezuju</h4><p>Nosiva konstrukcija i zidovi stvaraju osnovu objekta, nakon čega slijede zatvaranje otvora, zaštita kritičnih zona, ugradnja stolarije i priprema za instalaterske i završne radove. Dobra koordinacija redoslijeda važna je kako bi se izbjeglo nepotrebno vraćanje na već završene površine.</p></div></section>'''

stages+='''<section class="stage" aria-labelledby="stage-instalacije"><div class="stage-head"><div class="eyebrow">Faza 02</div><h3 id="stage-instalacije">Elektro i vodovodne instalacije</h3><p>Drugi dio galerije prikazuje unutarnje instalacijske faze. Na fotografijama se vide elektroinstalacijske cijevi, zidni i stropni izvodi, pripremljene instalacijske kutije te plave cijevi i vertikale. Ove se instalacije izvode prema projektu i usklađuju s rasporedom budućih prostorija i opreme.</p></div>'''+gallery_html(cards['instalacije'],'Galerija elektroinstalacija i vodovodnih instalacija')+'''<div class="stage-copy"><h4>Instalacije prije zatvaranja zidova</h4><p>Dok su instalacije otvoreno vidljive, moguće je provjeriti njihove trase, položaje izvoda i međusobnu koordinaciju s pregradama, stolarijom i drugim građevinskim elementima. Nakon provjere slijedi zatvaranje obloga i priprema za završnu montažu opreme.</p></div></section>'''

stages+='''<section class="stage" aria-labelledby="stage-interijer"><div class="stage-head"><div class="eyebrow">Faza 03</div><h3 id="stage-interijer">Unutarnji radovi, stolarija i priprema za završno uređenje</h3><p>Treća skupina fotografija prikazuje unutarnje prostore u prijelaznoj fazi između grubih radova i završnog uređenja. Vidljivi su veliki stakleni otvori, pripremljeni zidovi, unutarnja stolarija, stubište te suhomontažne pregrade i obloge.</p></div>'''+gallery_html(cards['interijer'],'Galerija unutarnjih građevinskih i suhomontažnih radova')+'''<div class="stage-copy"><h4>Od gradilišta do gotovog interijera</h4><p>Ovakva faza predstavlja važnu poveznicu između građevinskih i završnih radova. Nakon pripreme zidova, podova, stolarije i instalacija slijede završne obloge, bojanje, montaža sanitarne i elektro opreme te uređenje prostora prema projektu i zahtjevima investitora.</p></div></section>'''

start=s.index('<div class="gallery" aria-label="Fotogalerija stambenog projekta">')
end=s.index('<div class="details">', start)
s=s[:start]+stages+'\n\n        '+s[end:]

# Add an overall project text section before the next section begins
marker='''        <div class="details">\n          <article class="detail-card"><h3>Hidroizolacija</h3>'''
# Existing details retained. Add project intro note just before it.
note='''        <div class="project-intro-note"><h3>Detaljna dokumentacija faza gradnje</h3><p>Galerija je proširena kako bi prikazala projekt iz više perspektiva – od vanjske konstrukcije i zaštite objekta do instalacija, stolarije, suhomontažnih radova i pripreme unutarnjih prostora. Na taj način potencijalni investitor može dobiti realniji uvid u redoslijed i međusobnu povezanost građevinskih faza. Opisi uz fotografije odnose se na ono što je vidljivo na snimkama i služe kao informativni pregled projekta.</p></div>\n\n'''
s=s.replace(marker,note+marker,1)

# Update ImageGallery JSON-LD image list with all project images
all_images=['projekt-stambeni-naslovna.png']+[f'projekt-stambeni-0{i}.jpg' for i in range(1,7)]
all_images += [
'projekt-stambeni/07-elektroinstalacije-pregradni-zid.jpg','projekt-stambeni/08-stolarija-pogled.jpg','projekt-stambeni/09-zidovi-priprema.jpg','projekt-stambeni/10-elektroizvodi-strop.jpg','projekt-stambeni/11-boravak-stolarija.jpg','projekt-stambeni/12-kutna-stolarija.jpg','projekt-stambeni/13-prostor-sa-stolarijom.jpg','projekt-stambeni/14-elektroizvodi-zid.jpg','projekt-stambeni/15-zavrsna-priprema-zidova.jpg','projekt-stambeni/16-unutarnja-stolarija.jpg','projekt-stambeni/17-vodovodne-instalacije.jpg','projekt-stambeni/18-elektroinstalacije-soba.jpg','projekt-stambeni/19-stepeniste.jpg','projekt-stambeni/20-vodovodne-cijevi.jpg','projekt-stambeni/21-suhomontazni-radovi.jpg']
imgjson=json.dumps(['https://proinmont-jedan.com.hr/assets/'+x for x in all_images],ensure_ascii=False,separators=(',',':'))
s=re.sub(r'("@type":"ImageGallery","name":"Galerija projekta stambenog objekta","image":)\[[^\]]*\]', r'\1'+imgjson, s, count=1)
p.write_text(s)
print('updated', len(all_images), 'images')
