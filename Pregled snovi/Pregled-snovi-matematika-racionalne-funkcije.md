# Racionalne funkcije – kratek pregled za učenje

Pregled zajema gimnazijsko snov: definicijo in lastnosti racionalnih funkcij, ničle in pole, asimptote, analizo in skiciranje grafov, reševanje enačb in neenačb ter uporabo v matematičnih in življenjskih problemih.

## 1. Kaj je racionalna funkcija?

Racionalna funkcija je količnik dveh polinomov:
\[
f(x)=\frac{P(x)}{Q(x)},\qquad Q(x)\ne 0.
\]
Definicijsko območje dobimo tako, da iz množice realnih števil izločimo vse ničle imenovalca $Q(x)$. Polinomske funkcije in potenčne funkcije z negativnim celim eksponentom so posebni primeri racionalnih funkcij.

**Pomembno:** ulomke krajšamo šele po razcepu na faktorje. Krajšanje ne vrne izločenih vrednosti v definicijsko območje.

### Ničle, poli in luknje

- **Ničle:** rešimo $P(x)=0$, vendar preverimo, da ta vrednost ni izločena iz definicijskega območja.
- **Poli:** ničle imenovalca, ki po krajšanju še vedno ostanejo v imenovalcu. V takih točkah je graf funkcije običajno razcepljen in se približuje navpični asimptoti. Večkratna ničla imenovalca določa stopnjo pola.
- **Luknja:** če se isti faktor v števcu in imenovalcu pokrajša, ostane ta $x$ kljub temu izločen iz definicijskega območja. Ordinato luknje dobimo tako, da izločeno vrednost vstavimo v poenostavljeni predpis.

**Zgled:**
\[
g(x)=\frac{x^2-4}{x^2-x-2}=\frac{(x-2)(x+2)}{(x-2)(x+1)}=\frac{x+2}{x+1},
\]
pri čemer sta $x=-1$ in $x=2$ izločeni. Pri $x=-1$ je pol, pri $x=2$ pa luknja z ordinato $\frac{2+2}{2+1}=\frac{4}{3}$. Torej je $D_g=\mathbb{R}\setminus\{-1,2\}$ in luknja je $\left(2,\frac{4}{3}\right)$.

## 2. Asimptote

Asimptota je premica, ki jo graf funkcije približno dosega, ne da bi jo nikoli dosegel oziroma se ji dotaknil. Pri racionalnih funkcijah poznamo tri vrste asimptot.

- **Navpična asimptota:** v točki $x=a$, kadar imenovalec postane nič, števec pa po krajšanju ni nič. Točka $a$ je pol.
- **Vodoravna asimptota:** po krajšanju skupnih faktorjev primerjamo stopnji polinomov:
  - če je $\deg P<\deg Q$, je $y=0$;
  - če sta stopnji enaki, je $y=$ količnik vodilnih koeficientov.
- **Poševna asimptota:** če je stopnja števca za 1 večja od stopnje imenovalca, delimo polinoma. Količnik deljenja je enačba poševne asimptote.

Racionalno funkcijo z linearnim števcem in imenovalcem lahko po preoblikovanju zapišemo v obliki
\[
f(x)=q+\frac{k}{x-p},\qquad k\ne 0,
\]
kjer so $p,q,k$ konstante. Potem je $x=p$ navpična asimptota, $y=q$ pa vodoravna asimptota.

**Zgled:**
\[
f(x)=\frac{2x+1}{x-2}=2+\frac{5}{x-2}.
\]
Asimptoti sta $x=2$ in $y=2$, ničla je $x=-\frac{1}{2}$, presečišče grafa z osjo $y$ pa je $f(0)=-\frac{1}{2}$.

## 3. Kako analiziramo in skiciramo graf?

Za pregledno skico grafa racionalne funkcije sledimo tem korakom:

1. Razstavi števec in imenovalec na faktorje.
2. Določi definicijsko območje in morebitne izločene vrednosti.
3. Poenostavi ulomek; označi ničle, pole in luknje.
4. Določi presečišča grafa z osema: ničle dobimo iz $f(x)=0$, presečišče z osjo $y$ pa izračunamo z $f(0)$, če je $0\in D_f$.
5. Določi vodoravno ali poševno asimptoto s primerjavo stopenj oziroma z deljenjem polinomov.
6. Nariši asimptote črtkano, označi značilne točke in skiciraj veje grafa. Po potrebi preveri vrednosti funkcije na vsaki strani pola ali uporabi grafični program.

**Zgled za risanje:** Naj bo
\[
 f(x)=\frac{2x+1}{x-2}.
\]
Najprej določimo, kje funkcija ni definirana: imenovalec je $x-2$, zato je $x\ne 2$.

- **Navpična asimptota:** nastane, ko imenovalec postane $0$, zato je
  \[
  x-2=0\quad\Rightarrow\quad x=2.
  \]
  To je navpična asimptota.

- **Vodoravna asimptota:** primerjamo stopnji števca in imenovalca. Oba sta stopnje $1$, zato je vodoravna asimptota enaka količniku vodilnih koeficientov:
  \[
  y=\frac{2}{1}=2.
  \]
  Torej je $y=2$ vodoravna asimptota.

- **Ničla:** rešimo števec $2x+1=0$:
  \[
  2x+1=0\quad\Rightarrow\quad 2x=-1\quad\Rightarrow\quad x=-\frac{1}{2}.
  \]
  Pri $x=-\frac{1}{2}$ je $y=0$, torej je ničla točka
  \[
  \left(-\frac{1}{2},0\right).
  \]

