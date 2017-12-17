using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Net;
using System.Security.Cryptography;
using System.Text;

namespace MarketApi.Market
{
    public class HuobiDemo
    {
        private string accessKey = "";
        private string secretKey = "";

        private const string domain = "be.huobi.com";
        private string baseUrl = $"https://{domain}";
        private string symbol = "ethcny";
        private const string SignatureMethod = "HmacSHA256";
        private const int SignatureVersion = 2;
        public string Accounts()
        {
            var action = "/v1/account/accounts";
            var method = "GET";
            var data = new Dictionary<string, object>()
            {
                {"AccessKeyId", accessKey},
                {"SignatureMethod", SignatureMethod},
                {"SignatureVersion", SignatureVersion},
                {"Timestamp", GetDateTime()},
            };
            var sign = CreateSign(method, action, secretKey, data);
            data["Signature"] = sign;
            var url = $"{baseUrl}{action}?{ConvertQueryString(data, true)}";
            int statusCode;
            var result = RequestDataSync(url, method, null, null, out statusCode);
            Debug.WriteLine(result);
            return result;
        }

        private string GetDateTime() => DateTime.UtcNow.ToString("yyyy-MM-ddTHH:mm:ss");

        public string AccountBalance(string accountId)
        {
            var action = $"/v1/account/accounts/{accountId}/balance";
            var method = "GET";
            var data = new Dictionary<string, object>()
            {
                {"AccessKeyId", accessKey},
                {"SignatureMethod", SignatureMethod},
                {"SignatureVersion", SignatureVersion},
                {"Timestamp", GetDateTime()},
                {"account-id", accountId}
            };
            var sign = CreateSign(method, action, secretKey, data);
            data["Signature"] = sign;
            var url = $"{baseUrl}{action}?{ConvertQueryString(data, true)}";
            int statusCode;
            var result = RequestDataSync(url, method, null, null, out statusCode);
            Debug.WriteLine(result);
            return result;
        }

        public string NewOrder(string accountId, decimal amount, decimal price, string type)
        {
            var action = $"/v1/order/orders";
            var method = "POST";
            var data = new Dictionary<string, object>()
            {
                {"AccessKeyId", accessKey},
                {"SignatureMethod", SignatureMethod},
                {"SignatureVersion", SignatureVersion},
                {"Timestamp", GetDateTime()},
            };
            var sign = CreateSign(method, action, secretKey, data);
            data["Signature"] = sign;

            var postData = new Dictionary<string, object>()
            {
                {"account-id", accountId},
                {"amount", amount},
                {"price", price},
                {"symbol", symbol},
                {"type", type}
            };
            var url = $"{baseUrl}{action}?{ConvertQueryString(data, true)}";
            int statusCode;
            var result = RequestDataSync(url, method, postData, null, out statusCode);
            Debug.WriteLine(result);
            return result;
        }

        public string PlaceOrder(string orderId)
        {
            var action = $"/v1/order/orders/{orderId}/place";
            var method = "POST";
            var data = new Dictionary<string, object>()
            {
                {"AccessKeyId", accessKey},
                {"SignatureMethod", SignatureMethod},
                {"SignatureVersion", SignatureVersion},
                {"Timestamp", GetDateTime()},
                {"order-id", orderId}
            };
            var sign = CreateSign(method, action, secretKey, data);
            data["Signature"] = sign;
            var url = $"{baseUrl}{action}?{ConvertQueryString(data, true)}";
            int statusCode;
            var result = RequestDataSync(url, method, null, null, out statusCode);
            Debug.WriteLine(result);
            return result;
        }

        public string CancelOrder(string orderId)
        {
            var action = $"/v1/order/orders/{orderId}/submitcancel";
            var method = "POST";
            var data = new Dictionary<string, object>()
            {
                {"AccessKeyId", accessKey},
                {"SignatureMethod", SignatureMethod},
                {"SignatureVersion", SignatureVersion},
                {"Timestamp", GetDateTime()},
                {"order-id", orderId}
            };
            var sign = CreateSign(method, action, secretKey, data);
            data["Signature"] = sign;
            var url = $"{baseUrl}{action}?{ConvertQueryString(data, true)}";
            int statusCode;
            var result = RequestDataSync(url, method, null, null, out statusCode);
            Debug.WriteLine(result);
            return result;
        }

        public string QueryOrder(string orderId)
        {
            var action = $"/v1/order/orders/{orderId}";
            var method = "GET";
            var data = new Dictionary<string, object>()
            {
                {"AccessKeyId", accessKey},
                {"SignatureMethod", SignatureMethod},
                {"SignatureVersion", SignatureVersion},
                {"Timestamp", GetDateTime()},
                {"order-id", orderId}
            };
            var sign = CreateSign(method, action, secretKey, data);
            data["Signature"] = sign;
            var url = $"{baseUrl}{action}?{ConvertQueryString(data, true)}";
            int statusCode;
            var result = RequestDataSync(url, method, data, null, out statusCode);
            Debug.WriteLine(result);
            return result;
        }

