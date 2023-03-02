import {getLatestExchangeRates} from "../http/currencyAPI";

export const convertCurrency =  async (amount, baseCurrency, desiredCurrency) => {
    const {data} = await getLatestExchangeRates(baseCurrency)
    return amount * data[desiredCurrency]
}