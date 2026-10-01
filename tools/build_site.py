#!/usr/bin/env python3
"""
Builds Lubna Qassim's site as static HTML.

Every factual claim here traces to CLIENT-FACTS.md, which is her own biography text.
Nothing is invented. Where she supplied wording, her wording is used verbatim.

Generated rather than hand-written so the chrome stays identical across pages and a
design revision is one edit, not ten.
"""
import os, re, html, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "essays"), exist_ok=True)

NAV = [
    ("profile.html", "Profile"),
    ("contribution.html", "Advisory"),
    ("speaking.html", "Speaking"),
    ("writing.html", "Writing"),
    ("recognition.html", "Recognition"),
    ("mentorship.html", "Mentorship"),
    ("gallery.html", "Gallery"),
]


def page(fname, title, body, desc, cls="", depth=0):
    up = "../" * depth
    nav = "\n".join(
        f'      <a href="{up}{h}"{" class=\'is-current\'" if h == fname else ""}>{t}</a>'
        for h, t in NAV)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Alex+Brush&family=Allura&family=Newsreader:ital,opsz,wght@0,6..72,200;0,6..72,300;0,6..72,400;1,6..72,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}styles.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' fill='%2317150f'/><text x='50' y='68' font-family='Georgia,serif' font-size='44' fill='%23f5f2eb' text-anchor='middle'>LQ</text></svg>">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="{cls}">

<p class="draft-ribbon"><span>Draft</span> Design for review — not published. Content still being confirmed.</p>

<a class="skip" href="#main">Skip to content</a>

<header class="masthead" id="masthead">
  <a class="monogram" href="{up}index.html" aria-label="Home"><span>LQ</span></a>
  <nav class="masthead__nav" aria-label="Primary">
{nav}
  </nav>
  <div class="masthead__actions">
    <a class="btn" href="{up}contact.html">Enquiries</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Menu">
      <span></span><span></span>
    </button>
  </div>
</header>

<div class="drawer" id="drawer" hidden>
  <nav aria-label="Mobile">
{chr(10).join(f'    <a href="{up}{h}"><i>{i+1:02d}</i> {t}</a>' for i, (h, t) in enumerate(NAV))}
    <a href="{up}contact.html"><i>{len(NAV)+1:02d}</i> Enquiries</a>
  </nav>
</div>

<main id="main">
{body}
</main>

<footer class="footer">
  <div class="wrap footer__inner">
    <div class="footer__brand">
      <span class="monogram monogram--static"><span>LQ</span></span>
      <p>Lubna Qassim<br><i>Law · Government · Business · Diplomacy</i></p>
    </div>
    <nav class="footer__nav" aria-label="Footer">
{chr(10).join(f'      <a href="{up}{h}">{t}</a>' for h, t in NAV)}
      <a href="{up}contact.html">Enquiries</a>
    </nav>
    <p class="footer__colophon">
      &copy; Lubna Qassim. Draft design for review — nothing on this page is published.
      Set in Bodoni Moda, Newsreader and Archivo.
    </p>
  </div>
</footer>

<div class="lightbox" id="lightbox" hidden>
  <button class="lightbox__close" type="button" aria-label="Close">&times;</button>
  <button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="Previous">&#8249;</button>
  <button class="lightbox__nav lightbox__nav--next" type="button" aria-label="Next">&#8250;</button>
  <figure><img src="" alt=""><figcaption></figcaption></figure>
</div>

