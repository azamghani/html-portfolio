from pathlib import Path
import re,json,hashlib,html
import sys
base=Path(sys.argv[1]).read_text()
s=base
ops=[]
def rep(old,new,count=None):
 global s
 n=s.count(old)
 assert n>0, 'NOT FOUND: '+old[:160]
 if count is not None: assert n==count,(old[:100],n,count)
 ops.append({'old':old,'new':new,'count':n})
 s=s.replace(old,new)
def match(pattern,new):
 m=re.search(pattern,s,re.S);assert m,pattern
 rep(m.group(0),new,1)
def text_element(id,tag,new):
 match(r'<'+tag+r'\b[^>]*\bid="'+re.escape(id)+r'"[^>]*>.*?</'+tag+r'>',new)
arrow='<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'
# Public service identity and versioned consent; configuration remains fail-closed.
for old,new in [
 ('IIPLA Patent Monetization','IIPLA Patent Brokerage'),
 ('IIPLA PATENT MONETIZATION','IIPLA PATENT BROKERAGE'),
 ('Patent<br>Monetization','Patent<br>Brokerage'),
 ('6.0-patent-rights','7.0-patent-sales'),
 ('patent-monetization-2026-09-22-v2','patent-brokerage-2026-09-22-v1'),
 ('PM-2026-09-22-2','PB-2026-09-22-1'),
 ('BP-2026-09-22-2','PB-BUYER-2026-09-22-1'),
 ('patent-monetization-enquiry','patent-sale-enquiry'),
 ('iipla-patent-monetization','iipla-patent-brokerage'),
 ('buyer-partner-enquiry','patent-buyer-enquiry'),
 ("schemaVersion:'4.0'","schemaVersion:'7.0'"),
 ("schemaVersion:'1.0'","schemaVersion:'2.0'"),
]:rep(old,new)
match(r'<title>.*?</title>','<title>IIPLA Patent Brokerage | Sell Your Patents</title>')
match(r'<meta name="description"[^>]*>','<meta name="description" content="Looking to sell your patents? IIPLA Patent Brokerage helps patent owners prepare their portfolios, develop a sell-side package and reach relevant buyers. Start a non-confidential enquiry.">')
rep('PATENT SALES. IP LICENSING. PARTNERSHIPS.','PATENT SALES. SELLER-SIDE REPRESENTATION.')
rep('href="#options">Your options','href="#options">Our service')
rep('Patent sales · IP licensing · Partnerships','Patent sales · Seller-side brokerage')
text_element('hero-title','h1','<h1 id="hero-title">Ready to sell<br><span>your patents?</span></h1>')
rep('Sell your patents. License your IP.<br>Build a monetization partnership.','A focused service.<br>From patent portfolio to buyer discussions.')
rep('IIPLA helps patent owners prepare their portfolios, reach relevant buyers and licensees, and pursue transactions in patent rights.','We help patent owners organize their portfolio, prepare a sell-side package and connect with relevant buyers. You decide whether to accept an offer.')
rep('Explore my options','Discuss a patent sale')
rep('Patent rights. A focused monetization service.','A broker on the seller’s side.')
rep('Direct sales, direct IP licences and licensing partnerships. You stay in control of the patents, disclosures and terms until an agreement says otherwise.','We facilitate patent sales. You retain ownership until a sale is completed under signed agreements. An enquiry does not appoint us or commit you to sell.')
rep('Tell us how to reach you. Your patent details can follow.','Interested in selling? Start with your contact details. Your patent list can follow.')
# One service, described through three deliverables rather than three monetization routes.
services='''<section class="section monetization-options sales-services" id="options" aria-labelledby="options-title"><div class="wrap"><div class="section-heading"><div><div class="eyebrow">One focus. Patent sales.</div><h2 id="options-title">Your portfolio.<br>Prepared for the market.</h2></div><p>We work on the seller’s side of a patent sale: organizing the opportunity, preparing approved materials and coordinating discussions with prospective buyers.</p></div><div class="options-grid">
'''
for n,title,desc,foot in [
 ('01 / REVIEW','Start with the assets.','Bring together the patent list, stated ownership, territorial coverage and known restrictions. Identify gaps and questions that need specialist review.','A clear starting point'),
 ('02 / PREPARE','Build the sale package.','Prepare an asset schedule, a non-confidential teaser and supporting information within the agreed scope. You approve what can be shared.','Materials you approve'),
 ('03 / CONNECT','Reach relevant buyers.','Coordinate targeted introductions, buyer questions and sale discussions. Your appointed counsel advises on legal documents and closing.','You decide on the offer'),
]:
 services+=f'<article class="option-card sale-service-card"><div class="option-top"><span class="option-index">{n}</span><span class="option-mark" aria-hidden="true">↗</span></div><h3>{title}</h3><p>{desc}</p><div class="ownership-tag">{foot}</div><a class="text-link" href="#start" data-start data-cta="sales-service">Discuss your portfolio {arrow}</a></article>\n'
