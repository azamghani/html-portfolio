"""Apply the reviewed v3 content to the exact v2 IIPLA preview. Standard library only.
Changes only the supplied HTML; no network requests and no lead collection.
"""
from pathlib import Path
import re
import sys
import hashlib

BASE_SHA256 = '99a1196e0d5a9576840082f2ef346a314851d845f41536a5fba3a6779fb8eeda'
ARROW = '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'

def build(source: str) -> str:
    text = source
    def one(old: str, new: str):
        nonlocal text
        count = text.count(old)
        if count != 1:
            raise ValueError(f'Expected one occurrence, got {count}: {old[:110]}')
        text = text.replace(old, new, 1)
    def sub(pattern: str, replacement: str):
        nonlocal text
        text, count = re.subn(pattern, lambda _: replacement, text, flags=re.S)
        if count != 1:
            raise ValueError(f'Expected one replacement, got {count}: {pattern[:110]}')

    one('<title>IIPLA Patent Brokerage | Sell Your Patent Portfolio</title>',
        '<title>IIPLA Patent Brokerage | Patent Sales, Licensing &amp; Monetization</title>')
    one('Explore a potential sale or licensing opportunity for your patent portfolio. Submit a non-confidential enquiry to IIPLA Patent Brokerage. Global patent owners. U.S.-market focus.',
        'Sell your patents, license your technology or explore a monetization partnership. IIPLA supports portfolio review, buyer-ready materials and targeted outreach. Start with a non-confidential enquiry.')
    one('</head>', '<meta name="iipla-preview-version" content="3.0-2026-09-22"><meta property="og:title" content="IIPLA Patent Brokerage | More ways to monetize your patents"><meta property="og:description" content="Patent sales, licensing and structured monetization partnerships. Explore your options with IIPLA."><meta property="og:type" content="website"></head>')
    one('IIPLA PATENT BROKERAGE &nbsp; / &nbsp; GLOBAL OWNERS. U.S. MARKET FOCUS.',
        'IIPLA PATENT BROKERAGE &nbsp; / &nbsp; SALES. LICENSING. PARTNERSHIPS.')
    one('<a href="#technologies">Technologies</a>', '<a href="#options">Your options</a><a href="#technologies">Technologies</a>')

    hero = '''<div class="hero-copy"><div class="eyebrow">Patent sales · Licensing · Monetization</div>
<h1 id="hero-title">Your patents.<br><span>More ways<br>to monetize.</span></h1>
<p class="hero-lede">Sell your patents. License your technology.<br>Build a monetization partnership.</p>
<p class="hero-description">From portfolio review and buyer-ready materials to targeted outreach, IIPLA helps you explore the right route for your patents.</p>
<div class="hero-actions"><a class="btn btn-primary" href="#start" data-start data-cta="hero">Explore my options ''' + ARROW + '''</a><a class="text-link" href="#process">See how it works <span aria-hidden="true">↗</span></a></div>
<div class="hero-proof"><span><span class="proof-check" aria-hidden="true">✓</span> Owners worldwide</span><span><span class="proof-check" aria-hidden="true">✓</span> U.S. market focus</span><span><span class="proof-check" aria-hidden="true">✓</span> No public listing</span></div>
<div class="hero-route"><div class="route-label">A brokerage service. Not a marketplace.</div><p>One point of coordination for review, preparation and buyer engagement. You stay in control of the terms.</p></div></div>'''
    sub(r'<div class="hero-copy">.*?(?=<div class="lead-card")', hero)
    one('Start your portfolio review.', 'Start with a conversation.')
    one('Tell us how to reach you. Patent details can follow.', 'Tell us how to reach you. Your patent details can follow.')
    text = text.replace('Request portfolio review', 'Discuss my patent portfolio')
    text = text.replace('Submit your portfolio', 'Discuss your portfolio')
    one('Give the review<br>a head start.', 'Give your portfolio<br>a stronger start.')
    one('Your enquiry can start with a conversation. Add these details now when you have them—there is no need for a polished sales deck.',
        'A patent list and an outline of existing rights or restrictions help us assess the opportunity. Start with public information; detailed diligence comes later.')
    one('Tell us about the portfolio.', 'Share the assets. Flag the restrictions.')
    one('Required fields apply only when you choose to add portfolio details.',
        'This step is optional. When you complete it, identify the owner, preferred route and any existing rights or restrictions. “Not sure” is an accepted answer.')
    one('Public patent / application references', 'Asset list: public patent / application references')
    one('Provide public references, attach a public list, or request a conversation below.',
        'Include patent or application numbers and countries. Paste the list, attach it below, or request a conversation before sharing references.')
    one('Portfolio list <span class="optional">(optional)</span>', 'Non-confidential asset list <span class="optional">(optional)</span>')
    one('Preferred outcome <span class="required" aria-hidden="true">*</span>',
        'Preferred route <span class="required" aria-hidden="true">*</span>')
    sub(r'<select id="transaction-goal".*?</select>', '''<select id="transaction-goal" name="transactionGoal" required><option value="discuss">Open to the best fit</option><option value="sale">Sell the patents</option><option value="license">License the patents</option><option value="partnership">Explore a monetization partnership</option><option value="either">Sale or licensing</option></select><small>Ownership structure and payment terms are considered separately.</small>''')
    sub(r'<div class="field"><label for="representation">.*?</select></div>', '')
    sub(r'<div class="field"><label for="encumbrances">.*?</select></div>', '')
    disclosure = '''<div class="disclosure-block"><h3>Rights &amp; restrictions</h3><p>Existing obligations can affect a sale or licence. A high-level answer is enough here—do not share confidential agreements.</p><div class="fields">
<div class="field"><label for="representation">Existing broker / sales mandate <span class="required" aria-hidden="true">*</span></label><select id="representation" name="existingRepresentation" required><option value="">Select an answer</option><option value="none">No current representation</option><option value="non-exclusive">Non-exclusive representation</option><option value="exclusive">Exclusive mandate — review needed</option><option value="unsure">Not sure</option></select></div>
<div class="field"><label for="encumbrances">Licences or other restrictions <span class="required" aria-hidden="true">*</span></label><select id="encumbrances" name="encumbrances" required><option value="">Select an answer</option><option value="none-known">None known</option><option value="yes">Yes — details to discuss</option><option value="unsure">Not sure</option></select><small>Often called “encumbrances”: existing licences, security interests, ownership claims or other commitments.</small></div>
<div class="field full"><label for="restrictions-summary">Anything the review team should know? <span class="optional">(optional)</span></label><textarea id="restrictions-summary" name="restrictionsSummary" maxlength="2000" placeholder="For example: an existing licence, joint ownership, a lender's security interest, a dispute or a prior exclusivity commitment. A non-confidential summary only."></textarea></div>
<div class="field full"><label for="payment-preference">Preferred payment structure <span class="optional">(optional)</span></label><select id="payment-preference" name="paymentPreference"><option value="discuss">Open to discussion</option><option value="upfront">One-time / upfront payment</option><option value="hybrid">Upfront + future participation (hybrid)</option><option value="backend">Future-proceeds participation only (backend)</option></select><small>Future payments may be conditional and may be zero. This is a preference, not an offer or commitment.</small></div></div></div>'''
    one('<details class="more-details">', disclosure + '<details class="more-details">')

    options = '''<section class="section monetization-options" id="options" aria-labelledby="options-title"><div class="wrap"><div class="section-heading"><div><div class="eyebrow">Choose the route, not just the price</div><h2 id="options-title">Selling is one option.<br>Not the only one.</h2></div><p>Your goals and the portfolio should shape the deal. We help you explore a sale, a licence or a structured partnership with a suitable counterparty.</p></div>
<div class="options-grid">
<article class="option-card"><div class="option-top"><span class="option-index">01 / SELL</span><span class="option-mark" aria-hidden="true">↗</span></div><h3>Sell your patents.</h3><p>Transfer ownership of the agreed assets to a buyer. Explore a one-time payment or a sale with additional future consideration.</p><div class="ownership-note">Ownership transfers</div><a class="text-link" href="#start" data-start data-route="sale" data-cta="route-sale">Explore a sale ''' + ARROW + '''</a></article>
<article class="option-card"><div class="option-top"><span class="option-index">02 / LICENSE</span><span class="option-mark" aria-hidden="true">↔</span></div><h3>License your technology.</h3><p>Keep ownership and authorize agreed uses of your patents. Define the scope, territories, duration and commercial terms of the licence.</p><div class="ownership-note">Ownership retained</div><a class="text-link" href="#start" data-start data-route="license" data-cta="route-license">Explore licensing ''' + ARROW + '''</a></article>
<article class="option-card featured"><div class="option-top"><span class="option-index">03 / PARTNER</span><span class="option-mark" aria-hidden="true">+</span></div><h3>Build a monetization partnership.</h3><p>Retain ownership while a specialist partner pursues licensing opportunities. The structure may include exclusive sublicensing rights for named companies.</p><div class="ownership-note">Rights and exclusivity specifically agreed</div><a class="text-link" href="#start" data-start data-route="partnership" data-cta="route-partnership">Explore a partnership ''' + ARROW + '''</a></article></div>
<div class="payment-panel" aria-labelledby="payment-title"><div class="payment-heading"><div><div class="eyebrow">How the economics can work</div><h3 id="payment-title">Different ways to get paid.</h3></div><p>Payment terms are separate from ownership.</p></div><div class="payment-grid"><article><span class="payment-kicker">UPFRONT</span><h4>Value at the start.</h4><p>An agreed one-time payment at signing or closing, subject to the transaction terms.</p></article><article><span class="payment-kicker">HYBRID</span><h4>Some now. Potential later.</h4><p>An upfront payment plus agreed future payments, royalties or revenue participation.</p></article><article><span class="payment-kicker">FUTURE PROCEEDS / BACKEND</span><h4>Participation in the outcome.</h4><p>No upfront payment; participate in defined future receipts. Returns depend on actual monetization and may be zero.</p></article></div><p class="payment-note">Availability depends on the portfolio and counterparty. Payment triggers, deductions, reporting and duration must be agreed in writing. No structure, sale price or future return is guaranteed.</p></div></div></section>'''
    one('<section class="section technologies"', options + '<section class="section technologies"')
    one('Technology interests</div><h2', 'High-tech patent portfolios</div><h2')
    one('What’s in<br>your portfolio?', 'Built around technology.<br>Focused on commercial fit.')
    one('Select the technologies you own or represent.<br>We’ll carry your selections into the enquiry.<br>Matching a category is a starting point—not a purchase offer.',
        'From chips and connectivity to AI and connected systems. Select your technologies to guide the review; a category match is not a purchase commitment.')
    one('A direct enquiry. Not a public listing.', 'A focused portfolio review.')
    one('Begin a private review process, not an open-market upload.', 'Screen technical fit, territorial coverage and disclosed restrictions.')
    one('Relevant technology. Clear rights.', 'A buyer-ready story.')
    one('Assess the portfolio against the brief and its territorial coverage.', 'Turn an asset list into an approved teaser and sell-side package.')
    one('Your approval at each material step.', 'Targeted engagement.')
    one('Agree representation and disclosures before buyer outreach.', 'Reach relevant counterparties—not an indiscriminate mailing list.')

    steps = [
        ('Share the asset list', 'Start with public patent references, the owner’s identity and any licences or restrictions. Contact us first when the list is not yet ready.'),
        ('Triage the opportunity', 'Review the portfolio’s technical focus, U.S. rights and disclosed obligations. Identify questions to resolve and routes worth exploring.'),
        ('Prepare the sell-side package', 'Once scope and fees are agreed, develop an owner-approved teaser, portfolio summary and supporting materials for buyers or licensees.'),
        ('Make targeted introductions', 'Conduct approved outreach through relevant IIPLA network relationships and direct connections with prospective buyers, licensees and specialist consultants.'),
        ('Advance the transaction', 'Coordinate buyer questions, diligence and commercial negotiations. Your appointed counsel handles legal documents; you decide whether to proceed.')
    ]
    process = '<section class="section process" id="process" aria-labelledby="process-title"><div class="wrap"><div class="section-heading"><div><div class="eyebrow">More than an introduction</div><h2 id="process-title">From a patent list<br>to a prepared opportunity.</h2></div><p>We bring structure to the seller side: assess the portfolio, prepare the materials and engage relevant counterparties under an agreed mandate.</p></div><div class="process-grid">'
    for i, (title, copy) in enumerate(steps, 1):
        process += f'<article class="process-item"><div class="process-top"><span>0{i}</span>{ARROW}</div><h3>{title}</h3><p>{copy}</p></article>'
    process += '''</div><div class="process-footer"><p>You approve the engagement, permitted disclosures and any exclusivity. An initial enquiry does not appoint IIPLA, reserve a portfolio for a buyer or authorize a transaction.</p><a class="text-link" href="#start" data-start data-cta="process">Discuss the next step ''' + ARROW + '''</a></div><aside class="settlement-note"><div><span class="eyebrow">Existing licensing discussions or disputes?</span><h3>Commercial resolution can be part of the conversation.</h3><p>Where appropriate, we can help coordinate commercial settlement discussions alongside your legal counsel. Legal advice, enforcement and settlement documentation require a separate counsel engagement.</p></div><a class="text-link" href="#start" data-start data-cta="settlement">Discuss your situation ''' + ARROW + '''</a></aside></div></section>'''
    sub(r'<section class="section process".*?</section>', process)
    one('The opportunity starts<br>with the right rights.', 'Global portfolios.<br>Clear territorial rights.')

    faqs = [
      ('Is IIPLA the buyer or my broker?', 'IIPLA’s role is seller-side brokerage: helping a patent owner assess an opportunity, prepare materials and engage prospective buyers, licensees or monetization partners. IIPLA is not offering to buy your patents through this page. Representation, specialist involvement and outreach permissions are agreed in a separate engagement.'),
      ('Can I start before I have a complete patent list?', 'Yes. Submit your contact details, including a phone number with country code. The portfolio step is optional. When ready, add public patent references, the owner’s name and known restrictions. An authorized attorney, university representative or broker can enquire on the owner’s behalf. No membership purchase is required.'),
      ('What are “encumbrances,” and why do you ask?', 'They are existing rights, claims or commitments that may limit what can be sold or licensed. Examples include prior licences, sublicensing rights, a lender’s security interest, co-ownership and existing exclusivity. Also flag disputes or other relevant obligations. A non-confidential summary is enough initially; detailed documents can follow under appropriate arrangements.'),
      ('Can I keep ownership and appoint an exclusive licensing partner?', 'Yes, that is a structure we can explore. An owner may retain the patents while granting a partner defined licensing or sublicensing rights, for example for named companies. The covered patents, companies, territory, duration, retained rights, reporting and termination terms must be negotiated. It is not an automatic grant of rights to IIPLA or any buyer.'),
      ('Who pays IIPLA, and does commission cover future payments?', 'The patent owner/seller pays the agreed sell-side commission under the brokerage engagement. The agreement will define the rate and the covered proceeds from an IIPLA-originated transaction, including applicable upfront, deferred, royalty and other backend payments actually received by the owner. Commission may be paid directly or deducted and remitted from proceeds with authorization. Payment timing and any separate assessment or preparation fees are agreed in writing before the relevant work begins. This is not a claim on all of the owner’s future income.'),
      ('What should I understand about hybrid or backend arrangements?', 'An upfront payment and future participation can be combined, or a deal can depend entirely on future proceeds. Agree what counts as revenue, which costs may be deducted, who is paid first, how payments are reported and when they are due. A backend arrangement may produce no payment; IIPLA does not guarantee monetization, returns or a completion date.'),
      ('Will a buyer receive exclusivity over my portfolio?', 'Not simply because you enquire. A prospective buyer may ask for an initial review period or a time-limited exclusive negotiation window. Any restriction must be separately agreed in writing with the owner, covering the assets, scope, duration, milestones and release conditions. Submitting this form is not an exclusivity commitment.'),
      ('Will you publish my patents or send them to buyers automatically?', 'No public listing or automatic buyer forwarding is created by this enquiry. Approved outreach is targeted, and disclosure permissions and confidentiality arrangements are agreed before materials are shared. Do not submit unpublished inventions, confidential agreements, privileged advice or export-controlled material here. Discuss an NDA before any sensitive follow-up.'),
      ('Do the technology categories mean you already have a buyer?', 'The 20 priority areas reflect a supplied acquisition brief. The 12 additional categories support broader screening; they are not confirmed demand from that buyer. A category match does not establish patent strength, essentiality, value or an offer. Each portfolio and proposed transaction still needs review.'),
      ('Why is a phone number required?', 'A direct number lets IIPLA follow up about the portfolio enquiry. Include your country code. Your permission covers enquiry-related phone and email contact only—not unrelated marketing, automated marketing calls or messages, or automatic sharing with a buyer.')
    ]
    faq = '<section class="section faq" id="faq" aria-labelledby="faq-title"><div class="wrap faq-grid"><div class="faq-intro"><div class="eyebrow">Clear terms from the start</div><h2 class="section-title" id="faq-title">Your questions.<br>Answered.</h2><p>The details that matter before you share a portfolio, appoint a broker or agree a transaction.</p><a class="text-link" href="#start" data-start data-cta="faq">Talk through your options ' + ARROW + '</a></div><div class="faq-list">'
    for q, a in faqs:
        faq += f'<details><summary>{q}</summary><p>{a}</p></details>'
    faq += '</div></div></section>'
    sub(r'<section class="section faq".*?</section>', faq)
    one('Let’s find the next step<br>for your patent portfolio.', 'Your next opportunity<br>starts with a conversation.')
    one('Start with a conversation. Add the details when you’re ready.', 'A sale, a licence or a partnership. Let’s explore what fits your portfolio.')
    one('A dedicated service for patent-owner enquiries, portfolio review and U.S.-focused transaction opportunities.',
        'Patent sales, licensing and monetization partnerships. Portfolio review, preparation and targeted outreach for global owners, with a U.S. market focus.')
    one('<a href="#technologies">Technology interests</a>', '<a href="#options">Sales, licensing &amp; partnerships</a><a href="#technologies">Technology interests</a>')
    one("schemaVersion:'2.0'", "schemaVersion:'3.0'")
    one("contact:getContact(),technologies:technologies(),", "contact:getContact(),technologies:technologies(),transactionInterest:value('transaction-goal'),")
    one("noticeVersion: 'brokerage-preview-2026-09-21'", "noticeVersion: 'brokerage-preview-2026-09-22'")
    one("existingRepresentation:value('representation'),encumbrances:value('encumbrances'),timeline:value('timeline'),",
        "existingRepresentation:value('representation'),encumbrances:value('encumbrances'),restrictionsSummary:value('restrictions-summary'),paymentPreference:value('payment-preference'),timeline:value('timeline'),")
    one("['owner-name','portfolio-size','rights-status','transaction-goal']", "['owner-name','portfolio-size','rights-status','transaction-goal','representation','encumbrances']")
    one("if(p.technologyUnsure)flags.push('technology-classification-review');", "if(p.technologyUnsure)flags.push('technology-classification-review');\n    if(p.transactionGoal==='partnership')flags.push('partnership-scope-and-rights-review');\n    if(['hybrid','backend'].includes(p.paymentPreference))flags.push('future-proceeds-terms-review');")
    one("enquiryReady?showPortfolio():showContact();", "if(el.dataset.route){$('transaction-goal').value=el.dataset.route;}enquiryReady?showPortfolio():showContact();")
    one("receiptRow('Owner',p.ownerLegalName);", "receiptRow('Owner',p.ownerLegalName);receiptRow('Preferred route',labelOf('transaction-goal'));receiptRow('Payment preference',labelOf('payment-preference'));receiptRow('Restrictions',labelOf('encumbrances'));")
    styles = '\n' + Path(__file__).with_name('v3-refinements.css').read_text(encoding='utf-8')
    one('</style>', styles + '</style>')
    assert text.count('name="phone"') == 1
    assert text.count('name="encumbrances"') == 1
    assert text.count('name="existingRepresentation"') == 1
    assert "mode: 'preview'" in text and 'noindex,nofollow' in text
    return text

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python build_v3.py INPUT.html OUTPUT.html')
    inp, out = map(Path, sys.argv[1:])
    raw = inp.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA256:
        raise SystemExit('Base HTML differs from the reviewed version; reconcile before updating.')
    result = build(raw.decode('utf-8')).encode('utf-8')
    out.write_bytes(result)
    print('v3 HTML:', len(result), 'bytes; SHA256:', hashlib.sha256(result).hexdigest())