<script src="{up}main.js"></script>
</body>
</html>
"""
    with open(os.path.join(OUT, fname), "w") as fh:
        fh.write(doc)
    print("  ", fname)


# ───────────────────────────── content ─────────────────────────────

CHAIRS = [
    ("Law", "Clifford Chance, London and Dubai — arbitration, corporate finance and "
            "cross-border matters for governments and financial institutions."),
    ("Government", "Director of Economic Legislation at the UAE Ministry of Economy — "
                   "fourteen major economic laws, the first modernisation in twenty-six years."),
    ("Business", "Senior Executive Vice President and Group Chief General Counsel at "
                 "Emirates NBD — its first female C-suite executive, leading a team of three hundred."),
    ("Diplomacy", "Deputy Permanent Representative and Chargé d'Affaires to the United "
                  "Nations in Geneva, across more than forty international organisations."),
]

AREAS = [
    ("Geoeconomics &amp; Global Strategy",
     "Geoeconomic shifts and the changing global order",
     ["The intersection of geopolitics, economics, investment and regulation",
      "Gulf positioning in a changing international system",
      "Cross-border investment and economic diplomacy",
      "Navigating complex international and political environments",
      "Multilateral strategy and international engagement",
      "The strategic implications of fragmentation, competition and shifting alliances"]),
    ("Governance, Institutional Reform &amp; Public Policy",
     "Institutional governance and effectiveness",
     ["Regulatory and legislative reform",
      "Economic policy and regulatory frameworks",
      "Public sector transformation",
      "Government decision-making and the public–private interface",
      "Institutional accountability",
      "Building effective governance frameworks"]),
    ("Boards, Leadership &amp; Strategic Advisory",
     "Strategic counsel to boards and senior leadership",
     ["Board governance, governance and risk",
      "Corporate and institutional leadership",
      "Stakeholder management",
      "Government and international relations",
      "Navigating complex or high-consequence decisions",
      "Executive leadership in highly regulated environments"]),
    ("Women's Leadership &amp; Economic Participation",
     "Women in senior leadership, and on boards",
     ["Women's economic participation",
      "Leadership in traditionally male-dominated environments",
      "Building institutional pathways for women to advance",
      "Returning to leadership after career transitions",
      "Mentorship and sponsorship",
      "Gender diversity as a governance and business issue"]),
    # fifth area added at her request, 29-sep
    ("Peace Diplomacy &amp; Interfaith Dialogue",
     "Dialogue between states, faiths and institutions",
     ["Multilateral peacebuilding and preventive diplomacy",
      "Interfaith and intercultural dialogue",
      "Women's participation in peace processes",
      "Humanitarian engagement and the institutions that carry it",
      "Convening across governments, faith leaders and international organisations",
      "Education and dialogue as instruments of stability"]),
]

THEMES = [
    ("Geoeconomics and the New Global Order",
     "How economics, investment, regulation and diplomacy are reshaping international power."),
    ("The Gulf and the Changing Architecture of Global Power",
     "The evolution of the Gulf's role in global economic and geopolitical affairs, and what the "
     "region's increasing international engagement means for business, diplomacy and institutions."),
    ("Leadership Across Institutions: From the Boardroom to the Diplomatic Table",
     "A personal keynote drawing on a career across private practice, government, banking and "
     "diplomacy — transitions lived rather than studied."),
    ("The Boardroom Meets the Diplomatic Table",
     "What leaders can learn from diplomacy about negotiation, stakeholder management, influence "
     "and decision-making — and what diplomacy can learn from business about governance, "
     "execution and accountability."),
    ("Women, Leadership and Economic Participation",
     "Not a generic talk on women in leadership, but what institutions actually need to do to "
     "create genuine pathways — drawn from navigating senior leadership across government, "
     "financial services and international diplomacy."),
    ("Law, Reform and Institutional Change",
     "How legal and regulatory architecture can enable economic and institutional transformation, "
     "drawing directly on legislative reform experience."),
]

FORMATS = ["Keynotes", "Executive Dialogues", "Board Retreats", "Roundtables",
           "Moderation", "University Lectures", "Policy Conversations"]

RECOGNITION = [
    ("Certificate of Recognition, World Health Organization",
     "Presented by Dr Tedros Adhanom Ghebreyesus, Director-General of the WHO, in recognition of "
     "leadership and contribution to strengthening the UAE's partnership with WHO.",
     "15 October 2024 · WHO Headquarters, Geneva", "who-tedros"),
    ("Top 100 Emirati Pioneers",
     "Honoured by Sheikha Shamma bint Mohammed bin Khalifa Al Nahyan — recognising a journey of "
     "contribution and impact beyond the titles held.",
     "16 October 2025", "pioneers"),
    ("Best General Counsel — Woman in Business Law, Middle East",
     "IFLR Women in Business Law Awards.", "2018", None),
    ("Arab Women 45", "Arabian Business.", "2018", None),
    ("Founding Member, 30% Club GCC Chapter",
     "Advancing women's representation on boards and in senior leadership across the Gulf.",
     "", None),
    # caption corrected at her instruction: she was interviewed and contributed to the
    # research — she was not "recognised by" an individual
    ("Balance for Better",
     "Contributor and interviewee to the research on gender parity and better balance, "
     "with the Dubai Business Women Council and the United Nations.", "", "balance"),
]

GALLERY = [
    ("chamber", "The chamber, before the session", "Geneva"),
    ("desk-bw", "At the High Representative's desk", "Geneva"),
    ("who-tedros", "Certificate of Recognition, with Dr Tedros Adhanom Ghebreyesus",
     "WHO HQ, Geneva · 15 October 2024"),
    ("pioneers", "Top 100 Emirati Pioneers", "16 October 2025"),
    ("speaking", "In conversation", ""),
    ("riyadh", "Keys to the Kingdom: Getting into the C-Suite", "Achieving Women Forum, Riyadh · 2017"),
    ("panel-ifrc", "Panel, International Federation of Red Cross and Red Crescent Societies", "Geneva"),
    ("desk-bw-2", "In session", "Geneva"),
    ("podium", "At the podium", ""),
    ("balance", "Balance for Better", "Dubai Business Women Council and the United Nations"),
    ("portrait-col", "Portrait", ""),
    ("students", "With students", ""),
]

ESSAYS = [
    ("bankruptcy-laws", "For the country's prosperity, better bankruptcy laws",
     "26 August 2009", "The National",
     "Written sixteen years before the UAE's insolvency framework was rebuilt: why a country "
     "that wants to be a financial centre needs a rescue culture, not a stigma."),
    ("leaders-vision", "Our leaders had a vision: today it is our reality",
     "11 January 2009", "The National",
     "On the fortieth anniversary years of a young federation — what it takes to build a nation "
     "on vision and trust, and what the UAE has to teach about growth."),
    ("jobs-for-emiratis", "Jobs for Emiratis: why the state can't do it all",
     "23 June 2009", "The National",
     "Employment, the private sector and the limits of what government can be asked to carry."),
    ("crisis-facing-graduates", "The crisis facing graduates, and how we can help",
     "2 March 2009", "The National",
     "Written in the teeth of the financial crisis, on what a generation entering the workforce "
     "needed from the institutions around it."),
    ("gender-parity-gap", "How to reduce the gender parity gap",
     "21 May 2008", "The National",
     "An early statement of an argument she has made ever since: parity is a governance and "
     "economic question, not a social courtesy."),
    ("book-at-bedtime", "To build a world, begin with a book at bedtime",
     "18 November 2008", "The National",
     "On reading, education and the long work of building a literate society."),
]

PRESS = [
    ("2026", "Leading the UN in a World That Has Already Changed",
     "Modern Diplomacy · 26 June 2026",
     "https://moderndiplomacy.eu/2026/06/26/leading-the-un-in-a-world-that-has-already-changed/"),
    ("2026", "The New Calculus of Global Investment",
     "ITT Nexus · 3 September 2026", "https://ittnexus.com/the-new-calculus"),
    ("2026", "How Merchant States Are Reshaping Global Business Connectivity",
     "The Business Times, Singapore",
     "https://www.businesstimes.com.sg/opinion-features/how-merchant-states-are-reshaping-global-business-connectivity"),
    ("2026", "New Age Chokepoints", "The Business Times, Singapore",
     "https://www.businesstimes.com.sg/opinion-features/new-age-chokepoints"),
    ("2026", "Law, Power and the Limits of Institutions",
     "The International Wire · interview by Danish Shaikh",
     "https://theinternationalwire.com/law-power-and-the-limits-of-institutions/"),
    ("2013", "Why I experienced discrimination as a public leader in the UAE",
     "The Guardian · Public Leaders Network",
     "https://www.theguardian.com/public-leaders-network/2013/nov/20/uae-public-leader-discrimination-experience"),
    ("", "Breaking barriers", "The Legal 500 · GC Magazine",
     "https://www.legal500.com/gc-magazine/interview/breaking-barriers-lubna-qassim/"),
    ("", "Legal visionary: a journey from boardrooms to global diplomacy", "Corporate Counsel Now",
     "https://corporatecounselnow.com/legal-visionary-lubna-qassims-journey-boardrooms-global-diplomacy"),
    ("2018", "Arab Women 45", "Arabian Business",
     "https://www.arabianbusiness.com/lists/391053-2018-arab-women45lubna-qassim"),
    ("", "Incentivising change: ten guidelines for MENA women",
     "Entrepreneur Middle East",
     "https://mena.entrepreneur.com/growth-strategies/incentivizing-change-10-guidelines-for-mena-women-in/295335"),
    ("", "Female appointments to key positions show KSA commitment to modernisation",
     "Arab News",
     "https://www.arabnews.com/business/female-appointments-to-key-positions-show-ksa-commitment-to-modernization-says-uaes-lubna-qassim-1126956"),
    ("", "My UAE: Lubna Qassim on her varied legal and political career", "The National",
     "https://www.thenationalnews.com/arts-culture/my-uae-lubna-qassim-on-her-varied-legal-and-political-career-1.76496"),
    ("", "Inspiring Women", "Al Shindagah",
     "http://www.alshindagah.com/en/article/en-us/13/13/29/24/463/inspiring-women-lubna-qassim"),
    ("", "Women Matter: ten years of insights on gender diversity",
     "McKinsey &amp; Company · cited alongside Christine Lagarde",
     "https://www.mckinsey.com/featured-insights/gender-equality/women-matter-ten-years-of-insights-on-gender-diversity"),
    ("", "30% Club — MENA chapter", "30% Club",
     "https://30percentclub.org/wp-content/uploads/2021/09/mena.html"),
    ("", "British Chamber of Commerce Dubai", "British Chamber Dubai",
     "https://britishchamberdubai.com/news-details/936"),
]

BOOKS = [
    ("book-peace", "Promoting Peace, Human Rights and Dialogue among Civilizations",
     "2020 · Geneva", "University for Peace · UN75 · Muslim World League"),
    ("book-multi", "Multilateralism, Human Rights and Diplomacy: A Global Perspective",
     "2021 · Geneva", "Muslim World League · University for Peace · United Nations"),
]

GLANCE = [
    # Helsinki removed at her instruction (29-sep). Do not reinstate.
    ("Present", "Distinguished Fellow, UCLA Center for Middle East Development"),
    ("2019 – 2024", "Deputy Permanent Representative and Chargé d'Affaires of the UAE to the "
                    "United Nations and International Organizations, Geneva"),
    ("2018", "Minister Plenipotentiary of the First Degree and Senior Legal Counsel to the "
             "UAE Minister of Foreign Affairs — appointed by Presidential Decree"),
    ("", "Senior Executive Vice President, Group Chief General Counsel and Group Company "
         "Secretary, Emirates NBD — first female C-suite executive"),
    ("", "Public Sector Reform Consultant, The World Bank"),
    ("", "Director of Economic Legislation, UAE Ministry of Economy"),
    ("", "Clifford Chance, London and Dubai"),
]


# ───────────────────────────── pages ─────────────────────────────

def home():
    chart = open(os.path.join(OUT, "chart.svg.html")).read()

    doors = """
      <a class="door reveal" href="profile.html">
        <span class="door__img"><img src="img/desk-bw.jpg" alt="" loading="lazy"></span>
        <span class="door__text"><i>01</i><b>The profile</b>
        <em>Twenty-six years, four institutions, one set of questions.</em></span>
      </a>
      <a class="door reveal" href="writing.html">
        <span class="door__img"><img src="img/book-multi.jpg" alt="" loading="lazy"></span>
        <span class="door__text"><i>02</i><b>Writing &amp; interviews</b>
        <em>Two books, essays and conversations on law, power and institutions.</em></span>
      </a>
      <a class="door reveal" href="speaking.html">
        <span class="door__img"><img src="img/speaking.jpg" alt="" loading="lazy"></span>
        <span class="door__text"><i>03</i><b>Speaking</b>
        <em>Keynotes, roundtables and rooms that want a real argument.</em></span>
      </a>"""

    recog = " <b>·</b> ".join(
        "World Health Organization", ) if False else " <b>·</b> ".join([
            "World Health Organization", "Top 100 Emirati Pioneers", "IFLR Women in Business Law",
            "Arabian Business Arab Women 45", "30% Club GCC"])

    body = f"""
  <section class="hero">
    <img class="hero__bg" src="img/chamber.jpg" alt="" fetchpriority="high">
    <div class="hero__inner wrap">
      <h1 class="hero__name"><span>Lubna</span> <em>Qassim</em></h1>
      <p class="hero__line">Working at the intersection of law, government,
        business and diplomacy.</p>
      <a class="link-arrow link-arrow--light" href="profile.html">Read the profile</a>
    </div>
    <span class="scrollcue"><i></i>Scroll</span>
  </section>

  <section class="section section--chairs">
    <div class="chart-wrap">{chart}</div>
    <div class="wrap">
      <div class="chairs__head">
        <h2 class="bigmarks"><span>Law.</span> <span>Government.</span>
          <span>Business.</span> <span>Diplomacy.</span></h2>
        <p class="chairs__lede">Four sides of the same table — and the same questions look
          entirely different depending on which chair you are sitting in.</p>
      </div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="wrap statement">
      <p class="statement__text">The rare adviser who can tell a minister and a chief
        executive the same difficult thing in the same afternoon.</p>
      <p class="statement__note">A statement of how she works — not a quotation.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="doors">{doors}</div>
    </div>
  </section>

  <section class="section section--dark">
    <div class="wrap">
      <p class="eyebrow">Selected recognition</p>
      <p class="recog-strip">{recog}</p>
      <a class="link-arrow" href="recognition.html">See the recognitions</a>
    </div>
  </section>
