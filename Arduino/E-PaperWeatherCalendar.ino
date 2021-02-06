/* Includes*/
#include<WiFi.h>
#include<ArduinoJson.h>
#include<HTTPClient.h>
#include <WiFiClientSecure.h>
#include "time.h"
#include "DEV_Config.h"
#include "EPD.h"
#include "GUI_Paint.h"
#include "imagedata.h"
#include "PoemsData.h"
#include <stdlib.h>

/*WiFi settings*/
/*Replace with your own WiFi Settings*/
const char* ssid = "*********";
const char* password = "*********";
/*Time settings*/
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 8 * 3600;
const int   daylightOffset_sec = 8 * 3600;
/*HeWeather settings*/
/*Replace with your own heWeatherKey*/
String heWeatherKey = "*************************";
/*Information of weather and location*/
String locationID;
String cityCN ;
String temp;
String icon;
String text;
String tempMin;
String tempMax;
String dateStr;
String weekStr;
String dayStr;
String monthStr;
int month;
/*Variables related to poems*/
int poemsCount = 86;
int indexMonth[12] = {180,170,205,205,225,215,215,195,160,190,170,170};


/* Entry point*/
void setup()
{
  /*Initialize the e-paper*/
  DEV_Module_Init();
  delay(3000);
  /*Connect to Wifi*/
  connectWifi(ssid, password);
  /*Set variables related to time*/
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  /*Refresh the information and display them on the screen*/
  refresh();
  /*Deep Sleep Mode*/
  deepSleep();
}

/* The main loop*/
void loop()
{
  /*Refresh the information every hour*/
  //sleep(3600);
  //refresh();
}

/* Connect to Wifi*/
void connectWifi(const char* ssid, const char* password){
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }  
    Serial.println("Wifi Connected");
}

/* Get current location*/
void getLocation(){
    String city;
    String province;
    WiFiClientSecure client;
    client.setInsecure();
    HTTPClient httpClient;
    String myIPAPI = "https://api.myip.la/en?jsonjson";
    int count = 0;
    /*Try to get information of city and province for 3 times*/
    while(count < 3){
      if (httpClient.begin(client, myIPAPI))
      {
          int httpCode = httpClient.GET();
          if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
          {
              String payload = httpClient.getString();
              DynamicJsonDocument doc(384);
              deserializeJson(doc, payload);           
              JsonObject location = doc["location"];
              city = location["city"].as<String>();       
              province = location["province"].as<String>();
              count = 5;
          }
          httpClient.end();
          client.stop();
          count+=1;
      }
      if(count < 3)
        delay(3000);
    }
    if(count == 3){
        city = "beijing";
        province = "beijing";
    }
    String heWeatherLocationAPI = "https://geoapi.qweather.com/v2/city/lookup?gzip=n&adm=" + province + "&location=" + city + "&key=" + heWeatherKey;
    count = 0;
    /*Try to get information of city name and locationID for 3 times*/
    while(count < 3){
      if (httpClient.begin(client, heWeatherLocationAPI))
      {
          int httpCode = httpClient.GET();
          if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
          {
              String payload = httpClient.getString();
              DynamicJsonDocument doc(8192);
              deserializeJson(doc, payload);  
              JsonArray locationArray = doc["location"];         
              JsonObject location = locationArray[0];
              cityCN = location["name"].as<String>();       
              locationID = location["id"].as<String>();
              count = 5;
          }
          httpClient.end();
          client.stop();
          count+=1;
      }
      if(count < 3)
        delay(3000);
    }
    if(count == 3)
    {
      /* Default location*/
      cityCN = "北京";       
      locationID = "101010100";
    }
    Serial.println(locationID);
    Serial.println(cityCN);
}

