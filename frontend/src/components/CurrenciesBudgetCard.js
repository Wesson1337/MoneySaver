import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {ACCOUNTS_ROUTE, SUPPORTED_CURRENCIES} from "../utils/consts";
import {Spinner} from "react-bootstrap";
import {convertCurrency} from "../utils/currency";

const CurrenciesBudgetCard = (props) => {
    const [showModal, setShowModal] = useState(false)
    const [currenciesAndBalance, setCurrenciesAndBalance] = useState(null)
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalance, setTotalBalance] = useState(null)

    const getCurrenciesAndBalance = () => {
        let currAndBalance = {}
        let total = 0
        for (const account of props.data.accounts) {
            if (account["currency"] in currAndBalance) {
                currAndBalance[account["currency"]] += account["balanceInUSD"]
            } else {
                currAndBalance[account["currency"]] = account["balanceInUSD"]
            }
            total += account["balanceInUSD"]
        }
        setTotalBalance(total)
        setCurrenciesAndBalance(currAndBalance)
        setIsLoading(false)
    }

    useEffect(() => {
        getCurrenciesAndBalance()
    }, [])

    return (
        <MainPageCard navigateto={ACCOUNTS_ROUTE} showModal={showModal}>
            {isLoading ? <div className="d-flex justify-content-center align-items-center"><Spinner variant="border"/></div> :
                <>
                    <b className="text-nowrap">Balance (Currencies)</b>
                    {Object.keys(currenciesAndBalance).map((currency) => (
                        <b>{((currenciesAndBalance[currency] / totalBalance) * 100).toFixed(0)}</b>
                    ))}
                </>
            }

        </MainPageCard>
    );
};

export default CurrenciesBudgetCard;