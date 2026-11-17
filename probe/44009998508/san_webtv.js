var CSS_TOP;
var keepOn;
var def_s_year,def_s_month,def_s_day,def_e_year,def_e_month,def_e_day,def_kaigi_name,def_kaigi_code;
var cur_page;
var keep_meetingname_height;

//指定の場所をブロックし、お待ちくださいメッセージを表示
function waiting_for(tgt){
	$(tgt).block({ 
		message: '<span style="font-size:14pt">しばらくお待ちください。</span>', 
		css: {backgroundColor:'#fff', width: '50%', border: '2px solid #a00' } ,
		overlayCSS:  {backgroundColor: '#000', opacity: 0.2}
	}); 
}

//指定の場所をブロックし、お待ちくださいメッセージを表示
function waiting_for2(tgt,pointY){
	if (typeof pointY === "undefined") pointY=120;
	CSS_TOP = (pointY - 30) + 'px';
	$(tgt).block({ 
		message: '<span style="font-size:14pt">しばらく<br>お待ちください。</span>', 
		centerY: false,
		css: { top:CSS_TOP , backgroundColor:'#fff', width: '50%', border: '2px solid #a00' } ,
		overlayCSS:  {backgroundColor: '#000', opacity: 0.2}
	}); 
}
//会議リスト高さ動的変更
function meetingname_height2(h_val){
	if (typeof h_val === "undefined") {
		offset_mn = $('#meetingname').offset();
		offset_ft = $('#footer').offset();
		h_val = offset_ft.top - offset_mn.top;
	}
	$("#meetingname").height(h_val);

	keep_meetingname_height = $("#meetingname").height();
}

//会議リスト高さ動的変更
function meetingname_height(){
	var h = 0;
	var sh = 0;
	if($('#result_area').is(':visible')){
		h = $('#result_area').height();
		sh = $('#result_area').attr('scrollHeight');
	}else if($('#faq_area').is(':visible')){
		h = $('#faq_area').height();
		sh = $('#faq_area').attr('scrollHeight');
	}else if($('#howto_area').is(':visible')){
		h = $('#howto_area').height();
		sh = $('#howto_area').attr('scrollHeight');
	}
	var mh = $('#meetingname').height();
	var msh = $('#meetingname').attr('scrollHeight');
	var dif = sh - 190;
	var nh = 0;
	if($('#news').is(':visible')){
		nh = $('#news').height() - 15;
	}
	if((dif)>0){
		$("#meetingname").height(345 + dif + nh);
	}else{
		$("#meetingname").height(345 + nh);
	}

	keep_meetingname_height = $("#meetingname").height();
}

function init_result(){
	meetingname_height();
	//検索結果部分初期表示
	$.ajax({
	  url: "./result_selecter.php",
	  cache: false,
	  type: "get",
	  success: function(data){
			$("#result_area").html(data);
			meetingname_height2();
		}
	});
}



function setupRadioChangeHandlers() {
    var speakerRows = document.querySelectorAll('tr.speaker');  // `speaker` クラスを持つすべての tr 要素を取得

    var radioAll = document.getElementById('m_k');
    var radioSpeechOnly = document.getElementById('m_h');

    function handleRadioChange() {
        speakerRows.forEach(row => {  // すべての対象行に対してループ処理
            row.style.display = radioSpeechOnly.checked ? 'none' : '';  // 条件に応じて表示を切り替え
        });
    }

    radioAll.addEventListener('change', handleRadioChange);
    radioSpeechOnly.addEventListener('change', handleRadioChange);

    handleRadioChange(); // 初期状態の設定
}


