import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {CURRENCIES_AND_SYMBOLS, INTERFACE_COLORS, OPERATIONS_ROUTE, SUPPORTED_CURRENCIES} from "../../utils/consts";
import {Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import {convertCurrency} from "../../utils/currency";
import {Spinner} from "react-bootstrap";

const LastSevenDaysOperationsCard = ({data, setErrorMsg}) => {
    const [operationData, setOperationData] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    const calcTotalAmountOfOperations = async (operations) => {
        let totalAmount = 0
        let amountInUSD
        for (let operation of operations) {
            if (operation["currency"] !== SUPPORTED_CURRENCIES.USD) {
                amountInUSD = await convertCurrency(operation["amount"], operation["currency"], SUPPORTED_CURRENCIES.USD)
            } else {
                amountInUSD = operation["amount"]
            }
            totalAmount += amountInUSD
        }
        return totalAmount
    }

    const getLastSevenOperationData = async () => {
        let startDate
        let endDate
        let filteredIncomes
        let filteredSpendings
        let tempOperationData = []
        for (let i = 0; i < 7; i++) {
            startDate = new Date()
            endDate = new Date()
            startDate.setDate(startDate.getDate() - i)
            endDate.setDate(endDate.getDate() - i)
            startDate.setUTCHours(0, 0, 0, 0)
            endDate.setUTCHours(23, 59, 59, 999)
            console.log(startDate, endDate)
            console.log(data.operations.incomes)
            filteredIncomes = data.operations.incomes.filter(income => new Date(income["created_at"]) >= startDate && new Date(income["created_at"]) < endDate)
            filteredSpendings = data.operations.spendings.filter(spending => new Date(spending["created_at"]) >= startDate && new Date(spending["created_at"]) < endDate)

            tempOperationData.push({
                name: startDate.toLocaleDateString('en-GB', {month: "numeric", day: "numeric", weekday: "short"}),
                Incomes: (await calcTotalAmountOfOperations(filteredIncomes)).toFixed(2),
                Spendings: (await calcTotalAmountOfOperations(filteredSpendings)).toFixed(2)
            })
        }
        return tempOperationData
    }

    useEffect(() => {
        getLastSevenOperationData().then((d) => {
            setOperationData(d);
            console.log(operationData)
        }).finally(() => {
            setIsLoading(false)
        })
    }, [])

    return (
        <MainPageCard navigateto={OPERATIONS_ROUTE} className="mt-3">
            <b>Last 7 days</b>
            {isLoading ? <div className="mt-3 d-flex justify-content-center align-items-center"><Spinner variant="border"/></div> :
                <>
                    <div className="mt-3" style={{width: "100%", height: "300px"}}>
                        <ResponsiveContainer>
                            <BarChart
                                data={operationData.reverse()}
                                margin={{
                                    top: 5,
                                    right: 30,
                                    left: 20,
                                    bottom: 5
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="name"/>
                                <YAxis unit={CURRENCIES_AND_SYMBOLS.USD}/>
                                <Tooltip/>
                                <Legend/>
                                <Bar dataKey="Incomes" fill={INTERFACE_COLORS.GREEN}/>
                                <Bar dataKey="Spendings" fill={INTERFACE_COLORS.RED}/>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </>
            }
        </MainPageCard>
    );
};

export default LastSevenDaysOperationsCard;