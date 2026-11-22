import re, os, shutil, html

import pathlib
B = str(pathlib.Path(__file__).resolve().parent)
OUT = str(pathlib.Path(__file__).resolve().parent.parent / "_site")
LIGHTS = open(f"{B}/lights.html").read()
LIGHTS_L = open(f"{B}/lights_large.html").read()
EMAIL = "slavacreatives@gmail.com"


def smart(text):
    """Curly quotes in text only (never inside tags, scripts or styles)."""
    out, i = [], 0
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)", text, flags=re.S)
    prev = " "
    for p in parts:
        if not p:
            continue
        if p.startswith("<"):
            out.append(p)
            continue
        s = []
        for ch in p:
            if ch == "'":
                s.append("’" if prev.strip() and prev not in "([{— " else "‘")
            elif ch == '"':
                s.append("“" if (not prev.strip() or prev in "([{—”") else "”")
            else:
                s.append(ch)
            prev = s[-1]
        out.append("".join(s))
    return "".join(out)


def fix_quote_spans(doc):
    # In pull quotes the opening mark sits right after a tag; force correct direction.
    doc = re.sub(r'<span class="q">[“”]</span>(?=[A-Z])', '<span class="q">“</span>', doc)
    doc = re.sub(r'(?<=[.?!])<span class="q">[“”]</span>', '<span class="q">”</span>', doc)
    return doc


