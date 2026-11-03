"""Builds the RuloSport static site. Run: python3 build.py  (writes HTML into ./site)"""
import html, os, shutil

CDN = "https://cdn.shopify.com/s/files/1/0689/4695/2354/files/"  # DemoPadel Shopify file storage
def img(name, w=1200):
    return f"{CDN}{name}&width={w}" if "?" in name else f"{CDN}{name}?width={w}"

DEMOPADEL = "https://demopadel.au/products/"
COMING_SOON = True  # set to False once the products are live on DemoPadel
SHOW_PRICES = False  # set to True to show retail prices again
YEAR = "2026"

PRODUCTS = [
    {
        "slug": "rulo-pro-overgrips", "file": "overgrips.html", "title": "Rulo Pro Overgrips", "tag": "Overgrip",
        "card_price": "From $22.00",
        "images": [("RULOProOvergripPackaging.png?v=1793702198", "Rulo Pro Overgrips 3-pack"),
                   ("rulo-site-overgrip-pack.png?v=1793702910", "Rulo Pro Overgrip pack front"),
                   ("Screenshot_2026-10-03_at_12.37.55_pm.png?v=1793702198", "Rulo Pro Overgrips"),
                   ("rulo-site-cardboard.png?v=1793702910", "Rulo overgrip packaging")],
        "variants": [("3-pack (3 grips)", "$22.00", "50804496826530")],
        "chips": [("0.6mm thin", True), ("Tacky", False), ("Tack that holds", False)],
        "desc": """<p>Tested by players and coaches. Rulo Pro Overgrips are built for players who want a locked-in feel without adding bulk to the handle.</p>
<ul><li><strong>Thin, premium feel</strong>: 0.6mm, keeps the feel of your racket's original handle</li>
<li><strong>Tacky feel</strong>: a secure, locked-in hold from the first hit</li>
<li><strong>Tack that holds</strong>: stays tacky session after session</li></ul>
<p>Sold in packs of 3 grips.</p>""",
        "specs": [("Thickness", "0.6mm"), ("Feel", "Tacky"), ("Colour", "White"), ("Pack", "3 grips")],
        "how_title": "How to regrip",
        "how": ["Remove your old overgrip and wipe the handle clean.",
                "Peel the backing and start at the butt cap with the tapered end.",
                "Wrap up the handle, overlapping each turn slightly and keeping light tension.",
                "Trim if needed and secure the end with the finishing tape."],
        "blurb": "Thin, premium feel with a tacky grip that holds. Sold in packs of 3.",
    },
    {
        "slug": "rulo-edge-lite", "file": "edge-lite.html", "title": "Rulo Edge Lite", "tag": "Edge tape · TPU",
        "card_price": "$11.99",
        "images": [("RULOEdgeLiteWhiteBlisterPack.png?v=1793702202", "Rulo Edge Lite pack"),
                   ("rulo-site-edge-lite-studio.png?v=1793702912", "Rulo Edge Lite packaging studio shot")],
        "variants": [("Single pack", "$11.99", "50804496892066")],
        "chips": [("TPU", True), ("Translucent", False), ("Frame protection", False)],
        "desc": """<p>Translucent TPU protection tape for the frame of your padel racket. Rulo Edge Lite helps protect against scuffs and wall and floor contact while keeping your racket's design visible.</p>""",
        "specs": [("Material", "TPU"), ("Colour", "Translucent"), ("Use", "Padel racket frame protection")],
        "how_title": "How to apply",
        "how": ["Clean the racket surface.", "Peel off the backing of the protection tape.",
                "Centre the tape and apply from the middle first.", "Push the sides down onto the racket.", "Replace as needed."],
        "blurb": "Translucent TPU frame protection that lets your racket's design show through.",
    },
    {
        "slug": "rulo-edge-carbon", "file": "edge-carbon.html", "title": "Rulo Edge Carbon", "tag": "Edge tape · 3K carbon",
        "card_price": "$19.99",
        "images": [("RuloEdgeLiteCarbonProtectorPack.png?v=1793702204", "Rulo Edge Carbon pack"),
                   ("Neon_Racket_Edge_Macro.png?v=1793702204", "Rulo Edge Carbon on a racket edge"),
                   ("RULO_Edge_Lite_Carbon_Racket_Close-Up.png?v=1793702203", "Rulo Edge Carbon racket close-up"),
                   ("RULO_Edge_Lite_Carbon_Protector.png?v=1793702204", "Rulo Edge Carbon protector")],
        "variants": [("Single pack", "$19.99", "50804496924834")],
        "chips": [("3K carbon", True), ("Black finish", False), ("Frame protection", False)],
        "desc": """<p>Premium 3K carbon protection tape for the frame of your padel racket. A black carbon-weave finish that protects against scuffs and wall and floor contact.</p>""",
        "specs": [("Material", "3K carbon"), ("Colour", "Black"), ("Use", "Padel racket frame protection")],
        "how_title": "How to apply",
        "how": ["Clean the racket surface.", "Peel off the backing of the protection tape.",
                "Centre the tape and apply from the middle first.", "Push the sides down onto the racket.", "Replace as needed."],
        "blurb": "Premium 3K carbon frame protection with a black carbon-weave finish.",
    },
]

