//+------------------------------------------------------------------+
//|                                              GenX_EA_V4.mq5      |
//|                                  Copyright 2026, GenX FX Trading |
//|                                             https://genxfx.com   |
//+------------------------------------------------------------------+
#property copyright "Copyright 2026, GenX FX Trading"
#property link      "https://genxfx.com"
#property version   "4.10"
#property strict

//--- input parameters
input string   JULES_API_KEY_V4 = "YOUR_API_KEY_HERE"; // API Key for authentication
input string   GITHUB_TOKEN_PUSH = "YOUR_GITHUB_TOKEN_HERE"; // GitHub Token for push operations
input double   TargetProfit      = 100.0;              // Target Profit in points
input double   StopLoss          = 50.0;               // Stop Loss in points
input double   LotSize           = 0.1;                // Trading Lot Size
input string   BridgeURL         = "http://localhost:8000"; // Bridge Server URL
input int      MaxRetries        = 3;                  // Max retries on connection failure
input int      RetryDelay        = 1000;               // Delay between retries in ms

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   Print("GenX EA V4.10 (Optimized) Initializing...");

   if(JULES_API_KEY_V4 == "YOUR_API_KEY_HERE" || JULES_API_KEY_V4 == "")
   {
      Print("Error: JULES_API_KEY_V4 is not set correctly.");
      return(INIT_PARAMETERS_INCORRECT);
   }

   if(GITHUB_TOKEN_PUSH == "YOUR_GITHUB_TOKEN_HERE" || GITHUB_TOKEN_PUSH == "")
   {
      Print("Error: GITHUB_TOKEN_PUSH is not set correctly.");
      return(INIT_PARAMETERS_INCORRECT);
   }

   Print("Security tokens validated. Bridge communication enabled.");
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   Print("GenX EA V4 shutting down. Reason code: ", reason);
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   static int tick_count = 0;
   tick_count++;

   // Send data every 100 ticks for performance optimization
   if(tick_count % 100 == 0)
   {
      string data = "{\"symbol\":\"" + _Symbol + "\", " +
                    "\"bid\":" + DoubleToString(bid, _Digits) + ", " +
                    "\"ask\":" + DoubleToString(ask, _Digits) + ", " +
                    "\"lot_size\":" + DoubleToString(LotSize, 2) + ", " +
                    "\"tp\":" + DoubleToString(TargetProfit, 1) + ", " +
                    "\"sl\":" + DoubleToString(StopLoss, 1) + ", " +
                    "\"timestamp\":" + IntegerToString(TimeCurrent()) + "}";

      SendDataWithRetry(data);
   }
}

//+------------------------------------------------------------------+
//| Enhanced function to send data with retry logic                  |
//+------------------------------------------------------------------+
bool SendDataWithRetry(string data)
{
   for(int i=0; i<MaxRetries; i++)
   {
      if(SendDataToBridge(data)) return true;

      Print("Retry ", i+1, " of ", MaxRetries, " after failure...");
      Sleep(RetryDelay);
   }
   Print("Failed to send data to bridge after ", MaxRetries, " attempts.");
   return false;
}

//+------------------------------------------------------------------+
//| Custom function to send data to Python bridge                    |
//+------------------------------------------------------------------+
bool SendDataToBridge(string data)
{
   char post_data[];
   char result[];
   string result_headers;
   string headers = "Content-Type: application/json\r\n" +
                    "Authorization: Bearer " + JULES_API_KEY_V4 + "\r\n" +
                    "X-GitHub-Token: " + GITHUB_TOKEN_PUSH + "\r\n";

   StringToCharArray(data, post_data, 0, StringLen(data), CP_UTF8);

   // Increase timeout to 5000ms for concurrent handling
   int res = WebRequest("POST", BridgeURL, headers, 5000, post_data, result, result_headers);

   if(res == -1)
   {
      Print("WebRequest error: ", GetLastError());
      return false;
   }
   else if(res == 200)
   {
      return true;
   }
   else
   {
      Print("Bridge returned status: ", res, ". Response: ", CharArrayToString(result));
      return false;
   }
}