- **Presečišče z osjo $y$:** izračunamo $f(0)$, če je $0$ v definicijskem območju:
  \[
  f(0)=\frac{2\cdot 0+1}{0-2}=\frac{1}{-2}=-\frac{1}{2}.
  \]
  Torej je presečišče z osjo $y$ točka
  \[
  \left(0,-\frac{1}{2}\right).
  \]

Zdaj vemo: graf ima navpično asimptoto $x=2$, vodoravno asimptoto $y=2$, ničlo v $\left(-\frac{1}{2},0\right)$ in presečišče z osjo $y$ v $\left(0,-\frac{1}{2}\right)$. Nato lahko izračunamo še nekaj vrednosti, na primer $f(1)$ in $f(3)$, da določimo potek vej na intervalih $(-\infty,2)$ in $(2,\infty)$.

## 4. Racionalne enačbe

### Postopek

1. Zapiši pogoje: noben imenovalec ne sme biti nič.
2. Poišči najmanjši skupni imenovalec in pomnoži vsak člen enačbe z njim.
3. Reši dobljeno enačbo.
4. Preveri, ali rešitve zadoščajo začetnim pogojem, nato jih vstavimo v začetni izraz.

**Zgled:**
\[
\frac{2x+1}{x-1}=3,\qquad x\ne 1.
\]
Pomnožimo z $x-1$:
\[
2x+1=3(x-1)\Rightarrow 2x+1=3x-3\Rightarrow x=4.
\]
Ker $4\ne 1$, je rešitev $x=4$.

Presečišče grafov dveh racionalnih funkcij poiščemo tako, da rešimo enačbo $f(x)=g(x)$ in nato preverimo pogoje obeh funkcij.

## 5. Racionalne neenačbe

### Postopek z intervali predznakov

1. Vse prestavi na eno stran in izraz zapiši kot en ulomek.
2. Poišči ničle števca in imenovalca. To so kritične vrednosti, ki razdelijo številsko os na intervale.
3. Ugotovi predznak ulomka na vsakem intervalu.
4. Izberi intervale z zahtevanim predznakom. Ničle števca vključi pri $\leq$ ali $\geq$, pole pa vedno izključi.

**Zgled:** Rešimo $\frac{x-1}{x+2}\ge 0$. Kritični vrednosti sta $-2$ (pol, izločen) in $1$ (ničla števca, vključena). Ulomek je nenegativen na zunanjih intervalih, zato
\[
\boxed{(-\infty,-2)\cup[1,\infty)}.
\]

Neenačbo lahko rešimo tudi grafično: določimo, kje je graf nad osjo $x$ (za $>0$ oziroma $\ge 0$) ali pod njo (za $<0$ oziroma $\le 0$), pri tem pa izločimo pole.

## 6. Uporaba in modeliranje

Racionalna funkcija lahko opisuje obratno sorazmerje ali situacijo, kjer se razmerje spreminja z eno spremenljivko. Pri besedilni nalogi:

1. določi neznanko in njeno enoto;
2. zapiši zvezo med količinami kot enačbo ali funkcijo;
3. upoštevaj smiselne pogoje (npr. čas in količina sta pozitivna, imenovalec ni nič);
4. izračunaj rešitev in jo razloži v kontekstu;
5. presodi, ali model in odgovor ustrezata stvarni situaciji.

**Zgled:** Za stalno opravljeno delo velja $t=\frac{W}{v}$, kjer je $W$ obseg dela, $v$ hitrost dela in $t$ potreben čas. Če se hitrost poveča, se potreben čas zmanjša. Formula ima smisel za $v>0$.

## 7. Pogoste napake

Na hitro: ko si negotov, se vrni k enemu od teh primerov.

- **Pozabiti na pogoje.**

  Če je
  \[
  \frac{1}{x-2},
  \]
  potem je $x\ne 2$. Če tega ne zapišeš, lahko v nadaljevanju dobiš napačno rešitev.

- **Krajšanje, a napačna ničla.**

  Pri
  \[
  g(x)=\frac{(x-2)(x+2)}{(x-2)(x+1)}=\frac{x+2}{x+1}
  \]
  je $x=2$ luknja, ne ničla. Faktor $(x-2)$ se pokrajša, a vrednost $x=2$ še vedno ni v definicijskem območju.

- **Vključiti pol v neenačbo.**

  Pri
  \[
  \frac{x+1}{x-3}\ge 0
  \]
  je $x=3$ pol, zato ga ne smeš vključiti v rešitev. Samo ničle števca se lahko vključijo, če je neenačba $\ge 0$ ali $\le 0$.

- **Ne preveriti rešitve v začetnem izrazu.**

  Če rešiš enačbo in dobiješ $x=1$, a se v začetnem izrazu pojavi imenovalec $x-1$, potem je $x=1$ napačna rešitev, ker delimo z $0$.

- **Na skici pol, luknja in asimptota zamenjati.**

  Pri isti funkciji
  \[
  f(x)=\frac{(x-2)(x+2)}{(x-2)(x+1)}=\frac{x+2}{x+1}
  \]
  je:
  - $x=2$ luknja,
  - $x=-1$ pol,
  - asimptota je črtkana premica, ne del grafa.

  Kratko: pol = graf se »raztrga«, luknja = prazna točka, asimptota = graf se samo približuje črti.