def buy_url(p, variant_id):
    return f"{DEMOPADEL}{p['slug']}?variant={variant_id}"

NAV = [("about.html", "About"), ("wholesale.html", "Wholesale"), ("faq.html", "FAQ"), ("contact.html", "Contact")]

def header(active):
    shop_links = "".join(f'<a href="{p["file"]}">{p["title"]}</a>' for p in PRODUCTS)
    nav = "".join(f'<a href="{f}"{" aria-current=\"page\"" if f == active else ""}>{t}</a>' for f, t in NAV)
    mob = "".join(f'<a class="sub" href="{p["file"]}">{p["title"]}</a>' for p in PRODUCTS)
    mob_nav = "".join(f'<a href="{f}">{t}</a>' for f, t in NAV)
    return f"""<div class="announce"><div class="wrap"><a href="wholesale.html">Clubs, coaches &amp; retailers: wholesale pricing available →</a></div></div>
<header class="site-header"><div class="wrap header-inner">
  <a class="logo" href="index.html"><img src="assets/logo-rulosport.png" alt="RuloSport" width="133" height="40"></a>
  <nav class="nav" aria-label="Main">
    <div class="nav-shop"><a href="index.html#shop">Shop</a><div class="nav-drop">{shop_links}</div></div>
    {nav}
  </nav>
  <div class="header-cta"><a class="btn btn-primary" href="wholesale.html#order">Wholesale order</a></div>
  <details class="menu-toggle"><summary>Menu</summary>
    <nav class="mobile-nav" aria-label="Mobile"><a href="index.html#shop">Shop</a>{mob}{mob_nav}<a href="wholesale.html#order">Wholesale order</a></nav>
  </details>
</div></header>"""

def footer():
    shop = "".join(f'<li><a href="{p["file"]}">{p["title"]}</a></li>' for p in PRODUCTS)
    info = "".join(f'<li><a href="{f}">{t}</a></li>' for f, t in NAV)
    return f"""<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <div class="stack" style="gap:12px"><img src="assets/logo-rulosport.png" alt="RuloSport" width="113" height="34">
      <p style="font-size:14px;max-width:320px">Protect | Play | Perform. Padel overgrips and frame protection, shipped from Melbourne.</p>
      <p style="font-size:14px"><a href="mailto:sales@rulosport.com">sales@rulosport.com</a></p></div>
    <div><h4>Shop</h4><ul>{shop}</ul></div>
    <div><h4>Info</h4><ul>{info}</ul></div>
  </div>
  <div class="footer-bottom"><span>© {YEAR} RuloSport · Padel AB Pty Ltd</span><span>Protect | Play | Perform</span></div>
</div></footer>"""