function init_search(){	
	//検索フォーム部分初期表示
	$.ajax({
	  url: "./form.php",
	  cache: false,
	  type: "get",
	  success: function(data){
			$("#search_area").html(data);
			def_kaigi_name=$("#tx_kaigi_name").val();
			def_kaigi_code=$("#sel_kaigi_code").val();
			def_s_year=$("#sel_s_year").val();
			def_s_month=$("#sel_s_month").val();
			def_s_day=$("#sel_s_day").val();
			def_e_year=$("#sel_e_year").val();
			def_e_month=$("#sel_e_month").val();
			def_e_day=$("#sel_e_day").val();
			setupRadioChangeHandlers();
		}
	});
}
function init_news(){
	meetingname_height();
	//お知らせ部分初期表示
	$.ajax({
	  url: "./news.php",
	  cache: false,
	  type: "get",
	  success: function(data){
			$("#news").html(data);
			meetingname_height2();
		}
	});
}

//よくある質問ページ内リンククリック時のスクロール処理
function faqLink_click(){
	$(".faqLink").click(function() {
		var lnk=$(this).attr('href').split("#");
		var t = "#" + lnk[1];
		$.scrollTo(t, 800);
		return false;
	});
}

function init_kaigilist(){
	//会議リスト部分初期表示
	$.ajax({
	  url: "./kaigi_list.php",
	  cache: false,
	  success: function(data){
			$("#meetingname").html(data);
			$("p.kaigi > a").mouseover(function(){
				$(this).addClass("hover");
			}).mouseout(function(){
				$(this).removeClass("hover");
			});
			//検索結果部分取得
			init_result();
		}
	});
}
function init_calendar(){
	//カレンダー初期表示
	$.ajax({
	  url: "./calendar.php",
	  cache: false,
	  success: function(html){
			$("#calendar").html(html);
		}
	});
}

//カレンダー次月、来月表示
function calendar_move(month) {
waiting_for('#container');//ブロック
	$.get("./calendar.php", { calendarmove: 1, dt_calendarpoint: month ,pars: Math.random()},
	  function(data){
	    $("#calendar").html(data);
			$('#container').unblock();//ブロック解除
	  });
}

function calendar_click(date){
	ymd=date.split("-");
	$("#tx_kaigi_name").val(def_kaigi_name);
	$("#sel_kaigi_code").val(def_kaigi_code);
	$("#sel_s_year").val(ymd[0]);
	$("#sel_s_month").val(parseInt(ymd[1], 10));
	$("#sel_s_day").html("");
	$("#sel_e_day").html("");
	year=ymd[0];
	mon=parseInt(ymd[1], 10);
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
	for(i=0;i<day_max;i++){
		dval=i+1;
		$("#sel_s_day").append('<option value="' + dval + '">' + dval + '</option>');
		$("#sel_e_day").append('<option value="' + dval + '">' + dval + '</option>');
	}
	$("#sel_s_day").val(parseInt(ymd[2], 10));
	$("#sel_e_year").val(ymd[0]);
	$("#sel_e_month").val(parseInt(ymd[1], 10));
	$("#sel_e_day").val(parseInt(ymd[2], 10));
	$("#tx_word").val("");
	$("#tx_speaker").val("");
	$("#tx_anken").val("");
	if(!$('#search_area').is(':visible')){
		$("#search_area").slideDown("fast");
		$("#txt-search_area").slideUp("fast",function(){search_click();});
	}else{
		search_click();
	}
}

function detail_click(no){
	$('.fancybox').fancybox({
		'scrolling': 'no',
		'padding':"10",
		'width'				: '680',
		'height'			: '98%',
		'iframe' : {
			scrolling : 'auto',
			preload   : false
		},
		'autoCenter' : true,
		'type'				: 'iframe',
		'beforeLoad':function(){
			//詳細画面開いたらタブレットでのスクロール禁止
			$(window).on('touchmove.noScroll', function(e) {
				e.preventDefault();
			});
			//タイマーセット済みであれば
			if(typeof(Reflesh) == "number") {
				//今日の審議中継　メイン部分自動更新解除
				clearInterval( Reflesh ) ; 
			}
		},
		'afterClose':function(){
			//スクロール禁止取りやめ
			$(window).off('.noScroll');
			if($("#live_list").length>0){
				//今日の審議中継リロード再開
				reloadTodayList();
			}
			
		}
	});
}

