import React, {useEffect, useState} from 'react';
import {useAuth} from "../context/Auth";
import {getAllAccounts} from "../http/accountsAPI";
import {Col, Container, Row, Spinner} from "react-bootstrap";
import {ErrorComponent} from "../components/ErrorComponent";
import BudgetCard from "../components/BudgetCard";
import MonthOperationsCard from "../components/MonthOperationsCard";
import {getAllOperations} from "../http/operationsAPI";
import {getCurrencyRate} from "../http/currencyAPI";
import {SUPPORTED_CURRENCIES} from "../utils/consts";
import LastOperationsCard from "../components/LastOperationsCard";
import CurrenciesBudgetCard from "../components/CurrenciesBudgetCard";
import AddRemoveButtons from "../components/AddRemoveButtons";

const MainPage = () => {
    const {user} = useAuth()
    const [isLoading, setIsLoading] = useState(true)
    const [data, setData] = useState(null)
    const [errorMsg, setErrorMsg] = useState(null)

    const getData = async () => {
        let accounts
        let operations
        try {
            accounts = await getAllAccounts()
            let currentDate = new Date()
            const firstDayOfPreviousMonth = new Date(
                currentDate.getFullYear(),
                currentDate.getMonth() - 1,
                1).toISOString().replace("Z", "")
            currentDate = currentDate.toISOString().replace("Z", "")
            operations = await getAllOperations(
                null,
                firstDayOfPreviousMonth,
                currentDate
            )
        } catch (e) {
            setErrorMsg(`Error with connecting to server, app may work incorrect. Error message: ${e}`)
        }
        return {operations: operations, accounts: accounts}
    }

    useEffect(() => {
        getData().then(data => {
            setData(data)
        }).finally(() => setIsLoading(false))
    }, [])

    return (<>
            {isLoading
                ?
                <Spinner
                    variant="border"
                    style={{position: 'absolute', top: window.innerHeight / 2 - 56, left: '50%'}}
                />
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
                        </Col>
                    </Row>
                    <AddRemoveButtons data={data}/>
                </Container>
            }
        </>
    );
};

export default MainPage;