def page(file, title, desc, body, active=""):
    t = "RuloSport" if file == "index.html" else f"{title} | RuloSport"
    return f"""<!doctype html>
<html lang="en-AU"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(t)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{img('rulo-site-hero.png?v=1793702912', 1200)}">
<link rel="icon" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="assets/style.css">
</head><body>
{header(active)}
<main>
{body}
</main>
{footer()}
<script src="assets/site.js"></script>
</body></html>
"""

def card(p):
    return f"""<a class="card" href="{p['file']}">
  <div class="card-img"><img src="{img(p['images'][0][0], 800)}" alt="{html.escape(p['images'][0][1])}" loading="lazy" width="800" height="800"></div>
  <span class="card-tag">{p['tag']}</span>
  <span class="card-title">{p['title']}</span>
  <span class="card-price">{" · ".join(x for x in [p['card_price'] if SHOW_PRICES else "", "Coming soon" if COMING_SOON else ""] if x)}</span>
</a>"""

WHOLESALE_CTA = """<section class="band-dark"><div class="wrap stack">
  <h2>Clubs &amp; coaches</h2>
  <p>Stock Rulo in your pro shop or kit out your academy. Wholesale pricing available.</p>
  <div class="btn-row"><a class="btn btn-primary" href="wholesale.html#order">Start a wholesale order</a><a class="btn btn-ghost-light" href="wholesale.html">How wholesale works</a></div>
</div></section>"""

def build_index():
    cards = "".join(card(p) for p in PRODUCTS)
    body = f"""<section class="hero">
  <div class="hero-media"><img src="{img('rulo-site-hero.png?v=1793702912', 1800)}" alt="Rulo edge tape on a padel racket" width="1672" height="941"></div>
  <div class="wrap"><div class="hero-content">
    <span class="eyebrow">Padel grips &amp; frame protection</span>
    <h1>Protect <span class="bar">|</span> Play <span class="bar">|</span> Perform</h1>
    <p>Thin, tacky overgrips and edge tape built for padel. Tested on court in Melbourne.</p>
    <div class="btn-row"><a class="btn btn-primary" href="#shop">Shop Rulo</a><a class="btn btn-ghost-light" href="wholesale.html">Wholesale</a></div>
  </div></div>
</section>
<section class="usp"><div class="wrap usp-grid">
  <div class="usp-item"><span class="usp-dot"></span><div><h4>Built for padel</h4><p>Every product designed around the padel racket</p></div></div>
  <div class="usp-item"><span class="usp-dot"></span><div><h4>Tested on court</h4><p>Developed with players and coaches</p></div></div>
  <div class="usp-item"><span class="usp-dot"></span><div><h4>Clubs &amp; coaches</h4><p>Wholesale pricing available</p></div></div>
</div></section>
<section class="section" id="shop"><div class="wrap">
  <div class="section-head"><h3>Shop Rulo</h3><a href="wholesale.html">Buying for a club? See wholesale →</a></div>
  <div class="grid-3">{cards}</div>
</div></section>
<section class="section feature"><div class="wrap feature-grid">
  <div class="stack">
    <span class="eyebrow">On court</span>
    <h2>Feel first</h2>
    <p class="lede">Protection and grip shouldn't change how your racket feels in your hand. Rulo overgrips are 0.6mm thin with a tack that holds, and our edge tape protects the frame without getting in the way.</p>
    <div class="btn-row"><a class="btn btn-secondary" href="overgrips.html">Overgrips</a><a class="btn btn-secondary" href="edge-lite.html">Edge Lite</a><a class="btn btn-secondary" href="edge-carbon.html">Edge Carbon</a></div>
  </div>
  <div class="feature-video"><video src="assets/rulo-reel.mp4" autoplay muted loop playsinline preload="metadata" aria-label="Rulo product reel"></video></div>
</div></section>
{WHOLESALE_CTA}"""
    return page("index.html", "RuloSport", "Padel overgrips and edge tape built for padel. Rulo Pro Overgrips, Edge Lite and Edge Carbon. Wholesale for clubs, coaches and retailers.", body)

