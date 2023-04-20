import React, {useEffect, useState} from 'react';
import {Card, Container, Spinner} from "react-bootstrap";
import {getAllAccounts} from "../http/accountsAPI";
import {convertCurrency} from "../utils/currency";
import {CURRENCIES_AND_SYMBOLS, SUPPORTED_CURRENCIES} from "../utils/consts";
import {prettifyFloat} from "../utils/prettifyFloat";

const Accounts = () => {
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalance, setTotalBalance] = useState(null)
    const [accounts, setAccounts] = useState(null)

    const addUSDBalanceToAccounts = async (accounts) => {
        let balanceInUSD
        for (const account of accounts) {
            balanceInUSD = await convertCurrency(account["balance"], account["currency"], SUPPORTED_CURRENCIES.USD)
            account["balanceInUSD"] = Number(balanceInUSD.toFixed(5))
        }
        return accounts
    }

    const getAccounts = async () => {
        return await addUSDBalanceToAccounts(await getAllAccounts())
    }

    useEffect(() => {
        getAccounts().then((v) => {
            setAccounts(v)
        }).finally(() => {setIsLoading(false)})
    }, [])

    const getTotalBalance = () => {
        let totalBalance = 0;
        let a
        let accountBalance
        if (accounts !== null) {
            for (let i = 0; i < accounts.length; i++) {
                a = accounts[i]
                if (a["is_active"]) {
                    accountBalance = a["balanceInUSD"]
                    totalBalance += accountBalance
                }
            }
            return totalBalance.toFixed(2)
        }
    }

    return (
        <Container>
            {isLoading ? <div
                    className="w-100 d-flex align-items-center justify-content-center"
                    style={{height: window.innerHeight - 56}}
                ><Spinner variant="border"/></div> :
                <>
                    <Card className="d-flex p-3 justify-content-between align-items-center flex-row mt-3">
                        <p className="m-0 h4">Total balance: </p>
                        <p className="m-0">{prettifyFloat(getTotalBalance())} {CURRENCIES_AND_SYMBOLS.USD}</p>

                    </Card>
                </>
            }
        </Container>

    );
};

export default Accounts;