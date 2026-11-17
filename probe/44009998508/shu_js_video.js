//**************************************************************************************
//    プログラム名：一般公開用メニュー／VOD検索条件入力form選択エラーチェック
//    作成日：2008/11/01
//    更新日：
//    バージョン：4.0.0
//    リリース日：
//    変更履歴
//      新規作成  :  V/R=4.0.0.00  2008/11/01
//**************************************************************************************

function kUp1(myEvents){
  if(document.FORM1.t_anken.value != ""){
    document.FORM1.c_anken.checked = true;
    return true;
  }
}
function kUp2(myEvents){
  if(document.FORM1.t_hatsugen.value != ""){
    document.FORM1.c_hatsugen.checked = true;
    return true;
  }
}

function ChangeDay(){
  if((document.FORM1.s_Year.value!="")||(document.FORM1.s_Month.value!="")||(document.FORM1.s_Day.value!="")||(document.FORM1.e_Year.value!="")||(document.FORM1.e_Month.value!="")||(document.FORM1.e_Day.value!="")){ 
    document.FORM1.c_day.checked = true;
    return false;
  }
}
function ChangeKaigi(){
  if(document.FORM1.s_kaigi.value!=""){
    document.FORM1.c_kaigi.checked = true;
    return false;
  }
}

function turnoffcheck(x){
  temp='document.FORM1.c_' + x ;
  if(x=='day'){
    if(eval(temp).checked == false){
      document.FORM1.s_Year.options[0].selected=true;
      document.FORM1.s_Month.options[0].selected=true;
      document.FORM1.s_Day.options[0].selected=true;
      document.FORM1.e_Year.options[0].selected=true;
      document.FORM1.e_Month.options[0].selected=true;
      document.FORM1.e_Day.options[0].selected=true;
    }
  }  
  if(x=='kaigi'){
    temp2='document.FORM1.s_' + x ;
    if(eval(temp).checked == false){
      eval(temp2).options[0].selected=true;
    }
  }
  if((x=='anken')||(x=='hatsugen')){  
    temp2='document.FORM1.t_' + x ;
    if(eval(temp).checked == false){
      eval(temp2).value ="";
    }
  }  
}

function Kensaku(){
  if(document.FORM1.c_day.value=="true"){
    var s_date="";
    var e_date="";
    if(   document.FORM1.s_Year.selectedIndex != 0 &&
        document.FORM1.s_Month.selectedIndex != 0 &&
        document.FORM1.s_Day.selectedIndex != 0
    ){
      s_date = dd = new Date(
         document.FORM1.s_Year.options[document.FORM1.s_Year.selectedIndex].value
        ,document.FORM1.s_Month.options[document.FORM1.s_Month.selectedIndex-1].value
        ,document.FORM1.s_Day.options[document.FORM1.s_Day.selectedIndex].value);
    }

    if(document.FORM1.e_Year.selectedIndex != 0 &&
      document.FORM1.e_Month.selectedIndex != 0 &&
      document.FORM1.e_Day.selectedIndex != 0
    ){
      e_date = dd = new Date(
         document.FORM1.e_Year.options[document.FORM1.e_Year.selectedIndex].value
        ,document.FORM1.e_Month.options[document.FORM1.e_Month.selectedIndex-1].value
        ,document.FORM1.e_Day.options[document.FORM1.e_Day.selectedIndex].value);
    }
    
    if( s_date == "" && e_date == ""){
      alert("検索対象の年月日を正しく入力して下さい");
      document.FORM1.s_Year.focus();
      return(false);
    }else
    if( s_date == "" &&
      (document.FORM1.s_Year.selectedIndex != 0 ||
         document.FORM1.s_Month.selectedIndex != 0 ||
         document.FORM1.s_Day.selectedIndex != 0)){

      alert("日付の指定が間違っています。");
      document.FORM1.s_Year.focus();
      return(false);
    }else
    if( e_date == "" &&
      (document.FORM1.e_Year.selectedIndex != 0 ||
         document.FORM1.e_Month.selectedIndex != 0 ||
         document.FORM1.e_Day.selectedIndex != 0)
    ){
      alert("日付の指定が間違っています。");
      document.FORM1.e_Year.focus();
      return(false);
    }else
    if( e_date != "" && (s_date > e_date) ){
        alert("日付の指定が間違っています。");
        document.FORM1.s_Year.focus();
        return(false);
    }
  }


  if((document.FORM1.c_kaigi.checked==true)&&(document.FORM1.s_kaigi.options[0].selected==true)){
    alert("検索条件を入力して下さい");
    document.FORM1.s_kaigi.focus();
    return(false);
  }
  if((document.FORM1.c_anken.checked==true)&&(document.FORM1.t_anken.value=="")){
    alert("検索条件を入力して下さい");
    document.FORM1.t_anken.focus();
    return(false);
  }
  if((document.FORM1.c_hatsugen.checked==true)&&(document.FORM1.t_hatsugen.value=="")){
    alert("検索条件を入力して下さい");
    document.FORM1.t_hatsugen.focus();
    return(false);
  }
  if((document.FORM1.c_day.value=="false")&&(document.FORM1.c_kaigi.value=="false")&&(document.FORM1.c_anken.value=="false")&&(document.FORM1.c_hatsugen.value=="false")){
    alert("検索対象をチェックし、検索条件を入力して下さい");
    document.FORM1.s_Year.focus();
    return(false);
  }
  if(document.FORM1.t_anken.value.length > 200){
    alert("「案件名」入力欄は、" + "200文字以内で入力して下さい。");
    document.FORM1.t_anken.focus();
    return(false);
  } else if(document.FORM1.t_hatsugen.value.length > 50){
    alert("「発言者名」入力欄は、" + "50文字以内で入力して下さい。");
    document.FORM1.t_hatsugen.focus();
    return(false);
  } else {

////  document.FORM1.action = 'video_lib2.php';
  document.FORM1.submit();
  return(true);
  }
}

