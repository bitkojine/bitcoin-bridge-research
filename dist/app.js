const { model, rules, assessment } = window.KNOWLEDGE;
const types = {
  bitcoin_capabilities: 'Bitcoin capability', finance_requirements: 'Finance requirement',
  legal_requirements: 'Legal requirement', bridges: 'Bridge', companies: 'Company', claims: 'Claim'
};
const state = { type: 'all', query: '', selected: null };
const allItems = Object.entries(types).flatMap(([key, label]) => model[key].map(x => ({...x, _key:key, _type:label})));
const byId = Object.fromEntries(allItems.map(x => [x.id, x]));
const sourceById = Object.fromEntries(model.sources.map(x => [x.id, x]));

document.querySelector('#version').textContent = `v${model.meta.version}`;
document.querySelector('#verified').textContent = model.meta.generated_on;
document.querySelector('#assessment-scope').textContent = assessment.scope;
document.querySelector('#metrics').innerHTML = [
  ['Capabilities', model.bitcoin_capabilities.length], ['Requirements', model.finance_requirements.length + model.legal_requirements.length],
  ['Bridges', model.bridges.length], ['Companies', model.companies.length], ['Claims', model.claims.length], ['Sources', model.sources.length]
].map(([label,value]) => `<div class="metric"><b>${value}</b><span>${label}</span></div>`).join('');

const filterDefs = [['all','All'], ...Object.entries(types).map(([key,label]) => [key,label.replace(' requirement','')])];
document.querySelector('#filters').innerHTML = filterDefs.map(([key,label],i) => `<button class="filter ${i===0?'active':''}" data-filter="${key}">${label}</button>`).join('');
document.querySelectorAll('.filter').forEach(btn => btn.addEventListener('click', () => {
  document.querySelectorAll('.filter').forEach(x => x.classList.remove('active')); btn.classList.add('active'); state.type=btn.dataset.filter; renderCatalog();
}));

function summary(item){
  if(item.establishes) return item.establishes;
  if(item.text) return item.text;
  if(item._key==='company') return item.bridges?.join(', ');
  return item.name || '';
}
function searchable(item){ return JSON.stringify(item).toLowerCase(); }
function renderCatalog(){
  const items=allItems.filter(x => (state.type==='all'||x._key===state.type) && searchable(x).includes(state.query));
  const root=document.querySelector('#catalog');
  root.innerHTML=items.length?items.map(x=>`<button class="catalog-item ${state.selected===x.id?'active':''}" data-id="${x.id}"><span class="item-type">${x._type}</span><strong>${x.name||x.text}</strong><p>${summary(x)}</p></button>`).join(''):'<div class="empty-state"><strong>No match.</strong><span>Try a broader term or another category.</span></div>';
  root.querySelectorAll('[data-id]').forEach(b=>b.addEventListener('click',()=>{state.selected=b.dataset.id;renderCatalog();renderDetail(byId[state.selected]);}));
}
function refs(ids=[]){ return ids.map(id=>`<span class="chip">${byId[id]?.name||id}</span>`).join(''); }
function renderDetail(item){
  const d=document.querySelector('#detail'); if(!item){d.innerHTML='<p class="detail-kicker">Select an entry</p><h2>Inspect the knowledge</h2><p>Choose any concept, company, bridge, or claim to see what the repository actually records and how it connects.</p>';return;}
  let body=`<p class="detail-kicker">${item._type} · ${item.id}</p><h2>${item.name||'Research claim'}</h2>`;
  if(item.formula) body+=`<div class="formula">${item.formula}</div><h3>Every term explained</h3>${Object.entries(item.terms).map(([k,v])=>`<p><strong>${k}</strong> — ${v}</p>`).join('')}`;
  if(item.establishes) body+=`<h3>What it establishes</h3><p>${item.establishes}</p>`;
  if(item.does_not_establish) body+=`<h3>What it does not establish</h3>${item.does_not_establish.map(x=>`<span class="chip">${x}</span>`).join('')}`;
  if(item.bitcoin_capabilities) body+=`<h3>Bitcoin capabilities</h3>${refs(item.bitcoin_capabilities)}<h3>Finance requirements</h3>${refs(item.finance_requirements)}<h3>Legal requirements</h3>${refs(item.legal_requirements)}`;
  if(item.bridges){body+=`<h3>Bridge territory</h3>${refs(item.bridges)}`;}
  if(item.text){body+=`<p>${item.text}</p><h3>Status</h3><span class="chip">${item.status}</span><h3>Evidence</h3>${item.source_ids.map(id=>sourceLink(sourceById[id])).join('')}`;}
  if(item._key==='bridges'){const cos=model.companies.filter(c=>c.bridges.includes(item.id));body+=`<h3>Companies occupying this territory</h3>${cos.map(c=>`<span class="chip company-chip">${c.name}</span>`).join('')||'<p>None recorded.</p>'}`;}
  d.innerHTML=body;
}
function sourceLink(s){return `<a class="source-link" href="${s.url}" target="_blank" rel="noreferrer">↗ ${s.title} <small>Level ${s.level}</small></a>`;}
const search=document.querySelector('#search');search.addEventListener('input',e=>{state.query=e.target.value.trim().toLowerCase();renderCatalog();});
document.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key==='k'){e.preventDefault();search.focus();}});

