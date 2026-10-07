# Racionalne funkcije – kratek pregled za učenje

Pregled zajema gimnazijsko snov: definicijo in lastnosti racionalnih funkcij, ničle in pole, asimptote, skiciranje grafov, enačbe, neenačbe ter uporabo v nalogah. Snov je povzeta po poglavju »Racionalna funkcija« v učnem načrtu za matematiko.

## 1. Kaj je racionalna funkcija?

Racionalna funkcija je količnik dveh polinomov:
\[
f(x)=\frac{P(x)}{Q(x)},\qquad Q(x)\ne0.
\]
Definicijsko območje dobimo tako, da iz realnih števil izločimo vse ničle imenovalca $Q(x)$. Polinomske funkcije in potenčne funkcije z negativnim celim eksponentom so posebni primeri racionalnih funkcij.

**Pomembno:** ulomke krajšamo šele po razcepu na faktorje. Krajšanje ne vrne izločenih vrednosti v definicijsko območje.

### Ničle, poli in luknje

- **Ničle:** rešimo $P(x)=0$, vendar preverimo, da ta vrednost ni izločena iz definicijskega območja.
- **Poli:** ničle imenovalca, ki po krajšanju še vedno ostanejo v imenovalcu. Tam je navadno navpična asimptota; večkratna ničla določa stopnjo pola.
- **Luknja:** če se isti faktor v števcu in imenovalcu pokrajša, ostane ta $x$ kljub temu izločen. Ordinato luknje dobimo tako, da izločeno vrednost vstavimo v poenostavljeni predpis.

**Zgled:**
\[
g(x)=\frac{x^2-4}{x^2-x-2}=\frac{(x-2)(x+2)}{(x-2)(x+1)}=\frac{x+2}{x+1},
\]
pri čemer sta $x=-1$ in $x=2$ izločeni. Pri $x=-1$ je pol, pri $x=2$ pa luknja z ordinato $\frac{2+2}{2+1}=\frac43$. Torej je $D_g=\mathbb R\setminus\{-1,2\}$ in luknja je $\left(2,\frac43\right)$.

## 2. Asimptote

Asimptota je premica, h kateri se graf približuje.

- **Navpična asimptota:** pri $x=a$, kadar imenovalec postane nič, števec pa po krajšanju ni nič. Točka $a$ je pol.
- **Vodoravna asimptota:** po krajšanju skupnih faktorjev primerjamo stopnji polinomov:
  - če je $\deg P<\deg Q$, je $y=0$;
  - če sta stopnji enaki, je $y=$ količnik vodilnih koeficientov.
- **Poševna asimptota:** če je stopnja števca za 1 večja od stopnje imenovalca, delimo polinoma. Količnik je enačba poševne asimptote.

Racionalno funkcijo z linearnim števcem in imenovalcem lahko po preoblikovanju zapišemo v obliki
\[
f(x)=q+\frac{k}{x-p},\qquad k\ne0,
\]
kjer so $p,q,k$ konstante; $x=p$ je navpična, $y=q$ pa vodoravna asimptota.

**Zgled:**
\[
f(x)=\frac{2x+1}{x-2}=2+\frac5{x-2}.
\]
Asimptoti sta $x=2$ in $y=2$; ničla je $x=-\frac12$, presečišče z osjo $y$ pa $f(0)=-\frac12$.

## 3. Kako analiziramo in skiciramo graf?

Za pregledno skico sledi tem korakom:

1. Razstavi števec in imenovalec na faktorje.
2. Določi definicijsko območje in morebitne izločene vrednosti.
3. Poenostavi ulomek; označi ničle, pole in luknje.
4. Določi presečišča z osema: ničle dobimo iz $f(x)=0$, presečišče z osjo $y$ pa z izračunom $f(0)$, če je $0\in D_f$.
5. Določi vodoravno ali poševno asimptoto s primerjavo stopenj oziroma z deljenjem polinomov.
6. Nariši asimptote črtkano, označi značilne točke in skiciraj veje grafa. Po potrebi preveri vrednosti funkcije na vsaki strani pola ali uporabi grafični program.