services+='''</div><aside class="patent-scope-note" aria-labelledby="patent-scope-title"><div><span class="eyebrow">Our service scope</span><h3 id="patent-scope-title">Patent brokerage.<br>Patent sales only.</h3></div><p>IIPLA’s current offering is <strong>seller-side patent sales brokerage</strong>. We do not offer direct IP licensing, sublicensing, monetization partnerships, enforcement or technology commercialization through this service.</p></aside><div class="payment-panel" aria-labelledby="payment-title"><div class="payment-heading"><div><div class="eyebrow">A sale needs the right fit</div><h3 id="payment-title">The assets. The buyer. The terms.</h3></div><p>No automatic acceptance or promised sale price.</p></div><div class="payment-grid"><article class="payment-item"><span>THE ASSETS</span><h4>What is being sold?</h4><p>Identify the patents, family members, countries and any existing rights or restrictions.</p></article><article class="payment-item"><span>THE BUYER</span><h4>Who is a relevant prospect?</h4><p>Match the portfolio’s subject matter and scope to a buyer’s acquisition interests.</p></article><article class="payment-item"><span>THE TERMS</span><h4>What can both sides agree?</h4><p>Price, diligence, permitted disclosures and closing conditions need agreement.</p></article></div><p class="payment-note">A technology match or introductory discussion is not an offer. Any representation, fee or exclusivity arrangement requires a separate written agreement.</p></div></div></section>'''
match(r'<section class="section monetization-options" id="options".*?</section>',services)
# Keep the five-step interaction and navigation; remove any settlement/licensing service pitch.
process='''<section class="section process" id="process" aria-labelledby="process-title"><div class="wrap"><div class="section-heading"><div><div class="eyebrow">A clear sales process</div><h2 id="process-title">From your patent list<br>to buyer discussions.</h2></div><p>Start with the essentials. Agree the work before outreach. Keep control of your portfolio, disclosures and decision to sell.</p></div><div class="process-grid">'''
for n,title,desc in [
 ('01','Share your patent list','Start with public patent references, the owner’s identity and known licences or restrictions. Contact us first if the list is not ready.'),
 ('02','Screen the opportunity','Review the available information and potential fit with buyer interests. Flag questions for specialists and agree the engagement, fees and disclosure permissions.'),
 ('03','Prepare for outreach','Organize the asset schedule, non-confidential teaser and supporting material. Any deeper patent analysis is separately scoped. You approve the sale package.'),
 ('04','Introduce relevant buyers','Conduct targeted outreach through relevant IIPLA relationships and patent-market contacts. Coordinate buyer questions and interest—not a public listing or mass mailing.'),
 ('05','Support the sale process','Coordinate diligence and discussions on price and closing conditions. You decide on the offer; your appointed counsel handles legal advice and transaction documents.'),
]:process+=f'<article class="process-item"><div class="process-step"><span>{n}</span>{arrow}</div><h3>{title}</h3><p>{desc}</p></article>'
process+='''</div><div class="process-bottom"><p>You approve the engagement, permitted disclosures and any exclusivity. An initial enquiry does not appoint IIPLA, reserve a portfolio or authorize a sale.</p><a class="text-link" href="#start" data-start data-cta="process">Discuss a patent sale '''+arrow+'''</a></div></div></section>'''
match(r'<section class="section process" id="process".*?</section>',process)
# Owner intake: retain its fields and two stages, but remove out-of-scope offers.
rep('This step is optional. When you complete it, identify the owner, preferred route and any existing rights or restrictions. “Not sure” is an accepted answer.','This step is optional. When you complete it, identify the owner, your sale objective and any existing rights or restrictions. “Not sure” is an accepted answer.')
rep('Preferred route <span','Sale objective <span')
text_element('transaction-goal','select','<select id="transaction-goal" name="transactionGoal" required><option value="discuss">Discuss a potential patent sale</option><option value="sale">Find a buyer for my patents</option></select>')
rep('Ownership structure and payment terms are considered separately.','This enquiry is for selling patents, not licensing or sublicensing services.')
rep('Existing obligations can affect a sale or licence.','Existing obligations can affect a patent sale.')
rep('Preferred payment structure <span','Purchase payment preference <span')
text_element('payment-preference','select','<select id="payment-preference" name="paymentPreference"><option value="discuss">Open to discussing sale payment terms</option><option value="upfront">Prefer payment in full at closing</option></select>')
rep('Future payments may be conditional and may be zero. This is a preference, not an offer or commitment.','Purchase price, payment timing and any conditions are agreed in the sale contract. This preference is not an offer.')
rep("    if(p.transactionGoal==='partnership')flags.push('partnership-scope-and-rights-review');\n",'')
rep("    if(['hybrid','backend'].includes(p.paymentPreference))flags.push('future-proceeds-terms-review');\n",'')
rep("if(el.dataset.route){$('transaction-goal').value=el.dataset.route;}","if(el.dataset.route && ['sale','discuss'].includes(el.dataset.route)){$('transaction-goal').value=el.dataset.route;}")
rep("receiptRow('Preferred route',labelOf('transaction-goal'))","receiptRow('Sale objective',labelOf('transaction-goal'))")
rep("    if(!selected.size&&!$('technology-unsure').checked)","    if(!['sale','discuss'].includes(value('transaction-goal')) || !['discuss','upfront'].includes(value('payment-preference'))){error('portfolio-error','Choose a patent-sale objective and purchase payment preference.',$('transaction-goal'));return false;}\n    if(!selected.size&&!$('technology-unsure').checked)")
# Detailed FAQ remains 30 questions with the same anchors, groups and search behavior.
faqs=json.loads((Path(__file__).parent/'sales-faqs-v7.json').read_text())
for group,entries in faqs.items():
 for i,(q,a) in enumerate(entries,1):
  id=f'faq-{group}-{i}'
  match(r'<details\b(?=[^>]*\bid="'+id+r'")[^>]*>.*?</details>',f'<details id="{id}" data-faq-item><summary>{q}</summary><p>{a}</p></details>')
