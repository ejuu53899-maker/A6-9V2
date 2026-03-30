//+------------------------------------------------------------------+
//|                                              GenX_EA_V4.mq5      |
//|                                  Copyright 2026, GenX FX Trading |
//|                                             https://genxfx.com   |
//+------------------------------------------------------------------+
#property copyright "Copyright 2026, GenX FX Trading"
#property link      "https://genxfx.com"
#property version   "4.00"
#property strict

//--- input parameters
input string   JULES_API_KEY_V4 = "YOUR_API_KEY_HERE"; // API Key for authentication
input string   GITHUB_TOKEN_PUSH = "YOUR_GITHUB_TOKEN_HERE"; // GitHub Token for push operations
input double   TargetProfit      = 100.0;              // Target Profit in points
input double   StopLoss          = 50.0;               // Stop Loss in points
input double   LotSize           = 0.1;                // Trading Lot Size
input string   BridgeURL         = "http://localhost:8000"; // Bridge Server URL

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   Print("GenX EA V4 Initializing...");

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

   Print("Security tokens validated. Ready to start.");
   Print("Configuration: LotSize=", LotSize, " TP=", TargetProfit, " SL=", StopLoss);

   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   Print("GenX EA V4 shutting down. Reason: ", reason);
}

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
{
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   // Print every 100th tick and send data to bridge for demo purposes
   static int tick_count = 0;
   tick_count++;
   if(tick_count % 100 == 0)
   {
      Print("Current Tick - Symbol: ", _Symbol, " Bid: ", bid, " Ask: ", ask);

      // Constructing JSON data including user parameters
      string data = "{\"symbol\":\"" + _Symbol + "\", " +
                    "\"bid\":" + DoubleToString(bid, _Digits) + ", " +
                    "\"ask\":" + DoubleToString(ask, _Digits) + ", " +
                    "\"lot_size\":" + DoubleToString(LotSize, 2) + ", " +
                    "\"tp\":" + DoubleToString(TargetProfit, 1) + ", " +
                    "\"sl\":" + DoubleToString(StopLoss, 1) + "}";

      SendDataToBridge(data);
   }
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

   // Using StringLen(data) to exclude the null terminator as per code review feedback
   StringToCharArray(data, post_data, 0, StringLen(data), CP_UTF8);

   int res = WebRequest("POST", BridgeURL, headers, 5000, post_data, result, result_headers);

   if(res == -1)
   {
      Print("Error in WebRequest: ", GetLastError());
      return false;
   }
   else if(res == 200)
   {
      Print("Data successfully sent to bridge.");
      return true;
   }
   else
   {
      Print("Bridge returned error code: ", res);
      return false;
   }
}