**Zgled za risanje:** Za $f(x)=\frac{2x+1}{x-2}$ označimo navpično asimptoto $x=2$, vodoravno asimptoto $y=2$, ničlo $(-\frac12,0)$ in presečišče z osjo $y$ $(0,-\frac12)$. Nato določimo potek vej z nekaj poskusnimi vrednostmi na intervalih $(-\infty,2)$ in $(2,\infty)$.

## 4. Racionalne enačbe

### Postopek

1. Zapiši pogoje: noben imenovalec ne sme biti nič.
2. Poišči najmanjši skupni imenovalec in pomnoži vsak člen enačbe z njim.
3. Reši dobljeno enačbo.
4. Preveri, ali rešitve zadoščajo začetnim pogojem, nato jih vstavi v začetno enačbo.

**Zgled:**
\[
\frac{2x+1}{x-1}=3,\qquad x\ne1.
\]
Pomnožimo z $x-1$:
\[
2x+1=3(x-1)\Rightarrow 2x+1=3x-3\Rightarrow x=4.
\]
Ker $4\ne1$, je rešitev $x=4$.

Presečišče grafov dveh racionalnih funkcij poiščemo tako, da rešimo enačbo $f(x)=g(x)$ in nato preverimo pogoje obeh funkcij.

## 5. Racionalne neenačbe

### Postopek z intervali predznakov

1. Vse prestavi na eno stran in izraz zapiši kot en ulomek.
2. Poišči ničle števca in imenovalca. To so kritične vrednosti, ki razdelijo številsko os na intervale.
3. Ugotovi predznak ulomka na vsakem intervalu.
4. Izberi intervale z zahtevanim predznakom. Ničle števca vključi pri $\leq$ ali $\geq$, pole pa vedno izključi.

**Zgled:** Rešimo $\frac{x-1}{x+2}\geq0$. Kritični vrednosti sta $-2$ (pol, izločen) in $1$ (ničla števca, vključena). Ulomek je nenegativen na zunanjih intervalih, zato
\[
\boxed{(-\infty,-2)\cup[1,\infty)}.
\]

Neenačbo lahko rešimo tudi grafično: določimo, kje je graf nad osjo $x$ (za $>0$ oziroma $\geq0$) ali pod njo (za $<0$ oziroma $\leq0$), pri tem pa pole izločimo.

## 6. Uporaba in modeliranje

Racionalna funkcija lahko opisuje obratno sorazmerje ali situacijo, kjer se razmerje spreminja z eno spremenljivko. Pri besedilni nalogi:

1. določi neznanko in njeno enoto;
2. zapiši zvezo med količinami kot enačbo ali funkcijo;
3. upoštevaj smiselne pogoje (npr. čas in količina sta pozitivna, imenovalec ni nič);
4. izračunaj rešitev in jo razloži v kontekstu;
5. presodi, ali model in odgovor ustrezata stvarni situaciji.

**Zgled:** Za stalno opravljeno delo velja $t=\frac{W}{v}$, kjer je $W$ obseg dela, $v$ hitrost dela in $t$ potreben čas. Če se hitrost poveča, se potreben čas zmanjša. Formula ima smisel za $v>0$.

## Pogoste napake

- Pozabiti izločiti ničle imenovalca pred krajšanjem.
- Razglasiti krajšano ničlo števca za ničlo funkcije, če je ta vrednost izločena.
- Vključiti pol v rešitev racionalne neenačbe.
- Pri reševanju enačbe ne preveriti dobljenih vrednosti v začetnem izrazu.
- Pri skici narisati asimptoto kot del grafa ali pozabiti označiti luknjo.

## Vir

Povzeto po poglavju »Racionalna funkcija« (str. 83) v dokumentu *Učni načrt z didaktičnimi priporočili: Matematika – gimnazija* (2025). Učni načrt poudarja definicijo, analizo in skiciranje grafov, vodoravne in poševne asimptote, enačbe in neenačbe ter matematično in življenjsko modeliranje. Glej [celotni učni načrt](Učni%20načrt%20matematika.pdf).