"""
    page("index.html", "Lubna Qassim — International lawyer, geoeconomics and governance",
         body, "Lubna Qassim — working at the intersection of law, government, business and "
               "diplomacy.", cls="page-home")


def profile():
    glance = "\n".join(
        f'        <li><i>{w}</i><span>{t}</span></li>' for w, t in GLANCE)

    body = f"""
  <section class="pagehead">
    <div class="wrap">
      <p class="eyebrow">Profile</p>
      <h1 class="pagehead__title">A career spent on<br>four sides of the<br><em>same table</em></h1>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="colset">
        <div class="colset__label">
          <figure class="sidefig">
            <img src="img/desk-bw-2.jpg" alt="Lubna Qassim at the High Representative's desk" loading="lazy">
            <figcaption>Geneva</figcaption>
          </figure>
        </div>

        <div class="colset__body">
          <div class="prose letter reveal">
            <p class="dropcap">Lubna Qassim is an international lawyer, senior policy leader and
            former senior diplomat whose twenty-six year career has spanned government,
            international law, institutional leadership, financial services and multilateral
            diplomacy.</p>

            <p>She has worked at the intersection of public policy, global affairs and
            institutional transformation, with extensive experience in initiatives relating to
            health, humanitarian affairs, human rights, women and girls, education, climate and
            sustainable development. She brings a distinctive combination of senior government
            experience, international diplomacy, executive leadership and global institutional
            relationships, with a strong understanding of how to translate strategic priorities
            into partnerships, programmes and sustainable impact.</p>

            <h2 class="movement">The lawyer, and then the legislator</h2>

            <p>Ms Qassim began her career with Clifford Chance in London and Dubai, advising
            governments, multinational corporations and financial institutions on international
            arbitration, corporate finance, governance and complex cross-border matters.</p>

            <p>She subsequently served as Director of Economic Legislation at the UAE Ministry of
            Economy, where she led the reform and passage of fourteen major economic laws —
            the first comprehensive modernisation of the UAE's federal economic legislation in
            twenty-six years. She later served as a Public Sector Reform Consultant to the World
            Bank, advising governments across the GCC on governance, institutional transformation
            and economic modernisation.</p>

            <h2 class="movement">The executive</h2>

            <p>In the private sector, Ms Qassim served as Senior Executive Vice President, Group
            Chief General Counsel and Group Company Secretary of Emirates NBD. As its first female
            C-suite executive, she led a three-hundred-member team supporting three listed banks,
            twenty-two companies and eight international operations, with responsibility spanning
            governance, risk, regulatory frameworks, complex disputes and institutional
            transformation.</p>

            <h2 class="movement">The diplomat</h2>

            <p>In 2018 she was appointed by Presidential Decree as Minister Plenipotentiary of the
            First Degree and Senior Legal Counsel to the UAE Minister of Foreign Affairs, advising
            on international law, treaty practice, state-to-state disputes before international
            courts and tribunals, foreign policy and multilateral engagement.</p>

            <p>From 2019 to 2024 she served as the UAE's Deputy Permanent Representative and
            Chargé d'Affaires to the United Nations and International Organizations in Geneva,
            representing the UAE across more than forty international organisations. Her
            responsibilities included engagement on global health, humanitarian affairs, human
            rights, women and girls, education, peacebuilding and climate. She worked closely with
            the leadership of WHO, OHCHR, ITU, UNCTAD, WMO, ILO and the ICRC.</p>

            <blockquote class="pullquote">
              <p>She led the UAE's successful campaign for election to the United Nations Human
              Rights Council, and the UAE's campaign for the Presidency of the World
              Meteorological Organization — building coalitions and advancing UAE priorities
              across the international system.</p>
            </blockquote>

            <div class="signoff">
              <span class="signoff__mark">Lubna Qassim</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="wrap">
      <p class="eyebrow">At a glance</p>
      <ul class="glance">
{glance}
      </ul>
    </div>
  </section>