function openModal(src){
	$('.modal-content iframe').attr('src', src);
	$('.modal-overlay').fadeIn();
	$('.modal-content').fadeIn();
}
function closeModal() {
	$('.modal-content').fadeOut();
	$('.modal-overlay').fadeOut(function() {
		$('.modal-content iframe').attr('src', '');
	});
}
function modal_action(){

	// モーダルリンクのクリックイベント
	$(document).on("click", ".modal-open",function(e){
		e.preventDefault();

		var src = $(this).attr('href');
		openModal(src);
	});

	// // モーダルウィンドウを閉じる処理
	// $(document).on("click", ".modal-overlay",function(e){
	// 	closeModal();
	// });

	// 子ウィンドウの閉じるボタンクリック時の処理
	// iframeの読み込み完了イベント
	$('.modal-content iframe').on('load', function() {
		var iframe = $(this)[0];
		var iframeWindow = iframe.contentWindow;

		// 子ウィンドウの閉じるボタンにイベントを設定
		$(iframeWindow.document).on('click', '.modal-close', function(e) {
			e.preventDefault();
			closeModal();
		});
	});

}

function detail2_click(){
	$(document).on("click", ".detail",function(event){
		event.preventDefault();
		$('#news').hide();
		$('#search_area').hide();
		$('#txt-search_area').hide();
		$('#result_area').hide();
		$('#detail_area').html("").hide();
		
		var tgturl = $(this).attr('href');
//		$.post(tgturl, "", function(data){
//			console.log(tgturl);
//			console.log("Server response:", data); // 全てのデータをログに出力
			//$("#detail_area").html(data).show();

			// 既存のiframeを確認し、存在する場合は削除する
			$('#detail_frame').remove();

			// iframeのsrc属性を設定して、URLのページをロードする
			$('#detail_area').show();
			//$("#detail_frame").attr('src', tgturl);

			// 新しいiframeを作成する
			var iframe = $('<iframe>', {
				id: 'detail_frame',
				src: tgturl,
				// scrolling: "no",
				//style: 'width:100%; height:880px; border:none;',
				load: function() {
					// iframeがロードされた後に実行される処理
					console.log("iframe loaded successfully.");

					// iframeのコンテンツにアクセス
					var iframeContent = this.contentWindow;
					// iframe内の子ウィンドウに再生を開始するよう指示
					iframeContent.postMessage({ action: 'initializePlayer', videoplay: 'auto' }, '*');

					//プレイヤーが見える位置までスクロール
					document.getElementById('detail_area').scrollIntoView({behavior: 'smooth', block: 'start'});

					//タイマーセット済みであれば
					if(typeof(Reflesh) == "number") {
						//今日の審議中継　メイン部分自動更新解除
						clearInterval( Reflesh ) ; 
					}

				}
			});
			$('#detail_area').append(iframe);

//		});

	});
}



function keika_click(){
	$(document).on("click", ".keika",function(event){
		event.preventDefault(); // デフォルトのアンカー動作を防ぐ
		var dataSid = $(this).data('sid'); // data-sid 属性の値を取得
		var targetDl = $('#keika-' + dataSid); // 対象の dl 要素を取得
//console.log('dataSid='+dataSid);
		// dl の表示状態を切り替える
		if (targetDl.is(':visible')) {
			//非表示前の高さ取得
			mainh_before=$("#maincontent").height();
			meetingh_before=$("#meetingname").height();

			//非表示
			targetDl.css('display','none');
			$(this).text('+');

			//非表示後の高さ取得
			mainh_after=$("#maincontent").height();
			mainh_diff=(mainh_before - mainh_after);
			new_meetingh = meetingh_before - mainh_diff;

			//会議名リスト高さ指定
			meetingname_height2(new_meetingh);			
		} else {
			//表示
			targetDl.css('display','inline-block');
			$(this).text('-');
			meetingname_height2();
		}

	});

}