def notify_section(p):
    t = p["title"]
    return f"""<section class="section feature" id="notify" style="padding-block:48px"><div class="wrap feature-grid" style="align-items:start">
  <div class="stack"><span class="eyebrow">Coming soon</span><h3>Be first to get {t}</h3>
    <p>Our first shipment is on its way to Melbourne. Leave your details and we'll email you as soon as {t} is available to buy.</p></div>
  <form class="form" data-rulo-form data-subject="Register interest – {t}" data-success="Thanks, you're on the list. We'll email you as soon as {t} is in stock." style="background:var(--white)">
    <input type="hidden" name="Product" value="{t}">
    <div class="field"><label for="n-name">Name</label><input id="n-name" name="Name" required autocomplete="name"></div>
    <div class="field"><label for="n-email">Email</label><input id="n-email" type="email" name="email" required autocomplete="email"></div>
    <div class="full stack" style="gap:10px"><button class="btn btn-primary" type="submit">Notify me</button><p class="form-status" role="status" aria-live="polite"></p></div>
  </form>
</div></section>"""

def build_product(p):
    imgs = p["images"]
    thumbs = "".join(f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-src="{img(n, 1200)}" data-alt="{html.escape(a)}"><img src="{img(n, 200)}" alt="" loading="lazy"></button>' for i, (n, a) in enumerate(imgs))
    v0 = p["variants"][0]
    if len(p["variants"]) > 1:
        opts = "".join(f'<label><input type="radio" name="pack" value="{html.escape(t)}" {f' data-price="{pr}"' if SHOW_PRICES else ""} data-url="{buy_url(p, vid)}"{" checked" if i == 0 else ""}><span>{t}</span></label>' for i, (t, pr, vid) in enumerate(p["variants"]))
        variants = f'<fieldset class="variants" data-variants><legend>Pack size</legend><div class="variant-opts">{opts}</div></fieldset>'
    else:
        variants = ""
    chips = "".join(f'<span class="chip{" accent" if a else ""}">{t}</span>' for t, a in p["chips"])
    specs = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in p["specs"])
    how = "".join(f"<li>{s}</li>" for s in p["how"])
    others = "".join(card(o) for o in PRODUCTS if o is not p)
    body = f"""<div class="wrap">
<div class="pdp">
  <div data-gallery>
    <div class="gallery-main"><img src="{img(imgs[0][0], 1200)}" alt="{html.escape(imgs[0][1])}" width="1200" height="1200"></div>
    <div class="thumbs">{thumbs if len(imgs) > 1 else ""}</div>
  </div>
  <div class="pdp-info">
    <span class="eyebrow">{p['tag']}</span>
    <h1>{p['title']}</h1>
    {f'<p class="price" data-price>{v0[1]} <small>AUD inc GST</small></p>' if SHOW_PRICES else ""}
    <div class="chips">{chips}</div>
    {variants}
    <div class="btn-row">
      {'<a class="btn btn-primary" href="#notify">Coming soon: register interest</a>' if COMING_SOON else f'<a class="btn btn-primary" data-buy href="{buy_url(p, v0[2])}" target="_blank" rel="noopener">Buy now at DemoPadel</a>'}
      <a class="btn btn-secondary" href="wholesale.html#order">Order wholesale</a>
    </div>
    <ul class="trust">
      <li>Designed for padel, tested by players and coaches</li>
      <li>{"Launching soon. Register and we'll email you as soon as it's in stock" if COMING_SOON else "Secure checkout through DemoPadel, our Melbourne retail partner"}</li>
      <li>Clubs &amp; coaches: <a href="wholesale.html">wholesale pricing available</a></li>
    </ul>
    <div class="desc">{p['desc']}</div>
  </div>
</div>
</div>
{notify_section(p) if COMING_SOON else ""}
<section class="pdp-more"><div class="wrap pdp-detail">
  <div><h3>Specs</h3><table class="specs"><tbody>{specs}</tbody></table></div>
  <div class="how"><h3>{p['how_title']}</h3><ol>{how}</ol></div>
  <div class="cta-box"><h3>Wholesale</h3><p>Stocking Rulo in your club or pro shop, or kitting out an academy? We offer wholesale pricing for clubs, coaches and retailers.</p><a class="btn btn-primary" href="wholesale.html#order">Start a wholesale order</a></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><h3>Complete your setup</h3></div>
  <div class="grid-3">{others}</div>
</div></section>"""
    plain_desc = p["blurb"]
    return page(p["file"], p["title"], plain_desc, body)

