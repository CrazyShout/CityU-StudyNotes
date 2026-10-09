const fs=require('fs'),path=require('path'),crypto=require('crypto');
const sha256=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..');
const index=JSON.parse(fs.readFileSync(path.join(root,'QuestionIndex.json')));
const buildDate=new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Shanghai'});
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
 const reports=[];
 const pageMaps=fs.existsSync(path.join(root,'PageIndex.json'))?JSON.parse(fs.readFileSync(path.join(root,'PageIndex.json'))):{};
 try{for(const kind of ['Questions','Answers']){
  const page=await browser.newPage({viewport:{width:650,height:980}});
  await page.emulateMedia({media:'print'});await page.route(/^https?:/,r=>r.abort());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('file://'+path.join(root,'.build',kind+'.html'),{waitUntil:'load'});
  await page.waitForFunction(()=>window.printReady);await page.evaluate(()=>document.fonts.ready);
  const qa=await page.evaluate(()=>({
   mathErrors:[...document.querySelectorAll('.katex-error')].map(e=>e.textContent),
   brokenImages:[...document.images].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src),
   overflow:[...document.querySelectorAll('.katex-display,table')].filter(e=>e.scrollWidth>e.clientWidth+3).map(e=>({text:e.textContent.slice(0,120),width:e.clientWidth,scroll:e.scrollWidth})),
   questions:[...document.querySelectorAll('h2[id^="mt"]')].map(e=>e.id),
   math:document.querySelectorAll('.katex').length,images:document.images.length
  }));
  if(errors.length||qa.mathErrors.length||qa.brokenImages.length||qa.overflow.length||qa.questions.length!==index.unique_questions)throw Error(JSON.stringify({kind,errors,qa}));
  await page.pdf({path:path.join(root,kind+'.pdf'),format:'A4',preferCSSPageSize:true,printBackground:true,outline:true,tagged:true,displayHeaderFooter:true,
   headerTemplate:'<div style="font-size:8px;color:#555;margin-left:20mm;font-family:Arial">CS5489 · Midterm · '+kind+' · '+buildDate+'</div>',
   footerTemplate:'<div style="width:100%;font-size:9px;color:#555;text-align:right;margin-right:18mm;font-family:Arial"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'});
  reports.push({kind,...qa,errors,source_sha256:sha256(path.join(root,kind+'.md')),index_sha256:sha256(path.join(root,'QuestionIndex.json')),html_sha256:sha256(path.join(root,'.build',kind+'.html')),rendered_pdf_sha256:sha256(path.join(root,kind+'.pdf')),page_maps_used:pageMaps});await page.close();console.log('Rendered '+kind);
 }}finally{await browser.close();}
 fs.writeFileSync(path.join(root,'.build/render-report.json'),JSON.stringify(reports,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