/* Get information of weather*/
void getWeatherInfo(){
    WiFiClientSecure client;
    client.setInsecure();
    HTTPClient httpClient;
    String heWeatherNowAPI = "https://devapi.qweather.com/v7/weather/now?gzip=n&location=" + locationID + "&key=" + heWeatherKey;
    int count = 0;
    /*Try to get information of weather for 3 times*/
    while(count < 3){
      if (httpClient.begin(client, heWeatherNowAPI))
      {
          int httpCode = httpClient.GET();
          if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
          {
              String payload = httpClient.getString();
              DynamicJsonDocument doc(1024);
              deserializeJson(doc, payload);           
              JsonObject nowWeather = doc["now"];
              temp = nowWeather["temp"].as<String>();       
              icon = nowWeather["icon"].as<String>();
              text = nowWeather["text"].as<String>();
              count = 5;
          }
          httpClient.end();
          client.stop();
          count += 1;
       }
       if(count < 3)
          delay(3000);
    }
    if(count == 3){
      /*Default weather*/
      temp = "N/A";      
      icon = "999";
      text = "未知";
    }
    Serial.println(temp);
    Serial.println(icon);
    Serial.println(text);
    /*Try to get information of weather for 3 times*/
    String heWeatherDailyAPI = "https://devapi.qweather.com/v7/weather/3d?gzip=n&location=" + String(locationID) + "&key=" + heWeatherKey;
    count = 0;
    while(count < 3)
    {
      if (httpClient.begin(client, heWeatherDailyAPI))
      {
          int httpCode = httpClient.GET();
          if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY)
          {
              String payload = httpClient.getString();
              DynamicJsonDocument doc(8192);
              deserializeJson(doc, payload);  
              JsonArray dailyArray = doc["daily"];         
              JsonObject dailyWeather = dailyArray[0];
              tempMin = dailyWeather["tempMin"].as<String>();       
              tempMax = dailyWeather["tempMax"].as<String>(); 
              count = 5;
          }
          httpClient.end();
          client.stop();
          count += 1;
       }
       if(count < 3)
          delay(3000);
    }
    if(count == 3){
      /*Default temp range*/
      tempMin = "N/A";      
      tempMax = "N/A";
    }
    Serial.println(tempMin);
    Serial.println(tempMax);
}