"""
    page("profile.html", "Profile — Lubna Qassim", body,
         "Lubna Qassim: international lawyer, senior policy leader and former senior diplomat.")


def contribution():
    items = "\n".join(f"""
      <li class="area reveal">
        <div class="area__head">
          <i class="area__num">{i+1:02d}</i>
          <div>
            <h2>{title}</h2>
            <p class="area__lede">{lede}</p>
          </div>
        </div>
        <ul class="area__list">
{chr(10).join(f'          <li>{b}</li>' for b in bullets)}
        </ul>
      </li>""" for i, (title, lede, bullets) in enumerate(AREAS))

    body = f"""
  <section class="pagehead">
    <div class="wrap">
      <p class="eyebrow">Areas of contribution</p>
      <h1 class="pagehead__title">Where I am <em>useful</em></h1>
      <p class="pagehead__note">Not a menu of services. These are the questions I am called into,
        and the rooms where a career spent on four sides of the same table earns its keep.</p>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <ol class="areas">{items}</ol>
    </div>
  </section>

  <section class="section section--paper">
    <div class="wrap">
      <p class="eyebrow">Peace diplomacy &amp; interfaith dialogue</p>
      <div class="peacestrip">
        <figure><img src="img/peace-signing.jpg" alt="" loading="lazy"></figure>
        <figure><img src="img/peace-disarm.jpg" alt="" loading="lazy"></figure>
        <figure><img src="img/peace-books.jpg" alt="" loading="lazy"></figure>
        <figure><img src="img/peace-courtyard.jpg" alt="" loading="lazy"></figure>
      </div>
      <p class="peacestrip__note">Captions, dates and venues to be confirmed.</p>
    </div>
  </section>

  <section class="section section--dark">
    <div class="wrap cta">
      <h2 class="cta__title">If one of these is your problem,<br><em>I would like to hear it.</em></h2>
      <a class="btn btn--solid" href="contact.html">Start a conversation</a>
    </div>
  </section>
