<?php
// 火币ETH
define('ACCESS_KEY', 'da1ba4bc-78627048-4a27aefa-***'); // 访问密匙 请替换成自己的
define('SECRET_KEY', '8bad3d19-f6a188b2-fe334847-***'); // 访问私匙 请替换成自己的
// 使用 api_url
define('DOMAIN', 'be.huobi.com');
define('BASEURL', 'https://'.DOMAIN);
define('SYMBOL', 'ethcny');
define('METHOD', 'HmacSHA256');
define('VERSION', 2);
// get_account() 获取个人资产信息
//$account=get_account();
//$account=get_account_balance(101616);
//$str=creat_orderid(101616,0.001,1790,'buy-limit');
//$str=place_orderid(566667);
//$str=cancel_orderid(564218);
//$str=query_order(566667);
//$str=order_detail(566667);
//$str=get_orders();
//$str=get_trades();
//$str=creat_withdraw();
//POST /v1/dw/withdraw-virtual/{withdraw-id}/cancel 申请取消提现虚拟币
function cancel_withdraw($withdraw_id){
    $method_name = '查询当前用户的所有账户';
    $data = $extra = array();
    $action="/v1/dw/withdraw-virtual/".$withdraw_id."/cancel";
	$method="POST";
    $data=get_symbol_data();
	$extra=array(
		'withdraw-id'=>$withdraw_id
	);

	$data['Signature'] = eth_createSign($method,$action,$data);
    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url,json_encode($extra));
	return $tResult;
}

//POST /v1/dw/withdraw-virtual/{withdraw-id}/place 确认申请虚拟币提现
function place_withdraw($withdraw_id){
    $method_name = '查询当前用户的所有账户';
    $data = $extra = array();
    $action="/v1/dw/withdraw-virtual/".$withdraw_id."/place";
	$method="POST";
    $data=get_symbol_data();
	$extra=array(
		'withdraw-id'=>$withdraw_id
	);

	$data['Signature'] = eth_createSign($method,$action,$data);
    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url,json_encode($extra));
	return $tResult;
}

//POST /v1/dw/withdraw-virtual/create 申请提现虚拟币
function creat_withdraw($addressid,$amount){
    $method_name = '查询当前用户的所有账户';
    $data = $extra = array();
    $action="/v1/dw/withdraw-virtual/create";
	$method="POST";
    $data=get_symbol_data();
	$extra=array(
		'address-id'=>$addressid,
		'amount'=>$amount
	);

	$data['Signature'] = eth_createSign($method,$action,$data);
    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url,json_encode($extra));
	return $tResult;
}


//POST /v1/dw/withdraw-virtual/create 申请提现虚拟币
function creat_withdraw($addressid,$amount){
    $method_name = '查询当前用户的所有账户';
    $data = $extra = array();
    $action="/v1/dw/withdraw-virtual/create";
	$method="POST";
    $data=get_symbol_data();
	$extra=array(
		'address-id'=>$addressid,
		'amount'=>$amount
	);

	$data['Signature'] = eth_createSign($method,$action,$data);
    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url,json_encode($extra));
	return $tResult;
}

//GET /v1/dw/withdraw-virtual/addresses 查询虚拟币提现地址
function get_address(){
    $method_name = '查询当前用户的所有账户';
    $data =$extra=array();
    $action="/v1/dw/withdraw-virtual/addresses";
	$method="GET";
    $data=get_symbol_data();
	$extra=array(
		'currency'=>'eth'
	);
    $data['Signature'] = eth_createSign($method,$action,array_merge($data,$extra));
    $tPreSign = http_build_query(array_merge($data,$extra));
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url);
    return $tResult;
}

//GET /v1/order/matchresults 查询当前成交、历史成交
function get_trades(){
    $method_name = '查询当前用户的所有账户';
    $data =$extra=array();
    $action="/v1/order/matchresults";
	$method="GET";
    $data=get_symbol_data();
	$extra=array(
		'symbol'=>SYMBOL,
		'types'=>'buy-limit,sell-limit'
	);
    $data['Signature'] = eth_createSign($method,$action,array_merge($data,$extra));
    $tPreSign = http_build_query(array_merge($data,$extra));
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url);
    return $tResult;
}

//GET /v1/order/orders 查询当前委托、历史委托
function get_orders(){
    $method_name = '查询当前用户的所有账户';
    $data =$extra=array();
    $action="/v1/order/orders";
	$method="GET";
    $data=get_symbol_data();
	$extra=array(
		'symbol'=>SYMBOL,
		'states'=>"pre-submitted,submitted,canceled,filled",
		'types'=>'buy-limit,sell-limit'
	);
    $data['Signature'] = eth_createSign($method,$action,array_merge($data,$extra));
    $tPreSign = http_build_query(array_merge($data,$extra));
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url);
    return $tResult;
}