        public string QueryDetail(string orderId)
        {
            var action = $"/v1/order/orders/{orderId}/matchresults";
            var method = "GET";
            var data = new Dictionary<string, object>()
            {
                {"AccessKeyId", accessKey},
                {"SignatureMethod", SignatureMethod},
                {"SignatureVersion", SignatureVersion},
                {"Timestamp", GetDateTime()},
                {"order-id", orderId}
            };
            var sign = CreateSign(method, action, secretKey, data);
            data["Signature"] = sign;
            var url = $"{baseUrl}{action}?{ConvertQueryString(data, true)}";
            int statusCode;
            var result = RequestDataSync(url, method, data, null, out statusCode);
            Debug.WriteLine(result);
            //如果订单没有成交记录(比如已经撤单的订单)会返回{"status":"error","err-code":"base-record-invalid","err-msg":"record invalid","data":null}
            return result;
        }

        public string GetOrders()
        {
            var action = $"/v1/order/orders";
            var method = "GET";
            var data = new Dictionary<string, object>()
            {
                {"AccessKeyId", accessKey},
                {"SignatureMethod", SignatureMethod},
                {"SignatureVersion", SignatureVersion},
                {"Timestamp", GetDateTime()},
                {"states", "submitted"},
                {"symbol", symbol},
                {"types","buy-limit,sell-limit"},
            };
            var sign = CreateSign(method, action, secretKey, data);
            data["Signature"] = sign;
            var url = $"{baseUrl}{action}?{ConvertQueryString(data, true)}";
            int statusCode;
            var result = RequestDataSync(url, method, data, null, out statusCode);
            Debug.WriteLine(result);
            return result;
        }

        private string RequestDataSync(string url, string method, Dictionary<string, object> param, WebHeaderCollection headers, out int httpCode)
        {
            string resp = string.Empty;
            httpCode = 200;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Headers.Add("Accept-Encoding", "gzip");
            request.Method = method;

            if (headers != null)
            {
                foreach (var key in headers.AllKeys)
                {
                    request.Headers.Add(key, headers[key]);
                }
            }
            try
            {
                if (method == "POST" && param != null)
                {
                    byte[] bs = Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(param));
                    request.ContentType = "application/json";
                    request.ContentLength = bs.Length;
                    using (var reqStream = request.GetRequestStream())
                    {
                        reqStream.Write(bs, 0, bs.Length);
                    }
                }
                //如果是Get 请求参数附加在URL之后
                using (HttpWebResponse response = request.GetResponse() as HttpWebResponse)
                {
                    if (resp == null)
                        throw new Exception("Response is null");
                    resp = GetResponseBody(response);
                    httpCode = (int)response.StatusCode;
                }
            }
            catch (WebException ex)
            {
                using (HttpWebResponse response = ex.Response as HttpWebResponse)
                {
                    resp = GetResponseBody(response);
                    httpCode = (int)response.StatusCode;
                }
            }
            return resp;
        }
        private string GetResponseBody(HttpWebResponse response)
        {
            var readStream = new Func<Stream, string>((stream) =>
            {
                using (var reader = new StreamReader(stream, Encoding.UTF8))
                {
                    return reader.ReadToEnd();
                }
            });

            using (var responseStream = response.GetResponseStream())
            {
                if (response.ContentEncoding.ToLower().Contains("gzip"))
                {
                    using (GZipStream stream = new GZipStream(responseStream, CompressionMode.Decompress))
                    {
                        return readStream(stream);
                    }
                }
                if (response.ContentEncoding.ToLower().Contains("deflate"))
                {
                    using (DeflateStream stream = new DeflateStream(responseStream, CompressionMode.Decompress))
                    {
                        return readStream(stream);
                    }
                }
                return readStream(responseStream);
            }
        }

        private string CreateSign(string method, string action, string secretKey, Dictionary<string, object> data)
        {
            var hashSource = $"{method}\n{domain.ToLower()}\n{action}\n";
            if (data != null)
            {
                hashSource += ConvertQueryString(data, true);
            }
            var hmacSha256 = new HMACSHA256(Encoding.UTF8.GetBytes(secretKey));
            var hash = hmacSha256.ComputeHash(Encoding.UTF8.GetBytes(hashSource)).ToArray();
            return Convert.ToBase64String(hash);
        }

        private string ConvertQueryString(Dictionary<string, object> data, bool urlencode = false)
        {
            var stringbuilder = new StringBuilder();
            foreach (var item in data)
            {
                stringbuilder.AppendFormat("{0}={1}&", item.Key, urlencode ? Uri.EscapeDataString(item.Value.ToString()) : item.Value.ToString());
            }
            stringbuilder.Remove(stringbuilder.Length - 1, 1);
            return stringbuilder.ToString();
        }
    }
}