def build_about():
    tiles = "".join(f'<div class="tile"><h4>{p["title"]}</h4><p>{p["blurb"]}</p><a href="{p["file"]}">Shop {p["title"].replace("Rulo ", "").replace("Pro ", "")} →</a></div>' for p in PRODUCTS)
    body = f"""<div class="wrap">
<div class="page-head"><span class="eyebrow">About RuloSport</span><h1>About</h1>
<p class="lede"><strong>Protect | Play | Perform.</strong> RuloSport makes overgrips and frame protection designed specifically for padel.</p>
<p style="max-width:70ch">We started on the courts in Melbourne, testing gear with players and coaches and asking a simple question: why are accessories so often an afterthought? Rulo is our answer. Thin, tacky grips that keep the feel of your racket, and edge tape that protects your frame without getting in the way.</p></div>
<div class="page-body">
  <section><h2>What we make</h2><div class="tiles">{tiles}</div></section>
  <section><h2>What we care about</h2><div class="tiles">
    <div class="tile plain"><h4>Built for padel</h4><p>Every product is designed around the padel racket, not adapted from another sport.</p></div>
    <div class="tile plain"><h4>Tested on court</h4><p>We develop and test with players and coaches before anything goes on sale.</p></div>
    <div class="tile plain"><h4>Feel first</h4><p>Protection and grip shouldn't change how your racket feels in your hand.</p></div>
  </div></section>
  <div class="cta-box"><h3>Protect | Play | Perform</h3><p>Grips and edge tape, shipped from Melbourne.</p><a class="btn btn-primary" href="index.html#shop">Shop all</a></div>
</div></div>"""
    return page("about.html", "About", "RuloSport makes overgrips and frame protection designed specifically for padel, tested on court in Melbourne.", body, "about.html")