//GET /v1/order/orders/{order-id}/matchresults 查询某个订单的成交明细
function order_detail($orderid){
    $method_name = '查询当前用户的所有账户';
    $data =$extra=array();
    $action="/v1/order/orders/".$orderid."/matchresults";
	$method="GET";
    $data=get_symbol_data();
	$extra=array(
		'order-id'=>$orderid
	);
    $data['Signature'] = eth_createSign($method,$action,array_merge($data,$extra));
    $tPreSign = http_build_query(array_merge($data,$extra));
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url);
    return $tResult;
}


//GET /v1/order/orders/{order-id} 查询某个订单详情
function query_order($orderid){
    $method_name = '查询当前用户的所有账户';
    $data =$extra=array();
    $action="/v1/order/orders/".$orderid;
	$method="GET";
    $data=get_symbol_data();
	$extra=array(
		'order-id'=>$orderid,
	);
    $data['Signature'] = eth_createSign($method,$action,array_merge($data,$extra));
    $tPreSign = http_build_query(array_merge($data,$extra));
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url);
    return $tResult;
}


//POST /v1/order/orders/{order-id}/submitcancel 申请撤销一个订单请求
function cancel_orderid($orderid){
    $method_name = '查询当前用户的所有账户';
    $data = $extra = array();
    $action="/v1/order/orders/".$orderid."/submitcancel";
	$method="POST";
    $data=get_symbol_data();
	$extra=array(
		'order-id'=>$orderid,
	);

	$data['Signature'] = eth_createSign($method,$action,$data);
    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url,json_encode($extra));
	return $tResult;
}

//POST /v1/order/orders/{order-id}/place 执行一个订单
function place_orderid($orderid){
    $method_name = '查询当前用户的所有账户';
    $data = $extra = array();
    $action="/v1/order/orders/".$orderid."/place";
	$method="POST";
    $data=get_symbol_data();
	$extra=array(
		'order-id'=>$orderid,
	);
	$data['Signature'] = eth_createSign($method,$action,$data);
    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url,json_encode($extra));
	return $tResult;
}

//POST /v1/order/orders 创建一个新的订单请求
function creat_orderid($account_id,$amount,$price,$type){
    $method_name = '查询当前用户的所有账户';
    $data = $extra = array();
    $action="/v1/order/orders";
	$method="POST";
    $data=get_symbol_data();
	$extra=array(
		'account-id'=>$account_id,
		'amount'=>$amount,
		'price'=>$price,
		'source'=>'api',
		'symbol'=>'ethcny',
		'type'=>$type
	);
	$data['Signature'] = eth_createSign($method,$action,$data);
    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url,json_encode($extra));
	return $tResult;
}
//GET v1/account/accounts
function get_account(){
    $method_name = '查询当前用户的所有账户';
    $data =$extra=array();
    $action="/v1/account/accounts";
	$method="GET";
    $data=get_symbol_data();
    $data['Signature'] = eth_createSign($method,$action,$data);

    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url);
    return $tResult;
}

//GET /v1/account/accounts/{account-id}/balance
function get_account_balance($account_id){
    $method_name = '查询当前用户的所有账户';
    $data = $extra = array();
    $action="/v1/account/accounts/".$account_id."/balance";
	$method="GET";
    $data=get_symbol_data();
	$extra['account-id']=$account_id;
	$data=array_merge($data,$extra);
	$data['Signature'] = eth_createSign($method,$action,$data);
    $tPreSign = http_build_query($data);
    $api_url=BASEURL.$action."?".$tPreSign;
    $tResult = httpRequest($api_url);
	return $tResult;
}


//返回秘钥
function get_symbol_data(){
	return $data=array(
        'AccessKeyId'=>ACCESS_KEY,
        'SignatureMethod'=>METHOD,
        'SignatureVersion'=>VERSION,
        'Timestamp'=>get_utcTime()
    );
}
//get_utcTime
function get_utcTime(){
    return gmdate("Y-m-d\TH:i:s",time());
}
//createSign
function eth_createSign($method,$action,$data){
    ksort($data);
    $msg=$method."\n".DOMAIN."\n".$action."\n".http_build_query($data);
    $sign = hash_hmac('sha256', $msg, SECRET_KEY, true);
    return base64_encode($sign);
}
/**
 * 发送信息到api
 */
function httpRequest($pUrl,$pData){
	$tCh = curl_init();
	if($pData){
		is_array($pData) && $pData = http_build_query($pData);
		curl_setopt($tCh, CURLOPT_POST, true);
		curl_setopt($tCh, CURLOPT_POSTFIELDS, $pData);
	}
	curl_setopt($tCh, CURLOPT_HTTPHEADER, array("Content-type:application/json;charset=UTF-8"));
	curl_setopt($tCh, CURLOPT_URL, $pUrl);
	curl_setopt($tCh, CURLOPT_CONNECTTIMEOUT, 5);
	curl_setopt($tCh, CURLOPT_TIMEOUT, 10);
	curl_setopt($tCh, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($tCh, CURLOPT_SSL_VERIFYPEER, false);
	$tResult = curl_exec($tCh);
	curl_close($tCh);
	return $tResult;
}