//会議リスト高さ動的変更
function meetingname_height3(){

	meetingh=$("#meetingname").height();
	console.log('$("#meetingname").height()=' + meetingh);
	mainh=$("#maincontent").height();
	console.log('$("#maincontent").height()=' + mainh);


	offset_mn = $("#meetingname").offset();
	offset_ft = $("#footer").offset();
	h_val = offset_ft.top - offset_mn.top;
	console.log(h_val);


	// $("#meetingname").height(h_val);

	// keep_meetingname_height = $("#meetingname").height();
}




//初期表示時に詳細ページ表示（SNSからのアクセス用？）
function showDetail(param){
	
	$('#news').hide();
	$('#search_area').hide();
	$('#txt-search_area').hide();
	$('#result_area').hide();
	$('#detail_area').html("").hide();
	
	var tgturl = "detail.php?" + param + "&direct=1";
	$.post(tgturl, "", function(data){
//		console.log(tgturl);
//		console.log("Server response:", data); // 全てのデータをログに出力
		//$("#detail_area").html(data).show();

		// 既存のiframeを確認し、存在する場合は削除する
		$('#detail_frame').remove();

		// iframeのsrc属性を設定して、URLのページをロードする
		$('#detail_area').show();
		//$("#detail_frame").attr('src', tgturl);

		// 新しいiframeを作成する
		var iframe = $('<iframe>', {
			id: 'detail_frame',
			src: tgturl,
			//style: 'width:100%; height:400px; border:none;',
			load: function() {
				// iframeがロードされた後に実行される処理
				console.log("iframe loaded successfully.");

				// iframeのコンテンツにアクセス
				var iframeContent = this.contentWindow;
				// iframe内の子ウィンドウに再生を開始するよう指示
				iframeContent.postMessage({ action: 'initializePlayer', videoplay: 'manual' }, '*');

				//プレイヤーが見える位置までスクロール
				document.getElementById('detail_area').scrollIntoView({behavior: 'smooth', block: 'start'});

				//タイマーセット済みであれば
				if(typeof(Reflesh) == "number") {
					//今日の審議中継　メイン部分自動更新解除
					clearInterval( Reflesh ) ; 
				}

			}
		});
		$('#detail_area').append(iframe);

	});

}


//フォームから検索条件取得
function get_search_param(keyword_reuired=true){
	if($("#txt-search_area").is(':visible')){
		if($("#keyword").val()==""){
			if(keyword_reuired){
				alert("キーワードが未入力です。");
				return false;
			}
		}
		param=$("#search_form").serialize();
		param=param+"&m=k";
	}else if($("#search_area").is(':visible')){
		if(!date_sequence_check()){
			return false;	
		}
		param=$("form.search").serialize();
	}
	return param;
}

function get_search_result(param){
	del_more_link();//「さらに表示」リンク消去
	$('#detail_area').html("").hide();
	$(".pagination").hide();

	$("#method_area").html("").hide();
	$("#howto_area").html("").hide();
	$("#faq_area").html("").hide();
	$("#news").html("").hide();
	$(".searchRemark-list").remove();
	$("#live_list").remove();
	$("#result_area").show();
	$("#total_no").text("-");
	meetingname_height();
	waiting_for('#container');//ブロック
	$.ajax({
		url: "./keyword_search.php",
		data: param,
		cache: false,
		type: "post",
		success: function(data){
			$("#result_area").html(data);
			//add_more_link();//「さらに表示」リンク追加
			meetingname_height2();
			$('#container').unblock();//ブロック解除

			$(".pagination").show();

			//検索結果表示後の処理
			forSearchResult();
		}
	});
}


function pageno_click(){
	//ページ数クリック
	$(".page_no").css("cursor","pointer");
	$(document).on("click", ".page_no",function(event){
		event.preventDefault();

		var page_no = $(this).data('pageno');
		//alert('page_no=' + page_no);

		if($(this).hasClass("select")){return false;}
		//検索条件取得
		param=get_search_param(false);
		if(param!==false){
			param = param + "&page=" + page_no;
			//ページ送りの時には「searching」を空に
			param = param.replace(/searching=(on|tool)/, "searching=");
			//検索実行
			get_search_result(param);
		}
	});
}




