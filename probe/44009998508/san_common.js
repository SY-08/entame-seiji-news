function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_swapImgRestore() { //v3.0
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}

function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}


function MM_openBrWindow(theURL,winName,features) { //v2.0
  newwin = window.open(theURL,winName,features);
  newwin.focus();
  return newwin;
}

function MM_goToURL() { //v3.0
  var i, args=MM_goToURL.arguments; document.MM_returnValue = false;
  for (i=0; i<(args.length-1); i+=2) eval(args[i]+".location='"+args[i+1]+"'");
}



function kaigi_clear(str) {
	document.form.sel_kaigi_code.value = 0;
	document.form.tx_kaigi_name.value = str;
	document.form.kaigi_name_bk.value = str;
}

function kaigi_reset() {
	if (document.form.tx_kaigi_name == null){
		return;
	}
	document.form.tx_kaigi_name.value=document.form.kaigi_name_bk.value;
}


function date_future_check(sel_year,sel_month,sel_day,now_date,selY,selM,selD){
	day_check(sel_year,sel_month,sel_day);
    input_date = datejoin(sel_year,sel_month,sel_day);
    
	if (input_date > now_date){
		alert("開会日は今日以前の日付を指定してください。\n今日の日付に変更します。");
		sel_year.selectedIndex = selY;
		sel_month.selectedIndex = selM;
		sel_day.selectedIndex = selD;
		day_check(sel_year,sel_month,sel_day);
		return false;
	}
	return true;
}

function day_check(sel_year,sel_month,sel_day){

	year = sel_year.options[sel_year.selectedIndex].value;
	mon = sel_month.options[sel_month.selectedIndex].value;
	day = sel_day.options[sel_day.selectedIndex].value;
	
	day_max = 31;
	if ((mon == "4") || (mon == "6") || (mon == "9") || (mon == "11")){
		day_max = 30;
	}
	if(mon == "2"){
		if (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0)){
			day_max = 29;
		}else{
			day_max = 28;
		}
	}

	sel_day.length = day_max;
	for(i=0; i < day_max ; i++){
		sel_day.options[i].text = i+1;
		sel_day.options[i].value = i+1;
	}

	if( day_max < day){
		sel_day.selectedIndex=day_max-1;
	}else{
		sel_day.value=day;
	}		
} 

function date_sequence_check(){
	from_date = datejoin(document.form.sel_s_year,document.form.sel_s_month,document.form.sel_s_day);
	to_date = datejoin(document.form.sel_e_year,document.form.sel_e_month,document.form.sel_e_day);

	if (from_date > to_date){
		alert("開始日には終了日以前の日付を指定してください。");
		return false;
	}
	return true;
}
function datejoin(sel_year,sel_month,sel_day){
	year = sel_year.options[sel_year.selectedIndex].value;
	mon = sel_month.options[sel_month.selectedIndex].value;
	day = sel_day.options[sel_day.selectedIndex].value;
    return year + zerofill(mon,2) + zerofill(day,2);
}
function zerofill(num,size){
	effect = "0000" + num.toString();
	len = effect.length;
	return effect.substring(len-size,len);
}
function string_max_check(target){
	txt = target.value;
	bfind = 1;
	scount = 0;
	for (i=0; i<txt.length; i++){
		bfindback = bfind;
		bfind=(txt.charAt(i) == " " || txt.charAt(i) == "　")?1:0;
		if (bfind != bfindback && bfind == 0){
			scount++;
		}
	}
	return scount;
}

function wop(theURL,winName,features) {
newW=window.open(theURL,winName,features);
}


function link_personality(){
	for (i=0;i<window.document.links.length;i++){
		l = window.document.links[i];
		if (l.href.match("meta_generator") != null){
			if (l.href.match("&pars") != null){
				rep = new RegExp("&pars=(\d|\.)+");
				l.href = l.href.replace(rep,"");
			}
			l.href += "&pars=" + Math.random();
		}
	}
}
