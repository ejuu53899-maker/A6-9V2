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

   Print("API Key V4 validated. Ready to start.");
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
      string data = "{\"symbol\":\"" + _Symbol + "\", \"bid\":" + DoubleToString(bid, _Digits) + ", \"ask\":" + DoubleToString(ask, _Digits) + "}";
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
   string headers = "Content-Type: application/json\r\nAuthorization: Bearer " + JULES_API_KEY_V4 + "\r\n";

   StringToCharArray(data, post_data, 0, WHOLE_ARRAY, CP_UTF8);

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