/* Get information of time*/
void getDateTime()
{
  struct tm timeinfo;
  int count = 0;
  /*Try to get information of time for 3 times*/
  while (count < 3){
    if(getLocalTime(&timeinfo))
    {
      count = 5;
    }
    else{
      count+=1;
      delay(3000);
    }
  }
  if(count == 3){
      dateStr = "2017/11/04";;
      weekStr = "Saturday";;
      dayStr = "04";
      monthStr = "November";
  }
  else{
    char dateInfo[20];
    strftime(dateInfo, sizeof(dateInfo), "%Y/%m/%d", &timeinfo);
    dateStr = String(dateInfo);
    char weekInfo[20];
    strftime(weekInfo, sizeof(weekInfo), "%A", &timeinfo);
    weekStr = String(weekInfo);
    char dayInfo[10];
    strftime(dayInfo, sizeof(dayInfo), "%d", &timeinfo);
    dayStr = String(dayInfo);
    char monthInfo[20];
    strftime(monthInfo, sizeof(monthInfo), "%B", &timeinfo);
    monthStr = String(monthInfo);
    month = timeinfo.tm_mon;
  }
  Serial.println(dateStr);
  Serial.println(weekStr);
  Serial.println(dayStr);
  Serial.println(monthStr);
}
/*Select the image of weather*/
const unsigned char* getImagePointer(){
  const unsigned char* p;
  int code = icon.toInt();
  switch(code){
    case 100:
        p = gImage_100;
        break;
    case 101:
        p = gImage_101;
        break;
    case 102:
        p = gImage_102;
        break;
    case 103:
        p = gImage_103;
        break;
    case 104:
        p = gImage_104;
        break;
    case 150:
        p = gImage_150;
        break;
    case 153:
        p = gImage_153;
        break;
    case 154:
        p = gImage_154;
        break;
    case 300:
        p = gImage_300;
        break;
    case 301:
        p = gImage_301;
        break;
    case 302:
        p = gImage_302;
        break;
    case 303:
        p = gImage_303;
        break;
    case 304:
        p = gImage_304;
        break;
    case 305:
        p = gImage_305;
        break;
    case 306:
        p = gImage_306;
        break;
    case 307:
        p = gImage_307;
        break;
    case 308:
        p = gImage_308;
        break;
    case 309:
        p = gImage_309;
        break;
    case 310:
        p = gImage_310;
        break;
    case 311:
        p = gImage_311;
        break;
    case 312:
        p = gImage_312;
        break;
    case 313:
        p = gImage_313;
        break;
    case 314:
        p = gImage_314;
        break;
    case 315:
        p = gImage_315;
        break;
    case 316:
        p = gImage_316;
        break;
    case 317:
        p = gImage_317;
        break;
    case 318:
        p = gImage_318;
        break;
    case 350:
        p = gImage_350;
        break;
    case 351:
        p = gImage_351;
        break;
    case 399:
        p = gImage_399;
        break;
    case 400:
        p = gImage_400;
        break;
    case 401:
        p = gImage_401;
        break;
    case 402:
        p = gImage_402;
        break;
    case 403:
        p = gImage_403;
        break;
    case 404:
        p = gImage_404;
        break;
    case 405:
        p = gImage_405;
        break;
    case 406:
        p = gImage_406;
        break;
    case 407:
        p = gImage_407;
        break;
    case 408:
        p = gImage_408;
        break;
    case 409:
        p = gImage_409;
        break;
    case 410:
        p = gImage_410;
        break;
    case 456:
        p = gImage_456;
        break;
    case 457:
        p = gImage_457;
        break;
    case 499:
        p = gImage_499;
        break;
    case 500:
        p = gImage_500;
        break;
    case 501:
        p = gImage_501;
        break;
    case 502:
        p = gImage_502;
        break;
    case 503:
        p = gImage_503;
        break;
    case 504:
        p = gImage_504;
        break;
    case 507:
        p = gImage_507;
        break;
    case 508:
        p = gImage_508;
        break;
    case 509:
        p = gImage_509;
        break;
    case 510:
        p = gImage_510;
        break;
    case 511:
        p = gImage_511;
        break;
    case 512:
        p = gImage_512;
        break;
    case 513:
        p = gImage_513;
        break;
    case 514:
        p = gImage_514;
        break;
    case 515:
        p = gImage_515;
        break;
    case 900:
        p = gImage_900;
        break;
    case 901:
        p = gImage_901;
        break;
    case 999:
        p = gImage_999;
        break;
    default:
        p = gImage_999;
        break;
  }
  return p;
}
/*Get index of X for poems*/
int getPoemX(int length){
  int indexX;
  switch(length){
    case 5:
      indexX = 180;
      break;
    case 6:
      indexX = 165;
      break;
    case 7:
      indexX = 150;
      break;
    default:
      indexX = 150;
      break;
  }
  return indexX;
}
/*Refresh the information and display them on the screen*/
void refresh(){
  if(WiFi.status() != WL_CONNECTED)
      connectWifi(ssid, password);
  getLocation();
  getWeatherInfo();
  getDateTime();
  EPD_4IN2_Init();
  EPD_4IN2_Clear();
  DEV_Delay_ms(500);
  /*Create a new image cache*/
  UBYTE *BlackImage;
  /* you have to edit the startup_stm32fxxx.s file and set a big enough heap size */
  UWORD Imagesize = ((EPD_4IN2_WIDTH % 8 == 0) ? (EPD_4IN2_WIDTH / 8 ) : (EPD_4IN2_WIDTH / 8 + 1)) * EPD_4IN2_HEIGHT;
  if ((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
    while (1);
  }
  Paint_NewImage(BlackImage, EPD_4IN2_WIDTH, EPD_4IN2_HEIGHT, 0, WHITE);
  Paint_SelectImage(BlackImage);
  Paint_Clear(WHITE);
  Paint_DrawString_EN(30, 10, dateStr.c_str(), &Font20, WHITE, BLACK);
  Paint_DrawString_EN(30, 45, weekStr.c_str(), &Font20, WHITE, BLACK);
  Paint_DrawString_CN(30, 80, cityCN.c_str(), &CityFont20CN, BLACK, WHITE);
  Paint_DrawImage(getImagePointer(), 30, 115, 64, 64); 
  Paint_DrawString_CN(30, 185, text.c_str(), &WeatherFont20CN, BLACK, WHITE);
  temp = temp + "C";
  Paint_DrawString_EN(30, 225, temp.c_str(), &Font20, WHITE, BLACK);
  String tempRange = tempMin + "C-" + tempMax + "C";
  Paint_DrawString_EN(30, 260, tempRange.c_str(), &Font20, WHITE, BLACK);
  Paint_DrawString_EN(210, 20, dayStr.c_str(), &Font80, WHITE, BLACK);
  Paint_DrawString_EN(indexMonth[month], 140, monthStr.c_str(), &Font30, WHITE, BLACK);
  int randomNum = random(poemsCount);
  Paint_DrawString_CN(getPoemX(strlen(Poems[randomNum * 2]) / 3), 200, Poems[randomNum * 2], &PoemsFont24CN, BLACK, WHITE);
  Paint_DrawString_CN(getPoemX(strlen(Poems[randomNum * 2 + 1]) / 3), 240, Poems[randomNum * 2 + 1], &PoemsFont24CN, BLACK, WHITE);
  EPD_4IN2_Display(BlackImage);
  DEV_Delay_ms(2000);
  free(BlackImage);
  BlackImage = NULL;
}
/*Deep Sleep Mode*/
void deepSleep(){
  EPD_4IN2_Init();
  EPD_4IN2_Clear();
  EPD_4IN2_Sleep();
}
