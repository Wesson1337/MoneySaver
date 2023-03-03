import {getLatestExchangeRates} from "../http/currencyAPI";
import {SUPPORTED_CURRENCIES} from "./consts";

export const convertCurrency =  async (amount, baseCurrency, desiredCurrency) => {
    if (!(baseCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Base currency is not supported in app")
    }
    if (!(desiredCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Desired currency is not supported in app")
    }
    const {data} = await getLatestExchangeRates(baseCurrency)
    return amount * data[desiredCurrency]
}