//検索ボタンクリック時の処理
function search_click(){
	//フォームから検索条件取得
	param=get_search_param();
	if(param!==false){
		//デフォルトで選択されるタブ
		if ($("#txt-search_area").is(':visible')) {
			param = param + "&v=k";
		} else if (param.indexOf("&m=k&") > 0) {
			param = param + "&v=k";
		} else if (param.indexOf("&m=h&") > 0) {
			param = param + "&v=h";
		}

		//検索実行
		get_search_result(param);
	}
}



//メイン部分（ご利用方法）表示
function show_faq(){
	$("#method_area").html("").hide();
	////ご利用方法部分非表示
	$("#howto_area").html("").hide();
	////よくある質問部分非表示
	$("#faq_area").html("").hide();
	//メイン部分非表示
	$("#result_area").html("").hide();
	if(!$('#txt-search_area').is(':visible')){
		$("#search_area").hide();
		$("#txt-search_area").show();
	}

	//お知らせ部分非表示
	$("#news").html("").hide();

	$('#detail_area').html("").hide();


	meetingname_height();

	//よくある質問表示
	$.ajax({
	  url: "./faq.php",
	  cache: false,
	  type: "get",
	  success: function(data){
			$("#faq_area").show();
			$("#faq_area").html(data);
			faqLink_click();//ページ内リンククリック時の処理
			meetingname_height2();
		}
	});
}
//メイン部分（ご利用方法）表示
function show_howto(tid){
	if (typeof tid === "undefined") {
		tid = '';
	}

	$("#method_area").html("").hide();
	////ご利用方法部分非表示
	$("#howto_area").html("").hide();
	////よくある質問部分非表示
	$("#faq_area").html("").hide();
	//メイン部分非表示
	$("#result_area").html("").hide();
	if(!$('#txt-search_area').is(':visible')){
		$("#search_area").hide();
		$("#txt-search_area").show();
	}

	//お知らせ部分非表示
	$("#news").html("").hide();

	$('#detail_area').html("").hide();


	meetingname_height();
	
	//ご利用方法表示
	$.ajax({
	  url: "./howto.php",
	  cache: false,
	  type: "get",
	  success: function(data){
			$("#howto_area").show();
			$("#howto_area").html(data);
			meetingname_height2();

			if(tid!=''){
				//$.scrollTo("#"+tid, 200);
				document.getElementById(tid).scrollIntoView({behavior: 'smooth', block: 'start'});
			}

		}
	});
}

//検索方法表示
function show_method(){
	$('#detail_area').html("").hide();

	$("#howto_area").html("").hide();
	$("#faq_area").html("").hide();
	$("#news").html("").hide();
	$("#result_area").html("").hide();
	$("#method_area").fadeIn();
	meetingname_height();
	$.ajax({
		url: "./method.php",
		cache: false,
		type: "post",
		success: function(data){
			$("#method_area").html(data);
			meetingname_height2();
		}
	});
}

function more_result(){
	del_more_link();//「さらに表示」リンク消去
	//ブロックメッセージ表示中は処理しない
	if($(".blockUI").length>0) return false;
	//Loading表示中は処理しない
	if($("#loading_gif").length>0) return false;
	//詳細画面表示中は処理しない
	if($('#fancybox-content').is(':visible')) return false;
	//検索結果0件なら処理しない
	if($("#total_no").text()=="0") return false;
	//Fancybox表示中は処理しない
	if($("#fancybox-content:visible").length>0) return false;
	//検索結果最終データまで表示したら処理しない
	if($("#last_data_flg").length>0) return false;
	//Loading 表示
	$("#tab-box").append('<div class="searchRemark-list clearfix" id="loading_gif"><p class="photoThumb clearfix"><img src="./js/jQuery/loading.gif" alt="Now Loading..."> Now Loading...</p></div>');
	meetingname_height2();
	$.post("./keyword_search.php", "",
	function(data){
		//Loading 消去
		$("#loading_gif").remove();
		//取得コンテンツ追加
		$("#tab-box").append(data);

		meetingname_height2();

		//検索結果表示後の処理
		forSearchResult();

	});
}
function add_more_link(){
	//検索結果が0件でなくて最終データまで表示していなければリンク表示
	if(($("#total_no").text()!=="0")
	&&($("#last_data_flg").length==0)){
		$("#tab-box").append('<div class="searchRemark-list clearfix" id="more_result"><a href="#" id="more_result_link" class="font12px">［検索結果をさらに表示する］</a></div>');
	}
}
function del_more_link(){
	$("#more_result").remove();
	$("#more_result_link").remove();
}



