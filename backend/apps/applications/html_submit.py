from __future__ import annotations
from typing import Dict, Tuple, Any
from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup


def discover_form(html: str, base_url: str) -> Tuple[str, str, Dict[str, Any], list[str]]:
    soup = BeautifulSoup(html, 'lxml')
    forms = soup.find_all('form')
    candidate = None
    score = -1
    for f in forms:
        s = 0
        text = ' '.join([f.get('id', ''), f.get('name', ''), f.get('class', [''])[0] if f.get('class') else '']).lower()
        if 'apply' in text or 'application' in text:
            s += 2
        if f.find('input', {'type': 'file'}):
            s += 3
        if s > score:
            score = s
            candidate = f
    if not candidate and forms:
        candidate = forms[0]

    if not candidate:
        raise ValueError('No form found')

    action = candidate.get('action') or base_url
    method = (candidate.get('method') or 'post').lower()

    inputs: Dict[str, Any] = {}
    file_fields: list[str] = []
    for inp in candidate.find_all(['input', 'textarea', 'select']):
        name = inp.get('name')
        if not name:
            continue
        itype = inp.get('type', '').lower()
        if itype == 'file':
            file_fields.append(name)
            continue
        if inp.name == 'select':
            # pick first option value
            opt = inp.find('option')
            if opt and opt.has_attr('value'):
                inputs[name] = opt['value']
            elif opt:
                inputs[name] = opt.text.strip()
            continue
        value = inp.get('value', '')
        inputs[name] = value

    abs_action = urljoin(base_url, action)
    return abs_action, method, inputs, file_fields


def submit_with_documents(url: str, user_payload: Dict[str, Any], files: Dict[str, Tuple[str, bytes, str]] | None = None) -> Dict[str, Any]:
    with httpx.Client(timeout=30, follow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'}) as client:
        r = client.get(url)
        r.raise_for_status()
        action, method, inputs, file_fields = discover_form(r.text, url)
        # merge user payload
        data = {**inputs, **user_payload}
        # heuristic mapping
        for key, val in list(user_payload.items()):
            # map to common names if not present
            if key == 'email' and 'email' not in data:
                data['email'] = val
            if key == 'name' and not any(k in data for k in ['name', 'full_name', 'applicant.name']):
                data['name'] = val
        # send
        if method == 'post':
            resp = client.post(action, data=data, files=files or None)
        else:
            resp = client.get(action, params=data)
        ok = 200 <= resp.status_code < 400
        return {
            'ok': ok,
            'action': action,
            'status_code': resp.status_code,
            'url': str(resp.url),
            'file_fields': file_fields,
            'used_files': list((files or {}).keys()),
        }

