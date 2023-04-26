import React, {useEffect, useState} from 'react';
import {Card, Container, Spinner} from "react-bootstrap";
import {getAllAccounts} from "../http/accountsAPI";
import {convertCurrency} from "../utils/currency";
import {CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS, SUPPORTED_CURRENCIES} from "../utils/consts";
import {prettifyFloat} from "../utils/prettifyFloat";
import {ErrorComponent} from "../components/common/ErrorComponent";
import Account from "../components/account_page/Account";

const Accounts = () => {
    const [isLoading, setIsLoading] = useState(true)
    const [totalBalance, setTotalBalance] = useState(null)
    const [accounts, setAccounts] = useState([])
    const [errorMsg, setErrorMsg] = useState(null)

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
        }).finally(() => {
            setIsLoading(false)
        })
    }, [])

    const getTotalBalance = () => {
        let totalBalance = 0;
        let a
        let accountBalance
        if (accounts) {
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
                    <ErrorComponent
                        message={errorMsg}
                        onClose={() => setErrorMsg(null)}
                    />
                    <Card
                        className="d-flex p-3 justify-content-between align-items-center flex-row mt-3"
                    >
                        <h4
                            className="m-0"
                        >Total balance: </h4>
                        <h4
                            className="m-0 text-nowrap"
                            style={{color: INTERFACE_COLORS.GREEN}}
                        >{prettifyFloat(getTotalBalance())} {CURRENCIES_AND_SYMBOLS.USD}</h4>
                    </Card>
                    <div className="d-flex flex-column gap-3 mt-3">
                        {Object.values(accounts).map((account, index) => (
                            <Account
                                key={`account-${account["id"]}`}
                                index={index}
                                account={account}
                            />
                        ))}
                    </div>
                </>
            }
        </Container>

    );
};

export default Accounts;