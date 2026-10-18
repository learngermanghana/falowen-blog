(function(){
  'use strict';
  var base='https://docs.google.com/spreadsheets/d/e/2PACX-1vRSRGvV3i6dtdnl-n3QBj0j0frbCooUlEGRG_l_6XsJlc_OU-DlivYaw2XESuhHNkIxkOiy-ivBdiYc/pub?output=csv';
  var all=[],level='All',limit=36;
  var grid=document.getElementById('fl-vocab-grid'),status=document.getElementById('fl-vocab-status'),query=document.getElementById('fl-vocab-search'),more=document.getElementById('fl-load-more'),fallback=document.getElementById('fl-vocab-fallback');
  if(!grid||!status)return;
  function csvRows(source){var result=[],row=[],cell='',quoted=false;for(var i=0;i<source.length;i++){var c=source[i];if(c==='"'){if(quoted&&source[i+1]==='"'){cell+='"';i++;}else quoted=!quoted;}else if(c===','&&!quoted){row.push(cell);cell='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&source[i+1]==='\n')i++;row.push(cell);if(row.some(function(x){return x.trim();}))result.push(row);row=[];cell='';}else cell+=c;}if(cell||row.length){row.push(cell);result.push(row);}return result;}
  function elem(tag,klass,value){var el=document.createElement(tag);if(klass)el.className=klass;if(value!==undefined)el.textContent=value;return el;}
  function render(){
    var term=query.value.trim().toLocaleLowerCase('de'), filtered=all.filter(function(w){
      return (level==='All'||w.level.toUpperCase()===level)&&(w.de+' '+w.en).toLocaleLowerCase('de').includes(term);
    });
    grid.replaceChildren();
    var displayed=filtered.slice(0,limit),prevLevel='',prevLetter='';
    displayed.forEach(function(w){
      var letter=(w.de.replace(/^(der|die|das)\s+/i,'').charAt(0)||'#').toLocaleUpperCase('de');
      if(level==='All'&&w.level!==prevLevel){
        var group=elem('h2','fl-word-group',w.level||'Other vocabulary');
        grid.append(group);prevLevel=w.level;prevLetter='';
      }
      if(letter!==prevLetter){
        grid.append(elem('h3','fl-word-letter',letter));
        prevLetter=letter;
      }
      var card=elem('div','fl-word-card'),word=elem('strong','fl-word-german',w.de),meaning=elem('span','fl-word-english',w.en);
      card.append(word,meaning);grid.append(card);
    });
    status.textContent=filtered.length+' words'+(filtered.length>limit?' · showing '+displayed.length:'');
    more.hidden=filtered.length<=limit;
  }
  document.querySelectorAll('[data-level]').forEach(function(button){button.addEventListener('click',function(){level=button.dataset.level;limit=36;document.querySelectorAll('[data-level]').forEach(function(b){b.setAttribute('aria-pressed',String(b===button));});render();});});query.addEventListener('input',function(){limit=36;render();});more.addEventListener('click',function(){limit+=36;render();});
  fetch(base,{mode:'cors'}).then(function(r){if(!r.ok)throw Error('CSV fetch failed');return r.text();}).then(function(csv){var rows=csvRows(csv);var header=rows.findIndex(function(row){return row.some(function(x){return /^german$/i.test(x.trim());})&&row.some(function(x){return /^english$/i.test(x.trim());});});if(header<0)throw Error('Unknown vocabulary columns');var headings=rows[header].map(function(x){return x.trim().toLowerCase();});var de=headings.indexOf('german'),en=headings.indexOf('english'),lv=headings.indexOf('level');all=rows.slice(header+1).map(function(row){return{de:(row[de]||'').trim(),en:(row[en]||'').trim(),level:(row[lv]||'').trim()};}).filter(function(w){return w.de&&w.en;});if(!all.length)throw Error('No vocabulary rows');var rank={A1:1,A2:2,B1:3,B2:4,C1:5,C2:6};all.sort(function(a,b){return ((rank[a.level.toUpperCase()]||99)-(rank[b.level.toUpperCase()]||99))||a.de.replace(/^(der|die|das)\s+/i,'').localeCompare(b.de.replace(/^(der|die|das)\s+/i,''),'de',{sensitivity:'base'});});render();}).catch(function(){status.textContent='The live vocabulary cards could not be loaded. Use the published vocabulary table below.';fallback.hidden=false;});
})();