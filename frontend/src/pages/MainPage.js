import React, {useEffect, useState} from 'react';
import {getAllAccounts} from "../http/accountsAPI";
import {Col, Container, Row, Spinner} from "react-bootstrap";
import {ErrorComponent} from "../components/common/ErrorComponent";
import BudgetCard from "../components/main_page/BudgetCard";
import MonthTransactionsCard from "../components/main_page/MonthTransactionsCard";
import {getAllTransactions} from "../http/transactionsAPI";
import {SUPPORTED_CURRENCIES} from "../utils/consts";
import LastTransactionsCard from "../components/main_page/LastTransactionsCard";
import CurrenciesBudgetCard from "../components/main_page/CurrenciesBudgetCard";
import AddTransactionButtons from "../components/common/AddTransactionButtons";
import {convertCurrency} from "../utils/currency";
import LastSevenDaysTransactionsCard from "../components/main_page/LastSevenDaysTransactionsCard";

const MainPage = () => {
    const [isLoading, setIsLoading] = useState(true)
    const [data, setData] = useState(null)
    const [errorMsg, setErrorMsg] = useState(null)
    const [dataHasChanged, setDataHasChanged] = useState(false)

    const addUSDBalanceToAccounts = async (accounts) => {
        let balanceInUSD
        for (const account of accounts) {
            balanceInUSD = await convertCurrency(account["balance"], account["currency"], SUPPORTED_CURRENCIES.USD)
            account["balanceInUSD"] = Number(balanceInUSD.toFixed(5))
        }
        return accounts
    }

    const getData = async () => {
        setIsLoading(true)
        let accounts
        let operations
        try {
            accounts = await addUSDBalanceToAccounts(await getAllAccounts())
            let currentDate = new Date()
            const firstDayOfPreviousMonth = new Date(
                currentDate.getFullYear(),
                currentDate.getMonth() - 1,
                1).toISOString()
            currentDate = currentDate.toISOString()
            operations = await getAllTransactions(
                null,
                firstDayOfPreviousMonth,
                currentDate
            )
            return {operations: operations, accounts: accounts}
        } catch (e) {
            setErrorMsg(`Error with connecting to server, app may work incorrect. Error message: ${e.response.data.detail || e}`)
        }
    }

    useEffect(() => {
        getData().then(data => {
            if (data) {
                setData(data);
                setIsLoading(false)
            }
        })
    }, [dataHasChanged])

    return (<>
            {isLoading ? <div
                    className="w-100 d-flex align-items-center justify-content-center"
                    style={{height: window.innerHeight - 56}}
                ><Spinner animation="border"/></div>
                :
                <Container className="px-3">
                    <ErrorComponent message={errorMsg} onClose={() => setErrorMsg(null)}/>
                    <Row>
                        <Col className="g-3">
                            <BudgetCard data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                        <Col className="g-3">
                            <MonthTransactionsCard month="this-month" data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                        <Col className="g-3">
                            <MonthTransactionsCard month="previous-month" data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                    </Row>
                    <Row>
                        <Col className="g-3">
                            <LastTransactionsCard data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                        <Col className="g-3">
                            <CurrenciesBudgetCard data={data} setErrorMsg={setErrorMsg}/>
                            <LastSevenDaysTransactionsCard data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                    </Row>
                    <AddTransactionButtons data={data} setErrorMsg={setErrorMsg} hasChanged={dataHasChanged} setHasChanged={setDataHasChanged}/>
                </Container>
            }
        </>
    );
};

export default MainPage;