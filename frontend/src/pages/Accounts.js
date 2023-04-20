import React, {useEffect, useState} from 'react';
import {Card, Container, Spinner} from "react-bootstrap";
import {getAllAccounts} from "../http/accountsAPI";
import {convertCurrency} from "../utils/currency";
import {CURRENCIES_AND_SYMBOLS, SUPPORTED_CURRENCIES} from "../utils/consts";
import {prettifyFloat} from "../utils/prettifyFloat";

const Accounts = () => {

    const [isLoading, setIsLoading] = useState(true)
    const [totalBalance, setTotalBalance] = useState(null)

    const addUSDBalanceToAccounts = async (accounts) => {
        let balanceInUSD
        for (const account of accounts) {
            balanceInUSD = await convertCurrency(account["balance"], account["currency"], SUPPORTED_CURRENCIES.USD)
            account["balanceInUSD"] = Number(balanceInUSD.toFixed(5))
        }
        return accounts
    }

    const getTotalBalance = async () => {
        const accounts = await addUSDBalanceToAccounts(await getAllAccounts())
        let totalBalance = 0;
        let a
        let accountBalance
        for (let i = 0; i < accounts.length; i++) {
            a = accounts[i]
            if (a["is_active"]) {
                accountBalance = a["balanceInUSD"]
                totalBalance += accountBalance
            }
        }
        return totalBalance.toFixed(2)
    }

    useEffect(() => {
        getTotalBalance().then((v) => {
            setTotalBalance(v)
        }).finally(() => {
            setIsLoading(false)
        })
    }, [])

    return (
    <Container>
        { isLoading ? <Spinner/> :
            <>
        <Card className="d-flex p-3 justify-content-between align-items-center flex-row mt-3">
            <p className="m-0 h4">Total balance: </p>
            <p className="m-0">{prettifyFloat(totalBalance)} {CURRENCIES_AND_SYMBOLS.USD}</p>

        </Card>
        </>
        }
    </Container>

    );
};

export default Accounts;