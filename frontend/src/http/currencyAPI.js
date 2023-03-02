import axios from "axios";

export const getLatestExchangeRates = async (baseCurrency) => {
    const {data} = await axios({
         method: "get",
         url: "https://api.freecurrencyapi.com/v1/latest",
         params: {
             apikey: process.env.REACT_APP_CURRENCY_API_KEY,
             base_currency: baseCurrency
         }
     })
    return data
}