$(document).ready(function() {
	//detail_click();
	detail2_click();
	modal_action();

	pageno_click();//ページ番号クリック時の処理

	keika_click();//会議の経過クリック時の処理

	forFaq();//よくある質問ページの処理


	// スマホで最下部に表示される「ページトップへ戻る」リンククリック時の処理
	gopagetop_click();



	//「基本検索に戻る」クリック
	$(document).on("click", "#basic-search",function(event){
		event.preventDefault();
		$("#search_area").slideUp();
		$("#txt-search_area").slideDown();
		$("#keyword").val($("#tx_word").val());
	});
	//「検索ツール」クリック
	$(document).on("click", "#detail-search",function(event){
		event.preventDefault();
		$("#txt-search_area").slideUp();
		$("#search_area").slideDown("normal",function(){meetingname_height2();});
		$("#tx_word").val($("#keyword").val());
	});

	//「検索方法」クリック
	$(document).on("click", "#search-method",function(event){
		event.preventDefault();
		show_method();
	});
	

	//会議名クリック
	$(document).on("click", ".kaigimei",function(event){
		event.preventDefault();
		$("#tx_kaigi_name").val($(this).text());
		$("#sel_kaigi_code").val($(this).attr("id").split("-")[1]);
		$("#sel_s_year").val(def_s_year);
		$("#sel_s_month").val(def_s_month);
		$("#sel_s_day").val(def_s_day);
		$("#sel_e_year").val(def_e_year);
		$("#sel_e_month").val(def_e_month);
		$("#sel_e_day").val(def_e_day);
		$("#tx_word").val("");
		$("#tx_speaker").val("");
		$("#tx_anken").val("");
		if(!$('#search_area').is(':visible')){
			$("#search_area").slideDown("fast");
			$("#txt-search_area").slideUp("fast",function(){search_click();});
		}else{
			search_click();
		}
	});

	//カレンダー日付のTDクリック時
	$(document).on("mouseover", ".clickable",function(event){
		$(this).addClass("hover");
	});
	$(document).on("mouseout", ".clickable",function(event){
		$(this).removeClass("hover");
	})
	$(document).on("click", "td.clickable > a",function(event){
		event.preventDefault();
		calendar_click($(this).attr("id"));
	});
	
	//カレンダー年・月セレクトボックス変更時
	$(document).on("change", "select.cal_sl",function(event){
		var m1 = parseInt($('#h_n_y').val(), 10) * 12 +  parseInt($('#h_n_m').val(), 10);//現在の年月
		var m2 = parseInt($('#cal_y').val(), 10) * 12 +  parseInt($('#cal_m').val(), 10);//指定された年月
		var diffMon = m2 - m1;
		if(diffMon > 0){
		//未来の年月が指定されたら現在の年月に変更
			$('#cal_y').val($('#h_n_y').val());
			$('#cal_m').val($('#h_n_m').val());
			diffMon = 0;
		}
		var m3 = parseInt($('#h_o_y').val(), 10) * 12 +  parseInt($('#h_o_m').val(), 10);//過去限界の年月
		if(parseInt(m2 - m3) < 0){
		//過去限界より過去の年月が指定されたら過去限界の年月に変更
			$('#cal_y').val($('#h_o_y').val());
			$('#cal_m').val($('#h_o_m').val());
			diffMon = m3 - m1;
		}
		m = ( "0" + $('#cal_m').val() ).slice(-2);
		ymd = $('#cal_y').val() + "-" + m  + "-" + "01";
		calendar_move(ymd);
	});

	//検索フォーム部分取得
	init_search();
	//お知らせ部分取得
	init_news();
	//カレンダー部分取得
	init_calendar();
	//会議リスト部分取得
	init_kaigilist();

	
	//検索ボタンクリック
	$(".search_btn").css("cursor","pointer");
	$(document).on("click", ".search_btn",function(event){
		event.preventDefault();
		search_click();
	});

	//タブ「会議を検索」クリック
	$("#kaigi_search").css("cursor","pointer");
	$(document).on("click", "#kaigi_search",function(event){
		event.preventDefault();
		if($(this).hasClass("selected")) return false;
		//検索条件取得
		param=get_search_param();
		if(param!==false){
//			param=param+"&m=k";
			param=param+"&v=k";
			//検索実行
			get_search_result(param);
		}
	});
	//タブ「発言内容を検索」クリック
	$("#hatsugen_search").css("cursor","pointer");
	$(document).on("click", "#hatsugen_search",function(event){
		event.preventDefault();
		if($(this).hasClass("selected")) return false;
		//フォームから検索条件取得
		param=get_search_param();
		if(param!==false){
//			param=param+"&m=h";
			param=param+"&v=h";
			//検索実行
			get_search_result(param);
		}
	});

	//メニュー「よくある質問」クリック
	$(document).on("click", ".menuFaq",function(event){
		//よくある質問表示
		show_faq();
		return false;
	});

	//メニュー「ご利用方法」クリック
	$(document).on("click", ".menuHowto",function(event){
		//ご利用方法表示
		show_howto();
		return false;
	});

	//よくある質問「動画視聴の便利な機能について」クリック
	$(document).on("click", ".menuHowtoUseful",function(event){
		//ご利用方法表示
		show_howto('useful');
		return false;
	});

	//よくある質問「公式Xについて」クリック
	$(document).on("click", ".menuHowtoXPolicy",function(event){
		//ご利用方法表示
		show_howto('xpolicy');
		return false;
	});
		

	$("#header_title").css("cursor","pointer").click(function(e) {location.href="/index.php";});

});



