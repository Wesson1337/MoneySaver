import {getCurrencyRate} from "../http/currencyAPI";
import {SUPPORTED_CURRENCIES} from "./consts";

export const convertCurrency = async (amount, baseCurrency, desiredCurrency) => {
    if (!(baseCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Base currency is not supported in app")
    }
    if (!(desiredCurrency in SUPPORTED_CURRENCIES)) {
        throw new Error("Desired currency is not supported in app")
    }
    if (baseCurrency === desiredCurrency || amount === 0) {
        return amount
    }
    const rate = await getCurrencyRate(baseCurrency, desiredCurrency)
    return amount * rate
}