def build_faq():
    def q(question, answer, open_=False):
        return f'<details{" open" if open_ else ""}><summary>{question}</summary><div>{answer}</div></details>'
    body = f"""<div class="wrap">
<div class="page-head"><span class="eyebrow">Help</span><h1>FAQ</h1><p class="lede">Quick answers about our grips, edge tape and wholesale.</p></div>
<div class="page-body faq">
  <section><h2>Overgrips</h2><div>
    {q("How thin are Rulo Pro Overgrips?", "0.6mm. They add grip without noticeably building up the handle, so your racket keeps the feel you're used to.", True)}
    {q("How often should I change my overgrip?", "It depends on how often you play. Change it when it starts to feel slippery, shiny or worn. For frequent players that's often every few weeks.")}
    {q("Will they fit my racket?", "Yes. Overgrips wrap over your racket's existing handle, so they fit any padel racket.")}
  </div></section>
  <section><h2>Edge tape</h2><div>
    {q("What's the difference between Edge Lite and Edge Carbon?", "<strong>Edge Lite</strong> is translucent TPU. It protects your frame while letting your racket's design show through. <strong>Edge Carbon</strong> is our premium option with a black 3K carbon finish.")}
    {q("Why use edge tape?", "Padel rackets regularly take knocks from walls, glass and the floor. Edge tape adds a protective layer around the frame to help reduce chips and scuffs.")}
    {q("How do I apply it?", "<ol><li>Clean the racket surface.</li><li>Peel off the backing of the protection tape.</li><li>Centre the tape and apply from the middle first.</li><li>Push the sides down onto the racket.</li><li>Replace as needed.</li></ol>")}
  </div></section>
  <section><h2>Orders &amp; wholesale</h2><div>
    {q("Where do I buy Rulo?", "Rulo is launching soon through DemoPadel, our Melbourne retail partner, and at Prelli. Our first shipment is on its way. <a href='index.html#shop'>Pick a product</a> and register your interest, and we'll email you when it's in stock." if COMING_SOON else "Retail orders go through DemoPadel, our Melbourne retail partner. Every product page has a <strong>Buy now at DemoPadel</strong> button. You can also find Rulo at Prelli.")}
    {q("Do you sell to clubs and coaches?", 'Yes. See our <a href="wholesale.html">Wholesale</a> page or <a href="wholesale.html#order">start an order</a>.')}
    {q("Is there a minimum wholesale order?", 'Yes. The minimum is 24 units of each product you order. You can order one product or mix all three.')}
  </div></section>
  <div class="cta-box"><h3>Still have a question?</h3><p>We're happy to help.</p><a class="btn btn-primary" href="contact.html">Contact us</a></div>
</div></div>"""
    return page("faq.html", "FAQ", "Answers about Rulo Pro Overgrips, Edge Lite and Edge Carbon edge tape, and wholesale orders.", body, "faq.html")

def build_wholesale():
    rows = ["Rulo Pro Overgrips (3-pack)", "Rulo Edge Lite", "Rulo Edge Carbon"]
    qty_rows = "".join(f'<tr><td>{html.escape(r)}</td><td><input type="number" min="0" step="1" inputmode="numeric" id="qty-{i}" name="Qty – {html.escape(r)}" aria-label="Quantity of {html.escape(r)}" placeholder="24+"></td></tr>' for i, r in enumerate(rows))
    body = f"""<div class="wrap">
<div class="page-head"><span class="eyebrow">Clubs · Coaches · Retailers</span><h1>Wholesale</h1>
<p class="lede">Stock Rulo in your pro shop, kit out your academy, or add padel accessories to your range.</p>
<p>We supply Rulo Pro Overgrips, Rulo Edge Lite and Rulo Edge Carbon at wholesale pricing.</p></div>
<div class="page-body">
  <section><h2>Who it's for</h2><div class="tiles">
    <div class="tile"><h4>Clubs &amp; pro shops</h4><p>Grips and edge tape your members will reach for at the counter.</p></div>
    <div class="tile"><h4>Coaches &amp; academies</h4><p>Keep your players' rackets gripped and protected session to session.</p></div>
    <div class="tile"><h4>Sports retailers</h4><p>A focused padel accessories range with clear tier positioning.</p></div>
  </div></section>
  <section><h2>How it works</h2><div class="steps">
    <div class="step"><h4>Send your order</h4><p>Fill in the form below with your business details and quantities. Minimum order is 24 units per product.</p></div>
    <div class="step"><h4>Get your invoice</h4><p>We confirm wholesale pricing and send you an invoice.</p></div>
    <div class="step"><h4>Pay &amp; dispatch</h4><p>Orders are paid 100% upfront and dispatched once payment is received.</p></div>
  </div></section>
  <section id="order"><h2>Wholesale order form</h2>
  <form class="form" data-rulo-form data-needs-qty data-moq="24" data-subject="Wholesale order" data-success="Thanks, your order request is in. We'll confirm pricing and send an invoice within one business day.">
    <div class="field"><label for="w-business">Business name</label><input id="w-business" name="Business name" required autocomplete="organization"></div>
    <div class="field"><label for="w-abn">ABN (optional)</label><input id="w-abn" name="ABN" inputmode="numeric"></div>
    <div class="field"><label for="w-name">Contact name</label><input id="w-name" name="Contact name" required autocomplete="name"></div>
    <div class="field"><label for="w-type">Business type</label><select id="w-type" name="Business type" required><option value="">Choose one</option><option>Club / pro shop</option><option>Coach / academy</option><option>Sports retailer</option><option>Other</option></select></div>
    <div class="field"><label for="w-email">Email</label><input id="w-email" type="email" name="email" required autocomplete="email"></div>
    <div class="field"><label for="w-phone">Phone</label><input id="w-phone" type="tel" name="Phone" autocomplete="tel"></div>
    <div class="field full"><label for="w-address">Delivery address</label><input id="w-address" name="Delivery address" required autocomplete="street-address"></div>
    <div class="field full"><span style="font-size:13px;font-weight:700">Products and quantities <span style="font-weight:500;color:var(--muted)">(minimum 24 units of each product you order)</span></span>
      <div class="table-scroll"><table class="qty-table"><thead><tr><th>Product</th><th>Quantity</th></tr></thead><tbody>{qty_rows}</tbody></table></div></div>
    <div class="field full"><label for="w-notes">Notes (optional)</label><textarea id="w-notes" name="Notes"></textarea></div>
    <div class="full stack" style="gap:10px"><button class="btn btn-primary" type="submit">Send order request</button>
      <p class="form-note">No payment is taken here. We'll confirm pricing and send an invoice. Orders are paid 100% upfront.</p>
      <p class="form-status" role="status" aria-live="polite"></p></div>
  </form></section>
</div></div>"""
    return page("wholesale.html", "Wholesale", "Wholesale Rulo overgrips and edge tape for padel clubs, coaches and retailers. Send an order request online.", body, "wholesale.html")