//よくある質問ページのアコーディオン処理
function checkWindowSizeFAQ() {
	if (window.matchMedia('(max-width: 919px)').matches) {
	//スマホはクリックで開閉できる
		$('.accordion-desc').hide(); // 初期状態で答えを隠す
		$(document).off('click', '.accordion-term').on('click', '.accordion-term', function() {
			$(this).next('.accordion-desc').slideToggle(); // クリックで開閉
		});
	} else if (window.matchMedia('(min-width: 920px)').matches) {
	//PCはすべて開いた状態でクリックしても開閉しない
		$('.accordion-desc').show(); // すべての答えを表示
		$(document).off('click', '.accordion-term'); // クリックイベントを解除
	}
}
function forFaq(){
    // 初回のチェック
    checkWindowSizeFAQ();

    // ウィンドウサイズ変更時のチェック
    $(window).resize(function() {
        checkWindowSizeFAQ();
    });

	// FAQ 「ページの先頭へ戻る」リンククリック時の処理
	$(document).on("click", 'a.faqLink[href^="#"]',function(event){
	//$('a.faqLink[href^="#"]').click(function(){
		var speed = 500;
		var href = $(this).attr("href");
		var target = $(href == "#" || href == ""? 'html':href);
		var position = target.offset().top - 20;
		$("html,body").animate({
			scrollTop: position
		},speed,"swing");
		return false;
	});
}

//検索結果表示後の処理
function forSearchResult(){
	//検索実行時に検索結果表示部分へのスクロール実施
	document.getElementById('result_area').scrollIntoView({behavior: 'smooth', block: 'start'});
}


// スマホで最下部に表示される「ページトップへ戻る」リンククリック時の処理
function gopagetop_click(){
	$(document).on("click", '#goPageTop',function(event){
		document.getElementById('header_title').scrollIntoView({behavior: 'smooth', block: 'start'});
		event.preventDefault();
	});	
}
