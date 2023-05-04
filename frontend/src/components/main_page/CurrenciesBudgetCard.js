import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {ACCOUNTS_ROUTE} from "../../utils/consts";
import {Spinner} from "react-bootstrap";
import Currency from "./Currency";
import Sort from "../common/Sort";

const CurrenciesBudgetCard = ({data}) => {
    const [currenciesAndBalance, setCurrenciesAndBalance] = useState({})
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalanceInUSD, setTotalBalanceInUSD] = useState(null)

    const getCurrenciesAndBalance = () => {
        let currAndBalance = {}
        let totalInUSD = 0
        for (const account of data.accounts) {
            if (account.is_active) {
                if (account.currency in currAndBalance) {
                    currAndBalance[account["currency"]].balance += account.balance
                    currAndBalance[account["currency"]].USD += account.balanceInUSD
                } else {
                    currAndBalance[account["currency"]] = {}
                    currAndBalance[account["currency"]].balance = account.balance
                    currAndBalance[account["currency"]].USD = account.balanceInUSD
                }
                totalInUSD += account.balanceInUSD
            }
        }
        setTotalBalanceInUSD(totalInUSD)
        setCurrenciesAndBalance(currAndBalance)
        setIsLoading(false)
    }

    useEffect(() => {
        getCurrenciesAndBalance()
    }, [])

    return (
        <MainPageCard navigateto={ACCOUNTS_ROUTE}>
            {isLoading ?
                <div className="d-flex justify-content-center align-items-center"><Spinner variant="border"/></div> :
                <div className="d-flex flex-column gap-3">
                    <b className="text-nowrap">Balance (Currencies)</b>
                    <div className="d-flex flex-column gap-2">
                        <Sort by="percent">
                            {Object.keys(currenciesAndBalance).map((currency) => (
                                <Currency
                                    key={currency}
                                    currency={currency}
                                    balance={currenciesAndBalance[currency]["balance"]}
                                    percent={((currenciesAndBalance[currency]["USD"] / totalBalanceInUSD) * 100).toFixed(2)}
                                />
                            ))}
                        </Sort>
                    </div>
                </div>
            }

        </MainPageCard>
    );
};

export default CurrenciesBudgetCard;