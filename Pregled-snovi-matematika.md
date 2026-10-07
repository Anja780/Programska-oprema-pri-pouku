# Matematika – kratek pregled za učenje

Pregled povzema glavne vsebinske sklope gimnazijskega učnega načrta: logiko in množice, aritmetiko, algebro, geometrijo, funkcije, analizo ter kombinatoriko, verjetnost in statistiko. Namenjen je hitremu ponavljanju; pri učenju vedno preveri tudi zapiske in navodila učitelja.

## 1. Logika, množice in zapis

- Trditev je izjava, ki je lahko resnična ali neresnična. Pri dokazovanju uporabi definicije in jasno utemelji vsak sklep; za ovržbo splošne trditve zadostuje en protiprimer.
- $A\cup B$ je unija, $A\cap B$ presek, $A\setminus B$ pa elementi, ki so v $A$, ne pa v $B$.
- Interval $(a,b)$ ne vsebuje krajišč, $[a,b]$ ju vsebuje. Na primer, $x\geq2$ zapišemo $[2,\infty)$.

## 2. Števila in računanje

### Ulomki, potence in odstotki

Ulomke prištejemo s skupnim imenovalcem; pri množenju množimo števce in imenovalce; pri deljenju množimo z obratnim ulomkom. Imenovalec ne sme biti nič.

Za ustrezne $a,m,n$ veljajo:
\[
a^m a^n=a^{m+n},\qquad \frac{a^m}{a^n}=a^{m-n},\qquad (a^m)^n=a^{mn},\qquad a^{-n}=\frac1{a^n}.
\]

$p\%$ pomeni $p/100$. Povečanje za $p\%$ pomeni množenje z $1+p/100$, zmanjšanje pa z $1-p/100$.

**Zgled:** $15\%$ od 80 je $0,15\cdot80=12$.

### Korenjenje, logaritmi in kompleksna števila

Kvadratni koren realnega števila je definiran, kadar je podkoren izraz nenegativen. Logaritem je obratna operacija potenciranju:
\[
\log_a b=c\iff a^c=b,\qquad a>0,\ a\ne1,\ b>0.
\]
Zato moramo pri logaritemski enačbi preveriti, da so vsi argumenti pozitivni. Pravili: $\log_a(xy)=\log_a x+\log_a y$ in $\log_a(x^r)=r\log_a x$.

Kompleksno število je $z=a+bi$, kjer $i^2=-1$. Konjugirano število je $\bar z=a-bi$, absolutna vrednost pa $|z|=\sqrt{a^2+b^2}$.

## 3. Algebra: izrazi, enačbe in neenačbe

### Preoblikovanje izrazov

Pomembne identitete:
\[
(a+b)^2=a^2+2ab+b^2,\quad (a-b)^2=a^2-2ab+b^2,\quad a^2-b^2=(a-b)(a+b).
\]
Pri razčlenjevanju najprej izpostavi skupni faktor, nato preveri razliko kvadratov ali kvadrat dvočlenika. Ulomke krajšaj šele po razcepu na faktorje; zapiši vse vrednosti, ki izničijo imenovalec.

### Reševanje enačb in neenačb

1. **Linearna enačba:** odstrani oklepaje, zberi člene z neznanko na eno stran in izračunaj neznanko.
2. **Kvadratna enačba** $ax^2+bx+c=0$: izračunaj diskriminanto $D=b^2-4ac$ in uporabi
   \[
   x=\frac{-b\pm\sqrt D}{2a}.
   \]
   Če je $D>0$, sta dve realni rešitvi; če $D=0$, ena dvojna; če $D<0$, realnih rešitev ni.
3. **Racionalna enačba:** najprej določi prepovedane vrednosti imenovalcev; šele nato pomnoži z najmanjšim skupnim imenovalcem in na koncu preveri rešitve.
4. **Neenačba:** pri množenju ali deljenju z negativnim številom obrni znak. Pri racionalni neenačbi označi števca ničle in imenovalca pole, razdeli številsko os na intervale ter preveri predznak na vsakem.
5. **Sistem enačb:** uporabi vstavljanje ali seštevanje enačb, nato rešitev preveri v obeh.

**Zgled:** $x^2-5x+6=0\Rightarrow(x-2)(x-3)=0$, zato $x=2$ ali $x=3$.

## 4. Geometrija, merjenje in vektorji

### Formule za like in telesa

- Pravokotni trikotnik: $a^2+b^2=c^2$ (Pitagorov izrek).
- Trikotnik: ploščina $S=ah/2$, obseg $o=a+b+c$.
- Krog: ploščina $S=\pi r^2$, obseg $o=2\pi r$.
- Prizma: $V=S_{\rm osn}h$; valj: $V=\pi r^2h$, $S=2\pi r^2+2\pi rh$.
- Stožec: $V=\frac13\pi r^2h$; krogla: $V=\frac43\pi r^3$, $S=4\pi r^2$.

V poljubnem trikotniku veljata sinusni izrek $\frac a{\sin\alpha}=\frac b{\sin\beta}=\frac c{\sin\gamma}$ in kosinusni izrek $c^2=a^2+b^2-2ab\cos\gamma$. V pravokotnem trikotniku sta $\sin\alpha=\frac{\text{nasprotna kateta}}{\text{hipotenuza}}$ in $\cos\alpha=\frac{\text{priležna kateta}}{\text{hipotenuza}}$.

### Koordinate in vektorji

