package com.huobi.api;

import java.io.IOException;
import java.util.List;

import com.huobi.api.request.CreateOrderRequest;
import com.huobi.api.response.Account;

public class Main {

  static final String API_KEY = "your-api-key";
  static final String API_SECRET = "your-api-secret";

  public static void main(String[] args) {
    try {
      apiSample();
    } catch (ApiException e) {
      System.err.println("API Error! err-code: " + e.getErrCode() + ", err-msg: " + e.getMessage());
      e.printStackTrace();
    }
  }

  static void apiSample() {
    // create ApiClient using your api key and api secret:
    ApiClient client = new ApiClient(API_KEY, API_SECRET);
    // get symbol list:
    print(client.getSymbols());
    // get accounts:
    List<Account> accounts = client.getAccounts();
    print(accounts);
    if (!accounts.isEmpty()) {
      // find account id:
      Account account = accounts.get(0);
      long accountId = account.id;
      // create order:
      CreateOrderRequest createOrderReq = new CreateOrderRequest();
      createOrderReq.accountId = String.valueOf(accountId);
      createOrderReq.amount = "0.02";
      createOrderReq.price = "1100.99";
      createOrderReq.symbol = "ethcny";
      createOrderReq.type = CreateOrderRequest.OrderType.BUY_LIMIT;
      Long orderId = client.createOrder(createOrderReq);
      print(orderId);
      // place order:
      String r = client.placeOrder(orderId);
      print(r);
    }
  }

  static void print(Object obj) {
    try {
      System.out.println(JsonUtil.writeValue(obj));
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
