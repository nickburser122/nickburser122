import {readdirSync,readFileSync,statSync,existsSync} from 'node:fs'
import {join,extname} from 'node:path'

const root=process.argv[2]
if(!root){console.error('usage: node scripts/audit.mjs <repo-dir>');process.exit(2)}

const SKIP=new Set(['node_modules','.git','test','tests','__tests__','dist','build','docs','examples','fixtures','vendor'])
const EXT=new Set(['.webmanifest','.html','.htm','.js','.mjs','.cjs','.ts','.tsx','.jsx','.css','.kt','.java','.json'])

const files=[]
const walk=dir=>{
  for(const name of readdirSync(dir)){
    if(SKIP.has(name))continue
    const p=join(dir,name),st=statSync(p)
    if(st.isDirectory())walk(p)
    else if(EXT.has(extname(name))||name==='AndroidManifest.xml')files.push(p)
  }
}
walk(root)

const read=p=>{try{return readFileSync(p,'utf8')}catch{return ''}}
const hosts=new Map()
const add=(kind,host,file)=>{
  const key=kind+'|'+host
  if(!hosts.has(key))hosts.set(key,{kind,host,files:new Set()})
  hosts.get(key).files.add(file.slice(root.length+1))
}

const libName=url=>{
  const u=new URL(url)
  const h=u.hostname
  if(h==='fonts.googleapis.com'||h==='fonts.gstatic.com')return 'Google Fonts'
  if(h==='cdn.sheetjs.com')return 'SheetJS'
  const parts=u.pathname.split('/').filter(Boolean)
  if(h==='cdnjs.cloudflare.com'&&parts[0]==='ajax'&&parts[1]==='libs')return parts[2]==='xlsx'?'SheetJS':parts[2]
  if(h==='cdn.jsdelivr.net'&&parts[0]==='npm')return parts[1].replace(/@[^@]*$/,'')
  if(h==='unpkg.com')return parts[0].replace(/@[^@]*$/,'')
  if(h==='www.gstatic.com'&&parts[0]==='firebasejs')return 'the Firebase SDK'
  if(h==='accounts.google.com')return 'Google sign-in'
  if(h==='sheets.googleapis.com')return 'Google Sheets'
  if(h==='api.github.com')return 'GitHub API'
  if(h.endsWith('firebaseio.com')||h==='firestore.googleapis.com')return 'Firebase'
  return h
}

const RES=[
  ['cdn',/<script[^>]*\ssrc=["'](https?:\/\/[^"']+)/gi],
  ['cdn',/<link[^>]*\shref=["'](https?:\/\/[^"']+)/gi],
  ['cdn',/@import\s+(?:url\()?["']?(https?:\/\/[^"')\s]+)/gi],
  ['call',/fetch\(\s*["'`](https?:\/\/[^"'`]+)/g],
  ['call',/new\s+(?:WebSocket|EventSource)\(\s*["'`](wss?:\/\/[^"'`]+)/g]
]
const API_HINTS=[
  ['call',/firebaseio\.com|firestore\.googleapis\.com|identitytoolkit\.googleapis\.com/g,'Firebase'],
  ['call',/sheets\.googleapis\.com|script\.google\.com/g,'Google Sheets'],
  ['call',/api\.github\.com/g,'GitHub API']
]

let sw=false,manifestFile=false,androidManifest=null,beacon=false,xhr=false
for(const f of files){
  const t=read(f)
  if(/serviceWorker\s*\.\s*register/.test(t))sw=true
  if(/sendBeacon/.test(t))beacon=true
  if(/XMLHttpRequest/.test(t))xhr=true
  if(/\.(webmanifest)$/.test(f)||/(^|\/)manifest\.json$/.test(f))manifestFile=true
  if(f.endsWith('AndroidManifest.xml'))androidManifest=t
  for(const [kind,re] of RES){
    for(const m of t.matchAll(re)){
      try{add(kind,libName(m[1]),f)}catch{}
    }
  }
  for(const [kind,re,name] of API_HINTS){
    if(re.test(t))add(kind,name,f)
    re.lastIndex=0
  }
}

const list=k=>[...hosts.values()].filter(h=>h.kind===k)
const names=k=>[...new Set(list(k).map(h=>h.host))]
const join_=a=>a.length<=1?a.join(''):a.slice(0,-1).join(', ')+' and '+a[a.length-1]

let network,install,needsHuman=[]
if(androidManifest!==null){
  const internet=/uses-permission[^>]*android\.permission\.INTERNET/.test(androidManifest)
  network=internet?'Android (Kotlin); declares the INTERNET permission.':'Android (Kotlin); no INTERNET permission declared.'
  install=''
  if(internet)needsHuman.push('INTERNET permission is declared: state what it is used for')
}else{
  const cdnAll=names('cdn')
  const calls=[...new Set([...names('call'),...(cdnAll.includes('the Firebase SDK')?['Firebase']:[])])]
  const cdn=cdnAll
  if(calls.length){
    network='Calls '+join_(calls)+' for <purpose>.'+(cdn.length?' Loads '+join_(cdn)+' from CDNs.':'')
    needsHuman.push('network purpose must be written by hand')
  }else if(cdn.length){
    network='No network calls after load; loads '+join_(cdn)+' from a CDN.'
  }else{
    network='No network calls. Files stay in the tab.'
  }
  if(beacon||xhr)needsHuman.push('XMLHttpRequest or sendBeacon found: read the call sites')
  install=sw&&manifestFile?'Installable (PWA); works offline after the first load.':'Not installable; no service worker.'
  if(sw!==manifestFile)needsHuman.push('service worker and manifest do not both exist: installable claim is not justified')
}

const pkg=existsSync(join(root,'package.json'))?JSON.parse(read(join(root,'package.json'))||'{}'):{}
const out={
  network,
  install,
  scripts:Object.keys(pkg.scripts||{}),
  evidence:[...hosts.values()].map(h=>({kind:h.kind,host:h.host,files:[...h.files].slice(0,4)})),
  serviceWorker:sw,
  manifest:manifestFile,
  needsHuman
}
console.log(JSON.stringify(out,null,2))