Razdalja med točkama $(x_1,y_1)$ in $(x_2,y_2)$:
\[
d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}.
\]
Za $\vec u=(u_1,u_2)$ in $\vec v=(v_1,v_2)$ je skalarni produkt $\vec u\cdot\vec v=u_1v_1+u_2v_2$. Če je skalarni produkt 0, sta vektorja pravokotna.

**Postopek:** nariši skico, označi znane količine, izberi ustrezno formulo, vstavi enote in preveri, ali je rezultat smiseln glede na skico.

## 5. Funkcije in krivulje

Funkcija vsakemu dovoljenemu $x$ priredi natanko eno vrednost $f(x)$. Pri analizi grafa preveri definicijsko območje, ničle, presečišča z osema, simetrijo, ekstreme in asimptote.

- **Linearna:** $f(x)=kx+n$; $k$ je smerni koeficient, presečišče z osjo $y$ je $(0,n)$.
- **Kvadratna:** $f(x)=ax^2+bx+c$; os simetrije je $x=-b/(2a)$, teme pa $T=(-b/(2a),-D/(4a))$, kjer je $D=b^2-4ac$. Predznak $a$ pove, kam je obrnjena parabola.
- **Racionalna:** $f(x)=p(x)/q(x)$; $q(x)\ne0$. Ničle poiščemo iz $p(x)=0$, razen če jih krajšanje izloči. Skupni faktor števca in imenovalca lahko ustvari luknjo.
- **Eksponentna in logaritemska:** $a^x$ in $\log_a x$ ($a>0$, $a\ne1$) sta obratni funkciji; logaritem je definiran samo za $x>0$.
- **Trigonometrične:** $\sin x$, $\cos x$, $\tan x=\sin x/\cos x$; velja $\sin^2x+\cos^2x=1$.
- **Krivulje drugega reda:** krožnica s središčem $(h,k)$ in polmerom $r$ ima enačbo $(x-h)^2+(y-k)^2=r^2$; med krivulje sodijo tudi parabola, elipsa in hiperbola.

**Postopek za skico grafa:** določi definicijsko območje; poišči ničle in presečišča z osema; preveri značilne točke, simetrijo in asimptote; nato nariši graf skozi dobljene podatke.

**Zgled:** $f(x)=x^2-4$ ima ničli $-2$ in $2$, presečišče z osjo $y$ je $(0,-4)$, teme pa $(0,-4)$.

## 6. Zaporedja in analiza

### Zaporedja

- Aritmetično zaporedje z razliko $d$: $a_n=a_1+(n-1)d$, $S_n=\frac{n(a_1+a_n)}2$.
- Geometrijsko zaporedje s količnikom $q$: $a_n=a_1q^{n-1}$, $S_n=a_1\frac{1-q^n}{1-q}$ za $q\ne1$. Neskončna geometrijska vrsta ima vsoto $S=\frac{a_1}{1-q}$, če $|q|<1$.

### Odvod in integral

Odvod $f'(x)$ meri trenutni naklon oziroma hitrost spreminjanja. Osnovno pravilo je $(x^n)'=nx^{n-1}$; veljata tudi $(f+g)'=f'+g'$ in $(fg)'=f'g+fg'$. Za ekstreme poišči stacionarne točke z reševanjem $f'(x)=0$ in preveri spremembo predznaka odvoda.

Integral povezuje ploščino z obratnim postopkom odvajanja:
\[
\int x^n\,dx=\frac{x^{n+1}}{n+1}+C\ (n\ne-1),\qquad \int_a^b f(x)\,dx=F(b)-F(a),\quad F'=f.
\]

**Zgled:** $f(x)=x^2-4x$ ima odvod $f'(x)=2x-4$. Iz $f'(x)=0$ sledi $x=2$; ker je parabola obrnjena navzgor, je minimum $f(2)=-4$.

## 7. Kombinatorika, verjetnost in statistika

- **Pravilo produkta:** če prvi izbor opravimo na $m$, drugi pa na $n$ načinov, imamo $mn$ možnosti.
- **Permutacije:** razporeditev vseh $n$ različnih elementov: $n!$.
- **Variacije brez ponavljanja:** urejen izbor $k$ elementov izmed $n$: $\frac{n!}{(n-k)!}$.
- **Kombinacije:** izbor $k$ elementov, pri katerem vrstni red ni pomemben:
  \[
  \binom nk=\frac{n!}{k!(n-k)!}.
  \]
- **Verjetnost:** pri enako verjetnih izidih $P(A)=\frac{\text{ugodnih izidov}}{\text{vseh izidov}}$; velja $0\leq P(A)\leq1$ in $P(\bar A)=1-P(A)$.
- **Statistika:** aritmetična sredina je vsota podatkov, deljena z njihovim številom; mediana je srednja urejena vrednost; modus je najpogostejša vrednost. Varianca in standardni odklon merita razpršenost.

**Zgled:** Pri metu poštene kocke je verjetnost, da pade število večje od 4, $2/6=1/3$.

## Preden oddaš rešitev

1. Ali sem zapisal pogoje in upošteval definicijsko območje?
2. Ali sem pravilno uporabil predznake, oklepaje in enote?
3. Ali sem dobljene rešitve preveril v začetni nalogi?
4. Ali rezultat odgovarja na vprašanje in je smiseln?
5. Ali je postopek dovolj jasen, da mu lahko sledi še kdo drug?

## Vir

Povzeto po dokumentu *Učni načrt z didaktičnimi priporočili: Matematika – gimnazija* (2025). To je orientacijski povzetek, ne nadomestilo za učbenik ali učiteljeve zapiske. Glej tudi [celotni učni načrt](Učni%20načrt%20matematika.pdf).