/**
 * weixin register/login 
 * @authors Vee (vee@lagou.com)
 * @date    2014-08-18 16:29:15
 * @version $1.0$
 */
$(function(){
	//show password or not
	$('.new_register i.eye').click(function(){
		if($(this).hasClass('openeye')){
			$(this).removeClass('openeye');
			$(this).siblings('.r_psw').attr("type","password");
		}else{
			$(this).addClass('openeye');
			$(this).siblings('.r_psw').attr("type","text");
		}
	});

	$('.new_register select').each(function(){
		if($(this).val() == '' || $(this).val() == null){
			$(this).css('color','#aeaeae');
		}else{
			$(this).css('color','#333');
		}
	});

	//validate
	$('.r_email').keyup(function(){
		var email = $(this).val();
		if($.trim(email) != '' && checkEmail(email)){
			$(this).siblings('.err_email').hide(100);
		}
	});

	$('.r_psw').keyup(function(){
		var psw = $(this).val();
		if(psw != '' && checkPsw(psw)){
			$(this).siblings('.err_psw').hide(100);
		}
	});

	$('.r_phone').keyup(function(){
		var phone = $(this).val();
		if(phone != '' && checkPhone(phone)){
			$(this).siblings('.err_phone').hide(100);
		}
	});

	$('.r_name').keyup(function(){
		var name = $(this).val();
		if($.trim(name) != '' && $.trim(name).length <= 20){
			$(this).siblings('.err_name').hide(100);
		}
	});

	$('.r_edu').change(function(){
		var edu = $(this).val();
		if(edu != ''){
			$(this).css('color','#333').siblings('.err_edu').hide(100);
		}
	});
	$('.r_year').change(function(){
		var year = $(this).val();
		if(year != ''){
			$(this).css('color','#333').siblings('.err_year').hide(100);
		}
	});

	$('#registerForm').submit(function(e){
		var _email = $(this).find('.r_email');
		var _psw = $(this).find('.r_psw');
		var email = _email.val();
		var psw = _psw.val();
		
		var otype = $("#otype").val();
		
		var error = false;
		if($.trim(email) == ''){
			_email.siblings('.err_email').html('<em>!</em>填写邮箱').show(100);
			error = true;
		}else if(!checkEmail(email)){
			_email.siblings('.err_email').html('<em>!</em>无效邮箱').show(100);
			error = true;
		}
		if(!checkPsw(psw)){
			_psw.siblings('.err_psw').show(100);
			error = true;
		}
		if(error){
			return false;
		}else{
			$.ajax({
				url:ctx+'/mobile/regist.json?otype='+otype,
				type:'POST',
				data:{email:email,password:psw},
				dataType:'json'
			}).done(function(result){
				if(result.success){
					if(result.content.indexOf("http://",0)>=0){
						window.location.href = result.content;
					}else{
						window.location.href = ctx+"/"+result.content;
					}
				}else{
					if(result.code=='-1'){
						_email.siblings('.err_email').html('<em>!</em>邮箱已被注册').show(100);
					}else{
						_email.siblings('.err_email').html('<em>!</em>'+result.msg).show(100);
					}
					return false;
				}
			});
			return false;
		}
	});

	$('#loginForm').submit(function(e){
		var _email = $(this).find('.r_email');
		var _psw = $(this).find('.r_psw');
		var email = _email.val();
		var psw = _psw.val();
		
		var otype = $("#otype").val();
		
		var error = false;
		if($.trim(email) == ''){
			_email.siblings('.err_email').html('<em>!</em>填写邮箱').show(100);
			error = true;
		}else if(!checkEmail(email)){
			_email.siblings('.err_email').html('<em>!</em>无效邮箱').show(100);
			error = true;
		}
		if(!checkPsw(psw)){
			_psw.siblings('.err_psw').show(100);
			error = true;
		}
		if(error){
			return false;
		}else{
			$.ajax({
				url:ctx+'/mobile/login.json?otype='+otype,
				type:'POST',
				data:{email:email,password:psw},
				dataType:'json'
			}).done(function(result){
				if(result.success){
					if(result.content.indexOf("http://",0)>=0){
						window.location.href = result.content;
					}else{
						window.location.href = ctx+"/"+result.content;
					}
				}else{
					if(result.code=='-1'){
						popMsg('(⊙o⊙)…帐号不存在或密码错误，请重新填写');
						return false;
					}else if(result.code=='-2'){
						popMsg('账号绑定失败,请进入拉勾微信服务号进行账号绑定！');
						return false;
					}
					_email.siblings('.err_email').html('<em>!</em>无效邮箱').show(100);
					return false;
				}
			});
			return false;
		}
	});

	$('#stepForm1').submit(function(e){
		var _name = $(this).find('.r_name');
		var _edu = $(this).find('.r_edu');
		var _year = $(this).find('.r_year');
		
		var name = _name.val();
		var edu = _edu.val();
		var year = _year.val();
		
		var otype = $("#otype").val();
		var phone = $("#phone").val();
		if(phone!=''){
			phone = encodeURI(phone);
		}
		
		var error = false;
		if($.trim(name) == '' || $.trim(name).length > 20){
			_name.siblings('.err_name').show(100);
			error = true;
		}
		if(edu == '' || edu == null){
			_edu.siblings('.err_edu').show(100);
			error = true;
		}
		if(year == '' || year == null){
			_year.siblings('.err_year').show(100);
			error = true;
		}
		if(error){
			return false;
		}else{
			$.ajax({
				url:ctx+'/mobile/perfectBasicInfo.json?step=1&otype='+otype+'&tphone='+phone,  //step1
				type:'POST',
				data:{name:name,highestEducation:edu,workYear:year},
				dataType:'json'
			}).done(function(result){
				if(result.success){
					if(result.content.indexOf("http://",0)>=0){
						window.location.href = result.content;
					}else{
						window.location.href = ctx+"/"+result.content;
					}
				}else{
					popMsg(result.msg);
					return false;
				}
			});
			return false;
		}
	});
	
	$('#stepForm2').submit(function(e){
		var _email = $(this).find('.r_email');
		var _phone = $(this).find('.r_phone');
		
		var email = _email.val();
		var phone = _phone.val();
		
		var otype = $("#otype").val();
		
		var error = false;
		if($.trim(phone) == ''){
			_email.siblings('.err_phone').html('<em>!</em>填写手机号').show(100);
			error = true;
		}else if(!checkPhone(phone)){
			_phone.siblings('.err_phone').html('<em>!</em>无效手机号').show(100);
			error = true;
		}
		if($.trim(email) == ''){
			_email.siblings('.err_email').html('<em>!</em>填写邮箱').show(100);
			error = true;
		}else if(!checkEmail(email)){
			_email.siblings('.err_email').html('<em>!</em>无效邮箱').show(100);
			error = true;
		}
		if(error){
			return false;
		}else{
			$.ajax({
				url:ctx+'/mobile/perfectBasicInfo.json?step=2&otype='+otype,  //step2
				type:'POST',
				data:{email:email,phone:phone},
				dataType:'json'
			}).done(function(result){
				if(result.success){
					if(result.content.indexOf("http://",0)>=0){
						window.location.href = result.content;
					}else{
						window.location.href = ctx+"/"+result.content;
					}
				}else{
					popMsg(result.msg);
					return false;
				}
			});
			return false;
		}
	});

	//resend email
	$('#resendEmail').click(function(){
		var email = $('.active_text span').text();
		var otype = $("#otype").val();
		$.ajax({
			url:ctx+'/mobile/reActivateAccount.json?otype='+otype,
			type:'POST',
			data:{email:email},
			dataType:'json'
		}).done(function(result){
			if(result.success){
				popMsg('验证邮件发送成功');
			}else{
				if(result.msg=='' || result.msg==null || result.msg=='null'){
					popMsg("请重新登录!");
					return false;
				}else{
					popMsg(result.msg);
					return false;
				}
			}
		});
	});
	
	$("#lastStep").click(function(){
		//${base}/mobile/perfectBasicInfo.html?step=1&otype=${otype}
		var otype = $("#otype").val();
		var phone = $("#phone").val();
		if(phone!=''){
			phone = encodeURI(phone);
		}
		window.location.href = ctx+"/mobile/perfectBasicInfo.html?step=1&otype="+otype+"&tphone="+phone;
	});

	function popMsg(msg){
		$('body').append('<div id="popLayer">'+msg+'</div>');
		$('#popLayer').addClass('pop');
		setTimeout(function(){$('#popLayer').removeClass('pop')},3000);
	}
	
	//valid funcitons
	function checkEmail(email){
		var reg = /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i;
		if(!reg.test($.trim(email))){
			return false;
		}else{
			return true;
		}
	}
	function checkPsw(psw){
		var len = $.trim(psw).length;
		if(len<6 || len > 16){
			return false;
		}else{
			return true;
		}
	}
	function checkPhone(phone){
		var pattern= /(^1[3,4,5,7,8]{1}[0-9]{9}$)/;
		if(pattern.test($.trim(phone))){ 
			return true; 
		}else{ 
			return false; 
		} 
	}
	function checkName(name){
		var len = name.length;
		if(len<1 || len > 20){
			return false;
		}else{
			return true;
		}
	}
});