"""
    page("contribution.html", "Advisory — Lubna Qassim", body,
         "Geoeconomics and global strategy; governance and institutional reform; boards and "
         "strategic advisory; women's leadership and economic participation.")


def speaking():
    themes = "\n".join(f"""
      <li class="theme reveal">
        <i>{i+1:02d}</i>
        <div><h3>{t}</h3><p>{d}</p></div>
      </li>""" for i, (t, d) in enumerate(THEMES))
    fmts = "".join(f"<li>{f}</li>" for f in FORMATS)

    body = f"""
  <section class="pagehead pagehead--img">
    <img src="img/speaking.jpg" alt="" loading="lazy">
    <div class="wrap">
      <p class="eyebrow">Speaking</p>
      <h1 class="pagehead__title">Six things worth<br>an <em>hour of a room</em></h1>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <p class="lede lede--wide">Lubna speaks on the intersection of geoeconomics, international
        affairs, governance, leadership and institutional change, drawing on more than two decades
        across government, financial services, international law and multilateral diplomacy.</p>

      <ol class="themes">{themes}</ol>

      <div class="formats">
        <p class="eyebrow">Formats</p>
        <ul class="formats__list">{fmts}</ul>
        <p class="formats__note">Keynotes are only part of it. A moderated conversation, a board
          retreat or a closed-door roundtable is often the better use of me — an intelligent room
          grappling with a difficult question suits me more than a motivational speech.</p>
      </div>

      <div class="cta cta--inline">
        <a class="btn btn--solid" href="contact.html">Check availability</a>
      </div>
    </div>
  </section>
