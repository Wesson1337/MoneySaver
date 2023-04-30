import React, {useEffect, useState} from 'react';
import {getAllAccounts} from "../http/accountsAPI";
import {Col, Container, Row, Spinner} from "react-bootstrap";
import {ErrorComponent} from "../components/common/ErrorComponent";
import BudgetCard from "../components/main_page/BudgetCard";
import MonthOperationsCard from "../components/main_page/MonthOperationsCard";
import {getAllOperations} from "../http/operationsAPI";
import {SUPPORTED_CURRENCIES} from "../utils/consts";
import LastOperationsCard from "../components/main_page/LastOperationsCard";
import CurrenciesBudgetCard from "../components/main_page/CurrenciesBudgetCard";
import AddRemoveButtons from "../components/common/AddRemoveButtons";
import {convertCurrency} from "../utils/currency";
import LastSevenDaysOperationsCard from "../components/main_page/LastSevenDaysOperationsCard";

const MainPage = () => {
    const [isLoading, setIsLoading] = useState(true)
    const [data, setData] = useState(null)
    const [errorMsg, setErrorMsg] = useState(null)

    const addUSDBalanceToAccounts = async (accounts) => {
        let balanceInUSD
        for (const account of accounts) {
            balanceInUSD = await convertCurrency(account["balance"], account["currency"], SUPPORTED_CURRENCIES.USD)
            account["balanceInUSD"] = Number(balanceInUSD.toFixed(5))
        }
        return accounts
    }

    const getData = async () => {
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
            operations = await getAllOperations(
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
    }, [])

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
                            <MonthOperationsCard month="this-month" data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                        <Col className="g-3">
                            <MonthOperationsCard month="previous-month" data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                    </Row>
                    <Row>
                        <Col className="g-3">
                            <LastOperationsCard data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                        <Col className="g-3">
                            <CurrenciesBudgetCard data={data} setErrorMsg={setErrorMsg}/>
                            <LastSevenDaysOperationsCard data={data} setErrorMsg={setErrorMsg}/>
                        </Col>
                    </Row>
                    <AddRemoveButtons data={data} setErrorMsg={setErrorMsg}/>
                </Container>
            }
        </>
    );
};

export default MainPage;