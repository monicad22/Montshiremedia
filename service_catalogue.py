"""Service catalogue presentation; service copy lives in content/services.json."""
from html import escape
from urllib.parse import quote

GROUPS = [
    ('strategy', 'Strategy and measurement', 'Choose the direction. Know what changes.', 'Research, priorities and connected reporting to help you make the next decision.'),
    ('reach', 'Reach and customer growth', 'Get discovered. Keep the conversation going.', 'Connect search, advertising, social and email across the customer journey.'),
    ('brand', 'Brand, content and production', 'Give people a reason to remember you.', 'Build a clear identity and turn the story into useful creative, coverage and physical touchpoints.'),
    ('build', 'Websites, apps and ongoing care', 'Build the experience behind the promise.', 'Bring design and engineering together, then keep the experience working after launch.'),
]

def service_directory(services):
    out = '<div class="service-directory" id="services-directory"><nav class="service-jump" aria-label="Service categories">'
    for slug, title, _, _ in GROUPS:
        out += f'<a href="#services-{slug}">{escape(title)}</a>'
    out += '</nav>'
    for slug, title, headline, description in GROUPS:
        out += f'<section class="section service-group" id="services-{slug}"><div class="service-group-heading"><div class="eyebrow">{escape(title)}</div><h2>{escape(headline)}</h2><p>{escape(description)}</p></div><div class="service-catalogue-grid">'
        for s in services:
            if s['group'] != slug:
                continue
            out += f'<a class="catalogue-card" href="/services/{s["slug"]}/"><h3>{escape(s["name"])}</h3><p>{escape(s["description"])}</p><span class="card-action">Explore this service</span></a>'
        out += '</div></section>'
    return out + '</div>'

def service_contact(service):
    subject = quote(service['name'] + ' enquiry')
    out = '<section class="section service-next"><div><div class="eyebrow">LET’S SHAPE THE WORK</div><h2>What would progress<br>look like for you?</h2><p>Share your goal, current setup and timeline. We will help define the next useful step.</p></div><div>'
    if service.get('scope_note'):
        out += '<h3>Agree the scope first.</h3><p>' + escape(service['scope_note']) + '</p>'
    out += f'<a class="button" href="mailto:info@montshiremedia.ca?subject={subject}">Discuss this service</a><p class="service-return"><a class="text-link" href="/services/">View all services</a></p></div></section>'
    return out