"""
    page("speaking.html", "Speaking — Lubna Qassim", body,
         "Keynotes, executive dialogues, board retreats, roundtables and moderated conversations "
         "on geoeconomics, governance and institutional change.")


def writing():
    books = "\n".join(f"""
      <article class="book reveal">
        <img src="img/{img}.jpg" alt="{html.escape(title)}" loading="lazy">
        <div>
          <h3>{title}</h3>
          <p class="book__meta">{meta}</p>
          <p class="book__pub">{pub}</p>
        </div>
      </article>""" for img, title, meta, pub in BOOKS)

    essays = "\n".join(f"""
      <li class="essay">
        <i>{date.split()[-1]}</i>
        <div>
          <h3><a href="essays/{slug}.html">{title}</a></h3>
          <p>{note}</p>
        </div>
        <span>{pub}</span>
      </li>""" for slug, title, date, pub, note in ESSAYS)

    press = "\n".join(f"""
      <li class="press">
        <i>{year}</i>
        <div><h3><a href="{url}" rel="noopener" target="_blank">{title}</a></h3>
        <p>{outlet}</p></div>
        <span aria-hidden="true">&#8599;</span>
      </li>""" for year, title, outlet, url in PRESS)

    body = f"""
  <section class="pagehead">
    <div class="wrap">
      <p class="eyebrow">Writing &amp; interviews</p>
      <h1 class="pagehead__title">Books, essays<br>and <em>conversations</em></h1>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <p class="eyebrow">Books</p>
      <div class="books">{books}</div>
    </div>
  </section>

  <section class="section section--paper">
    <div class="wrap">
      <p class="eyebrow">Essays</p>
      <p class="lede">Written for <i>The National</i> between 2008 and 2009, and published here in
        full. Several of them argued for reforms that arrived years later.</p>
      <ul class="essays">{essays}</ul>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <p class="eyebrow">Interviews &amp; press</p>
      <ul class="presslist">{press}</ul>
    </div>
  </section>