document.querySelectorAll('.nav-item').forEach(btn=>btn.addEventListener('click',()=>{
  document.querySelectorAll('.nav-item,.view').forEach(x=>x.classList.remove('active'));btn.classList.add('active');document.querySelector(`#${btn.dataset.view}`).classList.add('active');
  document.querySelector('#page-title').textContent={explore:'Explore what the system knows',assessment:'Run an evidence-gap assessment',sources:'Inspect the evidence register',system:'Audit the system itself'}[btn.dataset.view];window.scrollTo({top:0,behavior:'smooth'});
}));

const form=document.querySelector('#assessment-form');
form.innerHTML=assessment.requirements.map((r,i)=>`<div class="question" data-fact="${r.fact}" ${r.applies_when?`data-condition="${r.applies_when.fact}"`:''}><div class="question-top"><label>${String(i+1).padStart(2,'0')} · ${r.label}</label></div><p>${r.evidence_expected}</p><div class="choice"><input type="radio" id="${r.fact}-u" name="${r.fact}" value="unknown" checked><label for="${r.fact}-u">No record</label><input type="radio" id="${r.fact}-y" name="${r.fact}" value="true"><label for="${r.fact}-y">Claimed pass</label><input type="radio" id="${r.fact}-n" name="${r.fact}" value="false"><label for="${r.fact}-n">Claimed gap</label></div></div>`).join('')+`<div class="question"><label>Sub-custodian or custody technology provider used?</label><p>This controls whether third-party diligence is applicable.</p><div class="choice"><input type="radio" id="sub-u" name="subcustodian_used" value="unknown" checked><label for="sub-u">Unknown</label><input type="radio" id="sub-y" name="subcustodian_used" value="true"><label for="sub-y">Yes</label><input type="radio" id="sub-n" name="subcustodian_used" value="false"><label for="sub-n">No</label></div></div>`;
form.addEventListener('change',renderAssessment);
function renderAssessment(){
  const data=new FormData(form), sat=[],failed=[],unknown=[]; const sub=data.get('subcustodian_used');
  assessment.requirements.forEach(r=>{if(r.applies_when&&sub==='false')return;let v=data.get(r.fact);if(r.applies_when&&sub==='unknown')v='unknown';(v==='true'?sat:v==='false'?failed:unknown).push(r);});
  const outcome=failed.length?'NOT READY':unknown.length?'INSUFFICIENT INFORMATION':'READY FOR EXPERT REVIEW';
  const cls=failed.length?'not-ready':unknown.length?'':'ready';
  const group=(title,items,details)=>items.length?`<div class="result-group"><h3>${title} · ${items.length}</h3>${items.map(x=>`<div class="result-item">${x.label}${details?`<em>${x.evidence_expected}</em>`:''}</div>`).join('')}</div>`:'';
  document.querySelector('#assessment-result').innerHTML=`<div class="outcome ${cls}"><span>UNVERIFIED SANDBOX RESULT</span><b>${outcome}</b></div><p class="detail-copy">${sat.length} claimed passes · ${failed.length} claimed gaps · ${unknown.length} unknown</p>${group('Claimed gaps',failed,true)}${group('Missing records',unknown,true)}${group('Claimed passes',sat,false)}<div class="result-group"><h3>Limit</h3><div class="result-item">These selections have no artifact, issuer, provenance, scope, or review record. This is not output from the evidence-backed engine.</div></div>`;
}

const levels={1:'Company marketing',2:'Official technical documentation',3:'Regulatory or legal filing',4:'Independent professional evidence',5:'Reproducible primary data'};
document.querySelector('#source-legend').innerHTML=Object.entries(levels).map(([n,l])=>`<span class="legend-item"><b>${n}</b> ${l}</span>`).join('');
document.querySelector('#source-grid').innerHTML=model.sources.sort((a,b)=>b.level-a.level).map(s=>`<article class="source-card"><span class="level">EVIDENCE LEVEL ${s.level} · CHECKED ${s.checked_on}</span><h3>${s.title}</h3><a href="${s.url}" target="_blank" rel="noreferrer">Open primary source ↗</a></article>`).join('');
const can=['Represent the current domain as structured data','Search concepts, companies, claims and relationships','Trace claims and assessment requirements to sources','Run a deterministic custody-readiness pre-screen','Distinguish explicit gaps from missing information'];
const cannot=['Authenticate the facts entered by a user','Determine legal ownership from key control','Give legal, compliance, tax or investment advice','Prove that every wallet, key copy or liability was disclosed','Track regulatory changes or news automatically','Claim expert-level coverage or professional validation'];
document.querySelector('#can-list').innerHTML=can.map(x=>`<li>${x}</li>`).join('');document.querySelector('#cannot-list').innerHTML=cannot.map(x=>`<li>${x}</li>`).join('');
document.querySelector('#rule-list').innerHTML=rules.rules.map(r=>`<article><span class="rule-id">${r.id}</span><span class="rule-desc">${r.description}</span><span class="priority">Priority ${r.priority}</span></article>`).join('');
renderCatalog();renderDetail(null);renderAssessment();