def build_contact():
    body = """<div class="wrap">
<div class="page-head"><span class="eyebrow">Contact</span><h1>Get in touch</h1>
<p class="lede">Questions about a product, an order or wholesale? Send us a message or email <a href="mailto:sales@rulosport.com"><strong>sales@rulosport.com</strong></a>.</p>
<p>Clubs and coaches, see our <a href="wholesale.html">wholesale page</a>.</p></div>
<div class="page-body"><section>
<form class="form" data-rulo-form data-subject="Website enquiry">
  <div class="field"><label for="c-name">Name</label><input id="c-name" name="Name" required autocomplete="name"></div>
  <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required autocomplete="email"></div>
  <div class="field full"><label for="c-msg">Message</label><textarea id="c-msg" name="Message" required></textarea></div>
  <div class="full stack" style="gap:10px"><button class="btn btn-primary" type="submit">Send message</button><p class="form-status" role="status" aria-live="polite"></p></div>
</form></section></div></div>"""
    return page("contact.html", "Contact", "Contact RuloSport about products, orders or wholesale.", body, "contact.html")

def main():
    out = "site"
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(out)
    shutil.copytree("assets", f"{out}/assets")
    pages = {"index.html": build_index(), "about.html": build_about(), "faq.html": build_faq(),
             "wholesale.html": build_wholesale(), "contact.html": build_contact()}
    for p in PRODUCTS: pages[p["file"]] = build_product(p)
    pages["404.html"] = page("404.html", "Page not found", "Page not found", '<div class="wrap page-head" style="padding-block:96px"><span class="eyebrow">404</span><h1>Page not found</h1><p class="lede">That page doesn\'t exist. <a href="index.html">Back to the home page</a>.</p></div>')
    for name, content in pages.items():
        open(f"{out}/{name}", "w").write(content)
    open(f"{out}/CNAME", "w").write("rulosport.com\n")
    open(f"{out}/.nojekyll", "w").write("")
    print("built", len(pages), "pages")

if __name__ == "__main__":
    main()