"""
    page("writing.html", "Writing &amp; interviews — Lubna Qassim", body,
         "Two co-authored books, essays on law and economic reform, and selected interviews.")


def essay_pages():
    lookup = {s: (t, d, p, n) for s, t, d, p, n in ESSAYS}
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "*.md"))):
        slug = os.path.basename(path)[:-3]
        if slug not in lookup:
            continue
        title, date, pub, note = lookup[slug]
        raw = open(path).read().split("---\n", 1)[1].strip()
        paras = [p.strip() for p in raw.split("\n\n") if p.strip()]
        # the final line of each post is the original publication credit
        paras = [p for p in paras if not p.lower().startswith("as published in")]
        body_html = "\n".join(f"            <p>{html.escape(p)}</p>" for p in paras)

        body = f"""
  <article class="essaypage">
    <header class="essaypage__head wrap">
      <p class="eyebrow"><a href="../writing.html">Essays</a></p>
      <h1>{title}</h1>
      <p class="essaypage__meta">{date} &nbsp;·&nbsp; First published in <i>{pub}</i></p>
    </header>
    <div class="wrap">
      <div class="prose prose--reading">
{body_html}
      </div>
      <p class="essaypage__foot">First published in <i>{pub}</i>, {date}.
        Republished here by the author.</p>
      <a class="link-arrow" href="../writing.html">All writing</a>
    </div>
  </article>
"""
        page(os.path.join("essays", slug + ".html"), f"{title} — Lubna Qassim",
             body, note, depth=1)


def recognition():
    items = "\n".join(f"""
      <li class="award reveal">
        {f'<img src="img/{img}.jpg" alt="" loading="lazy">' if img else '<span class="award__rule"></span>'}
        <div>
          <h2>{title}</h2>
          <p>{desc}</p>
          {f'<p class="award__date">{date}</p>' if date else ''}
        </div>
      </li>""" for title, desc, date, img in RECOGNITION)

    body = f"""
  <section class="pagehead">
    <div class="wrap">
      <p class="eyebrow">Recognition</p>
      <h1 class="pagehead__title">Selected<br><em>recognitions</em></h1>
      <p class="pagehead__note">Six, rather than everything.</p>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap"><ul class="awards">{items}</ul></div>
  </section>
