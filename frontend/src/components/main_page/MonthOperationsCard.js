import React, {useEffect, useState} from 'react';
import MainPageCard from "./MainPageCard";
import {OPERATIONS_ROUTE, SUPPORTED_CURRENCIES} from "../../utils/consts";
import {Cell, Pie, PieChart, Tooltip} from "recharts";
import {convertCurrency} from "../../utils/currency";
import {Spinner} from "react-bootstrap";


const MonthOperationsCard = (props) => {
    const [isLoading, setIsLoading] = useState(true)
    const [totalIncomeAmount, setTotalIncomeAmount] = useState(0)
    const [totalSpendingAmount, setTotalSpendingAmount] = useState(0)

    const dataForPie = [
        {name: "Incomes", value: totalIncomeAmount},
        {name: "Spendings", value: totalSpendingAmount},
    ];

    const filterOperationsByMonth = (operations) => {
        let filteredIncomes
        let filteredSpendings
        const date = new Date()
        if (props.month === "this-month") {
            date.setDate(1)
            filteredSpendings = operations.spendings.filter(
                spending => new Date(spending["created_at"]) >= date
            )
            filteredIncomes = operations.incomes.filter(
                income => new Date(income["created_at"]) >= date
            )
        } else {
            date.setMonth(date.getMonth() - 1)
            date.setDate(1)
            filteredSpendings = operations.spendings.filter(
                spending => new Date(spending["created_at"]) >= date && new Date(spending["created_at"]) < new Date(date.getFullYear(), date.getMonth() + 1, 1)
            )
            filteredIncomes = operations.incomes.filter(
                income => new Date(income["created_at"]) >= date && new Date(income["created_at"]) < new Date(date.getFullYear(), date.getMonth() + 1, 1)
            )
        }
        return {incomes: filteredIncomes, spendings: filteredSpendings}
    }

    const getTotalAmountOfIncomes = async (operations, type) => {
        let totalAmount = 0
        let convertedAmount
        const account = type === "spendings" ? "receipt_account" : "replenishment_account"
        await operations.map(async op => {
            if (op[account]["currency"] !== SUPPORTED_CURRENCIES.USD) {
                convertedAmount = await convertCurrency(
                    op["amount_in_account_currency_at_creation"],
                    op[account]["currency"],
                    SUPPORTED_CURRENCIES.USD,
                    props.data.latestExchangeRates
                )
                totalAmount += convertedAmount
            } else {
                totalAmount += op["amount_in_account_currency_at_creation"]
            }
        })
        return totalAmount
    }


    const getTotalAmountOfOperations = async () => {
        try {
            const filteredOperations = filterOperationsByMonth(props.data.operations)
            const totalIncomeAmount = await getTotalAmountOfIncomes(filteredOperations.incomes, "incomes")
            const totalSpendingAmount = await getTotalAmountOfIncomes(filteredOperations.spendings, "spendings")
            return {incomes: totalIncomeAmount, spendings: totalSpendingAmount}
        } catch (e) {
            props.setErrorMsg(`${e}`)
        }
    }

    useEffect(() => {
        getTotalAmountOfOperations().then(d => {
            setTotalIncomeAmount(d.incomes);
            setTotalSpendingAmount(d.spendings)
        }).finally(() => setIsLoading(false))
    })

    const CustomTooltip = ({active, payload}) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip p-1 d-flex align-items-center justify-content-center"
                     style={{background: "rgba(255, 255, 255, 1)"}}
                >
                    <p className="label m-0 text-nowrap">{`${payload[0].name} : ${payload[0].value.toFixed(2)}$`}</p>
                </div>
            );
        }
        return null;
    };

    const renderCustomizedLabel = ({cx, cy, midAngle, innerRadius, outerRadius, percent}) => {
        const RADIAN = Math.PI / 180;
        const radius = innerRadius + (outerRadius - innerRadius) * 0.4;
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);

        return (
            <text
                x={x}
                y={y}
                fill="black"
                fontSize="12"
                textAnchor="middle"
                dominantBaseline="central"
            >
                {`${(percent * 100).toFixed(1)}%`}
            </text>
        );
    };
    return (
        <MainPageCard
            navigateto={OPERATIONS_ROUTE}
            style={{
                minWidth: "350px"
            }}
        >
            {isLoading ? <Spinner variant="border"/> :
            <div className="d-flex flex-row justify-content-between align-items-center w-100"
            >
                <PieChart width={100} height={100} style={{cursor: "pointer"}}>
                    <Pie
                        animationBegin={200}
                        animationDuration={700}
                        dataKey="value"
                        data={dataForPie}
                        innerRadius={20}
                        outerRadius={50}
                        labelLine={false}
                        label={renderCustomizedLabel}
                        fill="#8884d8"
                    >
                        {dataForPie.map((entry) => (
                            <Cell style={{outline: "none"}} fill={entry["name"] === "Incomes" ? "#428345" : "#d93838"}/>
                        ))}
                    </Pie>
                    <Tooltip content={<CustomTooltip/>} wrapperStyle={{outline: "1px solid black", borderRadius: "3px"}}/>
                </PieChart>
                <div>
                    <p className="m-0">{totalIncomeAmount.toFixed(2)} $</p>
                    <p className="m-0">-{totalSpendingAmount.toFixed(2)} $</p>
                    <p className="m-0">{(totalIncomeAmount - totalSpendingAmount).toFixed(2)} $</p>
                </div>
            </div>}
        </MainPageCard>
    );
};

export default MonthOperationsCard;