import axios from "axios";
import {SUPPORTED_CURRENCIES} from "../utils/consts";

export const getLatestExchangeRates = async (baseCurrency) => {
    if (!(baseCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Base currency is not supported in app")
    }
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