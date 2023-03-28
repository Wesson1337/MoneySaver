import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {ACCOUNTS_ROUTE} from "../utils/consts";
import {Spinner} from "react-bootstrap";
import Currency from "./Currency";
import Sort from "./Sort";

const CurrenciesBudgetCard = (props) => {
    const [showModal, setShowModal] = useState(false)
    const [currenciesAndBalance, setCurrenciesAndBalance] = useState(null)
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalanceInUSD, setTotalBalanceInUSD] = useState(null)

    const getCurrenciesAndBalance = () => {
        let currAndBalance = {}
        let totalInUSD = 0
        for (const account of props.data.accounts) {
            if (account["currency"] in currAndBalance) {
                currAndBalance[account["currency"]]["USD"] += account["balance"]
                currAndBalance[account["currency"]]["USD"] += account["balanceInUSD"]
            } else {
                currAndBalance[account["currency"]] = {}
                currAndBalance[account["currency"]]["balance"] = account["balance"]
                currAndBalance[account["currency"]]["USD"] = account["balanceInUSD"]
            }
            totalInUSD += account["balanceInUSD"]
        }
        setTotalBalanceInUSD(totalInUSD)
        setCurrenciesAndBalance(currAndBalance)
        setIsLoading(false)
    }

    useEffect(() => {
        getCurrenciesAndBalance()
    }, [])

    return (
        <MainPageCard navigateto={ACCOUNTS_ROUTE} showModal={showModal}>
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
                                    percent={((currenciesAndBalance[currency]["USD"] / totalBalanceInUSD) * 100).toFixed(0)}
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