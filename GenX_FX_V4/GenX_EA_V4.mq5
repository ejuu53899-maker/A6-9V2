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

//--- global variables for remote control state
enum ENUM_OP_STATUS { OP_START, OP_STOP, OP_PAUSE };
ENUM_OP_STATUS CurrentOperationStatus = OP_START;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   Print("----------------------------------------------------------");
   Print("🚀 GenX EA V4 - REAL START");
   Print("Server Time: ", TimeToString(TimeCurrent(), TIME_DATE|TIME_SECONDS));
   Print("MT5 Build: ", TerminalInfoInteger(TERMINAL_BUILD));
   Print("----------------------------------------------------------");

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

   Print("Security tokens validated. Initializing with START status.");

   // Sync with bridge for initial remote status
   UpdateRemoteStatus();

   // Send initial performance update
   SendPerformanceUpdate();

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
   static int tick_count = 0;
   tick_count++;

   if(tick_count % 1000 == 0)
   {
      UpdateRemoteStatus();
   }

   if(CurrentOperationStatus == OP_STOP) return;

   if(CurrentOperationStatus == OP_PAUSE)
   {
      static bool pause_logged = false;
      if(!pause_logged) { Print("Trading is currently PAUSED via Remote Control."); pause_logged = true; }
      return;
   }

   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   if(tick_count % 100 == 0)
   {
      string data = "{\"symbol\":\"" + _Symbol + "\", " +
                    "\"bid\":" + DoubleToString(bid, _Digits) + ", " +
                    "\"ask\":" + DoubleToString(ask, _Digits) + ", " +
                    "\"lot_size\":" + DoubleToString(LotSize, 2) + ", " +
                    "\"tp\":" + DoubleToString(TargetProfit, 1) + ", " +
                    "\"sl\":" + DoubleToString(StopLoss, 1) + "}";

      SendDataToBridge(data, "/trade");
   }

   if(tick_count % 500 == 0)
   {
      SendPerformanceUpdate();
   }
}

//+------------------------------------------------------------------+
//| Function to fetch status from remote control bridge              |
//+------------------------------------------------------------------+
void UpdateRemoteStatus()
{
   char result[];
   string result_headers;
   string headers = "Authorization: Bearer " + JULES_API_KEY_V4 + "\r\n";

   int res = WebRequest("GET", BridgeURL + "/remote/status", headers, 5000, result, result, result_headers);

   if(res == 200)
   {
      string response = CharArrayToString(result, 0, WHOLE_ARRAY, CP_UTF8);
      if(StringFind(response, "\"status\": \"STOP\"") >= 0) { CurrentOperationStatus = OP_STOP; }
      else if(StringFind(response, "\"status\": \"PAUSE\"") >= 0) { CurrentOperationStatus = OP_PAUSE; }
      else { CurrentOperationStatus = OP_START; }
   }
}

//+------------------------------------------------------------------+
//| Function to send account performance update                      |
//+------------------------------------------------------------------+
void SendPerformanceUpdate()
{
   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   double pnl = AccountInfoDouble(ACCOUNT_PROFIT);
   long account = AccountInfoInteger(ACCOUNT_LOGIN);

   string data = "{\"account\":" + IntegerToString(account) + ", " +
                 "\"balance\":" + DoubleToString(balance, 2) + ", " +
                 "\"equity\":" + DoubleToString(equity, 2) + ", " +
                 "\"pnl\":" + DoubleToString(pnl, 2) + "}";

   SendDataToBridge(data, "/performance/update");
}

//+------------------------------------------------------------------+
//| Custom function to send data to Python bridge                    |
//+------------------------------------------------------------------+
bool SendDataToBridge(string data, string endpoint)
{
   char post_data[];
   char result[];
   string result_headers;
   string headers = "Content-Type: application/json\r\n" +
                    "Authorization: Bearer " + JULES_API_KEY_V4 + "\r\n" +
                    "X-GitHub-Token: " + GITHUB_TOKEN_PUSH + "\r\n";

   StringToCharArray(data, post_data, 0, StringLen(data), CP_UTF8);

   int res = WebRequest("POST", BridgeURL + endpoint, headers, 5000, post_data, result, result_headers);

   if(res == 200)
   {
      string response = CharArrayToString(result, 0, WHOLE_ARRAY, CP_UTF8);
      if(endpoint == "/trade")
      {
         Print("Bridge Response (Insights): ", response);
      }
      return true;
   }

   return false;
}