def page(title, body, desc="", script=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2A1A1F">
<meta name="robots" content="noindex">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Lora:ital,wght@0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="/styles.css">
<script src="/config.js"></script>
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', window.TMW.pixelId);
fbq('track', 'PageView');
</script>
</head>
<body>
<div class="simple-page">
<header class="simple-top"><a href="/">The Magnetic Wife</a>{LIGHTS}</header>
<main class="simple-main">
{body}
</main>
<footer class="simple-footer"><a href="/privacy/">Privacy</a>·<a href="/terms/">Terms</a>·<a href="/refunds/">Refunds</a>·<a href="mailto:{EMAIL}">{EMAIL}</a><br>© 2026 Happy Spouse Happy House</footer>
</div>
{script}
</body>
</html>
"""


PURCHASE_JS = """<script>
(function(){
  var C = window.TMW || {};
  var q = new URLSearchParams(location.search);
  var confirmed = q.get("payment") === "success" || q.has("session_id") || q.has("receipt_id");
  var started = 0, done = false;
  try { started = Number(localStorage.getItem("tmw:checkout-started")) || 0; done = sessionStorage.getItem("tmw:purchase") === "1"; } catch (e) {}
  var recent = started && (Date.now() - started) < 2 * 60 * 60 * 1000;
  if (done || !(confirmed || recent) || typeof fbq !== "function") return;
  fbq("track", "Purchase", { content_name: "The Magnetic Wife", content_ids: "the-magnetic-wife", content_type: "product", value: C.value || 55, currency: "USD", num_items: 1 });
  try { sessionStorage.setItem("tmw:purchase", "1"); localStorage.removeItem("tmw:checkout-started"); } catch (e) {}
})();
</script>"""

THANKS = f"""
<span class="simple-badge">Payment complete</span>
<h1>Welcome. Your Magnetic Wife bundle is on its way.</h1>
<p>Your purchase is confirmed. Everything is sent to the email address you used at checkout.</p>
<div class="simple-card">
<h2 style="margin-top:0">What happens next</h2>
<ol>
<li><strong>Check your inbox.</strong> Look for the email from Whop with your access to the e-book, the 4-Week Playbook and the private community.</li>
<li><strong>Give it up to 15 minutes.</strong> You don't need to buy again.</li>
<li><strong>Check spam and promotions</strong> if it isn't in your main inbox.</li>
</ol>
</div>
<p>Start with Part One of the e-book tonight. Then open Week 1 of the Playbook tomorrow morning. A few minutes is all it takes.</p>
<h2>Still nothing after 15 minutes?</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> with the email address you used at checkout, and we'll sort it out.</p>
<p class="simple-meta">Your 30-day guarantee starts today. If it isn't worth it, email us for a full refund. No form, no explanation.</p>
"""

WAITLIST = """
<span class="simple-badge">You're on the list</span>
<h1>Thank you. We'll let you know.</h1>
<p>We've saved your email. When the Hardcover Edition is available again, you'll be among the first to hear.</p>
<p>In the meantime, the digital bundle is available right now.</p>
<p><a class="letter-button" href="/#offer" style="color:#FFF8ED">Back to the bundle →</a></p>
"""


def legal(title, intro, sections):
    body = f'<h1>{title}</h1><p>{intro}</p><p class="simple-meta">Last updated November 19, 2026 · Questions? <a href="mailto:{EMAIL}">{EMAIL}</a></p>'
    for h, ps in sections:
        body += f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps)
    body += '<p class="simple-meta">This page is meant to make the agreement easier to understand. It is not legal advice.</p>'
    return body

M = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
TERMS = legal("Terms & Conditions", "The ground rules for using The Magnetic Wife and placing an order.", [
    ("About us and how to contact us", [f"The Services are provided by the operator of <strong>The Magnetic Wife</strong>. The Services are operated online. You can reach us at {M}."]),
    ("Using The Magnetic Wife", ["These Terms govern your access to and use of The Magnetic Wife website, e-book, playbook, community and related materials, together the \"Services\". By accessing the Services or placing an order, you agree to these Terms.", "You may use the Services only if you are legally able to enter into a binding agreement where you live. The Services are intended for adults."]),
    ("Orders, prices, and payment", ["Product descriptions, prices, availability, and any terms shown at checkout form part of the order process. Prices are shown in <strong>USD</strong>. Applicable taxes and charges are displayed before you submit an order where required by law. Payments are processed through <strong>Whop</strong>."]),
    ("Refunds and cancellations", [f"Our <a href=\"/refunds/\">Refund Policy</a> applies to payments for the Services. You can request a full refund within 30 days of purchase by emailing {M}. No form or explanation is required.", "Nothing in these Terms excludes, restricts, or limits a consumer guarantee, statutory warranty, cancellation right, or other protection that cannot lawfully be excluded."]),
    ("Acceptable use", ["You must not use the Services to break the law, infringe another person's rights, interfere with security or availability, introduce malicious code, impersonate another person, or use the Services for fraud, abuse, harassment, or any harmful purpose. In the community, treat other members with respect and keep what they share private."]),
    ("Not professional advice", ["The Services are educational. They are not therapy, counselling, medical, or legal advice. If your relationship involves abuse, threats, coercion or addiction, please seek professional or local support."]),
    ("Intellectual property", ["The Services and their content are owned by us or licensed to us. We grant you a limited, non-exclusive, non-transferable license to use the Services for your personal use. You must not reproduce, distribute, sell, or create derivative works from our content unless permitted by law or by written permission."]),
    ("Disclaimers and liability", ["We provide the Services with reasonable care and skill and as described at the time of purchase. We can't promise any particular result in your relationship. To the maximum extent permitted by law, we are not liable for indirect or consequential loss. These limits do not apply to liability that cannot legally be limited or to your non-waivable consumer rights."]),
    ("Governing law and disputes", [f"These Terms are governed by the laws that apply to the operator of the Services, unless mandatory consumer law in your place of residence requires otherwise. Before formal proceedings, contact us at {M} and give us a reasonable opportunity to respond."]),
    ("Changes and contact", [f"We may update these Terms to reflect changes to the Services, law, or business operations. The updated version will be posted on this page with a new date. Questions can be sent to {M}."]),
])
PRIVACY = legal("Privacy Notice", "What we collect, why we collect it, and the choices you have.", [
    ("Who we are", [f"We are the operator of <strong>The Magnetic Wife</strong>, an online relationship education resource. For privacy questions or requests, contact {M}."]),
    ("Information we collect", ["Depending on how you interact with us, we may collect your name, email address, billing details, order history, payment status, support messages, marketing preferences, and information you choose to provide through forms, including the hardcover waitlist.", "We may also collect device and usage information such as IP address, browser type, pages viewed, referring pages, and interaction data."]),
    ("How we use information", ["We use personal information to provide the Services, process payments, deliver your purchase, communicate with you, provide support, maintain security, prevent fraud, improve the Services, send updates you asked for (such as hardcover availability), comply with law, and enforce agreements."]),
    ("Cookies and advertising", ["We use the Meta Pixel to measure how our ads perform, for example when someone views this page, starts checkout, or completes a purchase. You can manage cookies through your browser settings and your ad preferences in your Meta account."]),
    ("When we share information", ["We share personal information with service providers that host, secure, measure, support, or deliver the Services: Whop for payment processing and product access, Netlify for hosting and forms, and Meta for advertising measurement. We may also share information with professional advisers, with authorities where required by law, and with parties involved in a sale of the business."]),
    ("International transfers and retention", ["We and our service providers may process information in countries other than the one where you live. We keep information only as long as reasonably necessary to provide the Services, document transactions, respond to support requests, prevent fraud, and comply with legal obligations."]),
    ("Your privacy rights", [f"Depending on where you live, you may have the right to access, correct, delete, restrict, or object to processing of your information; withdraw consent; opt out of targeted advertising; and complain to a privacy regulator. To make a request, contact {M}."]),
    ("Children", [f"The Services are for adults and are not directed to anyone under 18. If you believe a child has given us personal information, contact {M} so we can delete it."]),
])
REFUNDS = legal("Refund Policy", "A plain 30-day refund policy, with no explanation required.", [
    ("30-day refund policy", ["You can request a full refund within 30 days of purchase. No form and no explanation are needed.", f"Email {M} from the address you used at checkout, within 30 days of purchase."]),
    ("Access and delivery issues", [f"If you paid but can't access your purchase, first check the delivery email and your spam, junk, and promotions folders. If nothing has arrived within 15 minutes, contact {M} so we can fix it."]),
    ("Legal remedies that still apply", ["If applicable law requires a remedy because a product is defective, not delivered, or materially different from its description, we will provide the remedy required by law. This policy does not exclude or limit any right that cannot legally be excluded where you live."]),
])


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(content)


os.makedirs(OUT, exist_ok=True)
if os.path.exists(OUT):
    for f in os.listdir(OUT):
        if f not in ("bundle.webp", "bundle.jpg", "og-image.jpg"):
            p = os.path.join(OUT, f)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

idx = open(f"{B}/index.src.html").read().replace("{{LIGHTS_LARGE}}", LIGHTS_L).replace("{{LIGHTS}}", LIGHTS)
idx = fix_quote_spans(smart(idx))
write("index.html", idx)
write("thank-you/index.html", smart(page("Purchase confirmed | The Magnetic Wife", THANKS, "Your Magnetic Wife purchase is confirmed.", PURCHASE_JS)))
write("waitlist/index.html", smart(page("You're on the list | The Magnetic Wife", WAITLIST)))
write("terms/index.html", smart(page("Terms & Conditions | The Magnetic Wife", TERMS)))
write("privacy/index.html", smart(page("Privacy Notice | The Magnetic Wife", PRIVACY)))
write("refunds/index.html", smart(page("Refund Policy | The Magnetic Wife", REFUNDS)))
write("styles.css", open(f"{B}/base-letter.css").read() + open(f"{B}/extra.css").read())
shutil.copy(f"{B}/config.js", f"{OUT}/config.js")
shutil.copy(f"{B}/site.js", f"{OUT}/site.js")
write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#2A1A1F"/><circle cx="32" cy="34" r="12" fill="#E8B65C"/></svg>')
write("_redirects", """/honeymoon            /              301
/honeymoon/           /              301
/honeymoon/thank-you  /thank-you/    301
/honeymoon/terms      /terms/        301
/honeymoon/privacy    /privacy/      301
/honeymoon/refunds    /refunds/      301
/refund-policy        /refunds/      301
/pricing              /#offer        301
/honeymoon/pricing    /#offer        301
""")

print("built")