"""
    page("recognition.html", "Recognition — Lubna Qassim", body,
         "Selected recognitions, including the WHO Certificate of Recognition and the Top 100 "
         "Emirati Pioneers.")


def mentorship():
    body = """
  <section class="pagehead">
    <div class="wrap">
      <p class="eyebrow">Mentorship</p>
      <h1 class="pagehead__title">One hour,<br><em>one to one</em></h1>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap">
      <div class="mentor">
        <div class="mentor__text prose">
          <p class="lede">A small number of one-to-one sessions, offered on a first-come basis.</p>

          <p>They are for people at a hinge point: moving between sectors, walking into a room where
          the rules are not written down, taking a first board seat, or returning to senior work
          after a break. I have made each of those moves myself, and I know which parts of the
          advice usually given about them are useless.</p>

          <p>An hour, in confidence, on whatever you actually need to discuss.</p>

          <div class="mentor__pledge">
            <p>All proceeds support initiatives advancing girls' education in vulnerable
            communities.</p>
          </div>

          <a class="btn btn--solid" href="contact.html">Request a session</a>
          <p class="mentor__note">Booking and payment will be handled here once the page is live.</p>
        </div>
        <figure class="mentor__img">
          <img src="img/students.jpg" alt="" loading="lazy">
        </figure>
      </div>
    </div>
  </section>
"""
    page("mentorship.html", "Mentorship — Lubna Qassim", body,
         "One-to-one mentorship sessions. All proceeds support initiatives advancing girls' "
         "education in vulnerable communities.")


def gallery():
    items = "\n".join(f"""
      <figure class="mosaic__item reveal">
        <img src="img/{img}.jpg" alt="{html.escape(cap)}" loading="lazy">
        <figcaption><span>{cap}</span><i>{where}</i></figcaption>
      </figure>""" for img, cap, where in GALLERY)

    body = f"""
  <section class="pagehead">
    <div class="wrap">
      <p class="eyebrow">Gallery</p>
      <h1 class="pagehead__title">Selected<br><em>photographs</em></h1>
    </div>
  </section>

  <section class="section section--tight">
    <div class="wrap"><div class="mosaic">{items}</div></div>
  </section>
"""
    page("gallery.html", "Gallery — Lubna Qassim", body, "Selected photographs.")


def contact():
    body = """
  <section class="section section--enquiries section--first">
    <div class="wrap">
      <div class="enq">
        <div class="enq__aside">
          <p class="eyebrow">Contact</p>
          <h1 class="section__title">Speaking, advisory<br>and other<br><em>enquiries</em></h1>
          <p class="enq__note">Enquiries are read personally. For a speaking engagement, please
            include the date, the audience and the format — it saves a round of correspondence.</p>
          <dl class="enq__meta">
            <div><dt>Representation</dt><dd>Direct</dd></div>
            <div><dt>Based</dt><dd>United Arab Emirates</dd></div>
          </dl>
        </div>

        <form class="enq__form" novalidate>
          <div class="field">
            <label for="f-name">Name</label>
            <input id="f-name" name="name" type="text" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="f-org">Organisation</label>
            <input id="f-org" name="org" type="text" autocomplete="organization">
          </div>
          <div class="field">
            <label for="f-email">Email</label>
            <input id="f-email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="f-type">Nature of enquiry</label>
            <select id="f-type" name="type">
              <option>Speaking engagement</option>
              <option>Board or advisory</option>
              <option>Mentorship session</option>
              <option>Media &amp; interviews</option>
              <option>Other</option>
            </select>
          </div>
          <div class="field field--full">
            <label for="f-msg">Details</label>
            <textarea id="f-msg" name="message" rows="4" required></textarea>
          </div>
          <div class="field field--full enq__submit">
            <button class="btn btn--solid" type="submit">Send enquiry</button>
            <p class="enq__status" role="status"></p>
          </div>
        </form>
      </div>
    </div>
  </section>
"""
    page("contact.html", "Enquiries — Lubna Qassim", body,
         "Speaking, advisory and mentorship enquiries.")


print("building:")
home(); profile(); contribution(); speaking(); writing(); essay_pages()
recognition(); mentorship(); gallery(); contact()
print("done")