rep('Your deal options','Your patent sale')
rep('Understand the steps, your options and the terms to agree before moving forward.','Understand the patent-sale process, the information to prepare and the terms to agree before moving forward.')
# Closing CTA and buyer links remain in their existing positions.
rep('A patent sale, an IP licence or a monetization partnership. Let’s explore what fits your portfolio.','Considering a patent sale? Let’s discuss your portfolio and the next step.')
rep('Looking to acquire or license patents?','Looking to acquire patents?')
rep('Buyer &amp; Partner Enquiries','Patent Buyer Enquiries')
rep('Buyer &amp; partner enquiries','Patent buyer enquiries')
rep('Buyer &amp; Partner Enquiry','Patent Buyer Enquiry')
rep('Buyer and partner enquiry form','Patent buyer enquiry form')
rep('For buyers &amp; partners','For patent buyers')
rep('Direct patent sales, direct IP licensing and monetization partnerships. Patent portfolio review, sell-side preparation and targeted outreach. Global owners. U.S. market focus.','Seller-side brokerage for patent sales. Portfolio preparation, targeted buyer outreach and coordination through the sale process. Global owners. U.S. market focus.')
rep('<strong>Patent monetization</strong>','<strong>Patent brokerage</strong>')
rep('Patent sales, IP licensing &amp; partnerships','Patent sales brokerage')
rep('do not create representation or guarantee monetization','do not create representation or guarantee a sale')
# Seller submission notice: narrow scope without removing privacy and no-transfer protections.
rep('The service concerns direct patent sales, direct IP licensing of patent rights and patent licensing partnerships. It does not include know-how transfer, product development, technical implementation, manufacturing support or technology commercialization.','The service is seller-side brokerage for patent sales only. It does not include direct IP licensing, sublicensing, monetization partnerships, enforcement, know-how transfer, product development or technology commercialization.')
rep('A buyer or independent monetization partner does not receive your submission automatically.','A prospective buyer or independent third party does not receive your submission automatically.')
rep('Patent Monetization privacy enquiry','Patent Brokerage privacy enquiry')
rep('8. Fees and future transaction proceeds','8. Fees and patent-sale proceeds')
rep("Where agreed, the patent owner/seller pays IIPLA's commission on defined proceeds actually received from a covered IIPLA-originated transaction, including applicable upfront, deferred, royalty or other backend payments. Rates, duration, deductions, reporting and payment mechanics must be expressly agreed. This notice creates no claim over future income.","Where agreed, the patent owner/seller pays IIPLA's commission on defined purchase consideration actually received from a covered IIPLA-originated sale. The engagement must address any deferred or conditional purchase payments, rates, duration, deductions, reporting and payment mechanics. This notice creates no claim over future income or the buyer’s later exploitation of the patents.")
rep('a commitment to sell or license','a commitment to sell')
rep('Any buyer review window, exclusive negotiation period, licensing authority or monetization partnership requires a separate written agreement defining its scope and duration.','Any buyer review window or exclusive negotiation period requires a separate written agreement defining its assets, scope and duration. A sale requires its own transaction documents; submission grants no licensing or sublicensing authority.')
rep('guarantee of sale, licensing revenue or completion time. Backend payments depend on the negotiated terms and actual outcomes and may never arise.','guarantee of a sale, purchase price, payment or completion time. Any conditional purchase payments depend on the agreed terms and may never become payable.')
# Buyer contact stays a separate modal, but only for patent acquisition.
text_element('buyer-intro','p','<p id="buyer-intro">Looking to acquire patents? Tell us the patent sectors, territories and acquisition requirements you are interested in. IIPLA can discuss whether a seller’s portfolio may be a suitable fit.</p>')
text_element('buyer-interest','select','<select id="buyer-interest" name="interest" required><option value="">Select your interest</option><option value="acquisition">Acquire patents</option><option value="buyer-representative">Represent a patent buyer</option><option value="exploring">Explore a future patent acquisition</option></select>')
rep('Which patent rights or sectors are you interested in? Mention territories, purchase or IP-licensing preferences and timing, if known. Non-confidential requirements only.','Which patents or sectors are you looking to acquire? Mention territories, portfolio preferences and timing, if known. Non-confidential requirements only.')
rep('Patent acquisition or licensing requirements only. No budget required.','Patent acquisition requirements only. No budget required.')
rep('This channel covers patent acquisitions, direct IP licensing of patent rights and patent monetization partnerships, not know-how transfer or technology commercialization.','This channel is for prospective patent buyers and their representatives. It does not offer licensing, sublicensing, monetization partnerships or technology commercialization.')
rep('mention your Buyer &amp; Partner Enquiry','mention your Patent Buyer Enquiry') if 'mention your Buyer &amp; Partner Enquiry' in s else None
# Defence in depth: reject obsolete options even if a visitor injects them into a select.
needle="for(const [id,msg] of [['buyer-notice-accepted'"
rep(needle,"if(!['acquisition','buyer-representative','exploring'].includes(value('buyer-interest'))){fail('Please select a patent acquisition interest.',$('buyer-interest'));return false;}for(const [id,msg] of [['buyer-notice-accepted'")
# Small visual adjustments for the shorter hero and sales deliverables.
css='''\n/* v7: sales-only service; existing responsive forms and dialogues are retained. */
.sales-services .ownership-tag{font-size:11px;color:var(--blue);font-weight:600;margin:20px 0 16px}
.sales-services .option-card .text-link{margin-top:auto}.sales-services .option-card{display:flex;flex-direction:column}
.sales-services .payment-item>span{display:block;font-size:9px;font-weight:700;letter-spacing:.12em;color:#aec0ff;margin-bottom:10px}
.sales-services .payment-item h4{font-size:16px;line-height:1.5;margin:0 0 8px;color:#fff}
.sales-services .payment-item p{font-size:12px;line-height:1.85;color:#c5d2ed}
.hero h1{font-size:clamp(58px,5.3vw,76px)}
.process-step{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px}.process-step>span{font-size:28px;font-weight:500;color:#aec0ff}.process-step>.icon{width:18px;height:18px;color:#7f91b5}
.process-bottom{display:flex;align-items:center;justify-content:space-between;gap:32px;border-top:1px solid #3b5075;padding-top:24px;margin-top:30px}.process-bottom>p{font-size:11px;color:#c5d2ed;max-width:780px;line-height:1.9}.process-bottom .text-link{white-space:nowrap;color:#aec0ff}
@media(max-width:680px){.hero h1{font-size:54px;letter-spacing:-2.7px}.process-bottom{flex-direction:column;align-items:flex-start;gap:16px}.process-step{margin-bottom:12px}.process-step>span{font-size:24px}}
@media(max-width:365px){.hero h1{font-size:47px}}
'''
rep('</head>','<style id="sales-only-refinements">'+css+'</style></head>',1)

assert "mode: 'preview'" in s and "mode:'preview'" in s
assert 'noindex,nofollow' in s
assert len(re.findall(r'<details[^>]+data-faq-item',s))==30
assert 'Patent<br>Brokerage' in s
Path(sys.argv[2]).write_text(s)
print(hashlib.sha256(s.encode()).hexdigest())
