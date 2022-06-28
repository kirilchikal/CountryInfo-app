# CountryInfo-app
Dekstop app to find basic and most important information about all countries


### Description
The **App** class extends the components of the TKinter library and is responsible for handling user requests.
The classes and methods in the **Country_info.py** file are also responsible for the presentation of the user interface and program logic

After starting the program, user can enter the country by indicating its name or code. As the result there will be the following information:
- flag, full country name and code (alpha-2)
- local time of the country
- general and basic facts such as capital, official languages and currency, continent, border states etc.
- up-to-date data on covid cases
- current weather in the capital
Moreover, depending on the user's location, the distance from the selected country will be calculated (in kilometers). Also with the help of a currency calculator it is possible to convert user's local currency into the currency of the searched country and vice versa.
The user's location is determined automatically, but the user has the right to change his location.


### Interface
![image](https://user-images.githubusercontent.com/48454522/176184648-87f7f67e-986f-47a0-9f51-92fae8969b17.png)


### Resources used:
- Countries flags API: *https://www.countryflags.io*
- API for currency conversion: *https://www.currencyconverterapi.com*
- Weather API: *https://openweathermap.org/api*
- *https://www.worldometers.info/*
